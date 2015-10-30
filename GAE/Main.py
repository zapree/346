from flask import Flask
from flask import request
from flask import abort
from hashlib import sha256
from google.appengine.api import taskqueue
from boto.sqs.message import Message
import hmac
import boto
import dropbox
import ConfigParser

app = Flask(__name__)

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')
dbxsecret = config.get('Dropbox', 'secret')

aws_id = config.get('AWS', 'aws_access_key_id')
aws_secret = config.get('AWS', 'aws_secret_access_key')
queue_name = 'compressqueue'
region = 'us-west-2'

#in the AWS instance we have a .boto config, but since
#there is no home directoy, not sure where to put that
#so we put the aws access stuff in the settings file as well
aws_sqs = boto.sqs.connect_to_region(region,
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret)

@app.route('/')
def mainpage():
    return ''


#verify webhook by responding with challenge
@app.route('/webhook', methods=['GET'])
def verify():
    return request.args.get('challenge')


#get a change signal from the webhook
#send it to delta processing through task queue
@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Dropbox-Signature')
    if signature != hmac.new(dbxsecret, request.data, sha256).hexdigest():
        abort(403)

    #put it into the queue
    taskqueue.add(url='/DeltaPT')
    return ''


@app.route('/DeltaPT', methods=['POST'])
def ProcessDelta():
    if request.headers.get('X-AppEngine-QueueName') is None:
        # Ignore if not from AppEngine
        abort(403)

    client = dropbox.client.DropboxClient(token)
    try:
        #see if we can grab the cursor file from dropbox
        f = client.get_file('/.cursor')
        cursor = f.read()
    except:
        #if we can't, set cursor to none and it will
        #get all of the changes, then we write to it
        cursor = None

    delta = client.delta(cursor)

    for filepath, data in delta['entries']:
        #check that there is an entry, and that it isn't a cursor
        if (data is not None) and (filepath != '/.cursor'):
            #check for directories and compressed files
            if not data['is_dir'] and not filepath.endswith('.gz'):
                #we have something we want to process
                q = aws_sqs.create_queue(queue_name, 30)
                message = Message()
                message.set_body(filepath)
                q.write(message)

                #write the changes to the cursor file in dropbox
                cursor = delta['cursor']
                client.put_file('/.cursor', cursor, overwrite=True)



