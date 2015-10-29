from flask import Flask
from flask import abort
from pprint import pprint
import dropbox
import ConfigParser
from time import ctime

app = Flask(__name__)

cursor = None
deltalist = list()
timelist = list()

# app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

config = ConfigParser.RawConfigParser()
config.read("settings.cfg")
token = config.get('Dropbox', 'token')

client = dropbox.client.DropboxClient(token)
dbx = dropbox.Dropbox(token)

# print client



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handle_url(path):
    # handles all URLs
    if ("changes.txt" in path):
        return changes()
    try:
        metadata = client.metadata('/' + path)
    except:
        abort(404)
    print metadata['is_dir']
    if (metadata['is_dir']):
        return get_index(metadata)
    else:
        return getfile(metadata)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL. error 404', 404


def changes():
    global cursor
    global deltalist
    global timelist
    returnstring = "<br/>"
    while True:
        delta = client.delta(cursor)
        cursor = delta['cursor']
        for x in delta['entries']:
            deltalist.append(x[1])
            timelist = timelist + [ctime()]
        pprint(delta)
        if (delta['has_more'] is False):
            break
    if (len(deltalist) > 20):
        deltalist = deltalist[-20:0]
        timelist = timelist[-20:0]
    pprint(timelist)
    for file, time in zip(deltalist, timelist):
        pprint(file)
        pprint(time)
        if file != None:
            returnstring = returnstring + time + "\t" + file["path"] + "\tmodify<br/>"
        else:
            returnstring = returnstring + time + "\t" + "\tdelete<br/>"

    return returnstring


def getfile(metadata):
    try:
        f, metadata = client.get_file_and_metadata(metadata['path'])
    except:
        return "Couldn't access the file you were looking for"

    return f.read()


def get_index(metadata):
    print metadata
    for filename in [x["path"] for x in metadata['contents']]:
        if ("index.html" in filename):
            print metadata
            f, metadata = client.get_file_and_metadata(filename)
            return f.read()

    abort(404)
