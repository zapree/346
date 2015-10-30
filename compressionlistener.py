#!/usr/bin/env python

"""
Receives messages via AWS SQS 'compressqueue' queue. Runs forever,
so you will have to use ^C to kill it.

NOTE: make sure you have a ~/.boto file containing
your AWS credentials.
"""

import boto.sqs
import time
import gzip
import shutil
import dropbox
import sys
import ConfigParser

__author__ = 'Eugene'

config = ConfigParser.RawConfigParser()
config.read("settings.cfg")

token = config.get('Dropbox', 'token')


def compress(fileloc):
    client = dropbox.client.DropboxClient(token)

    f, metadata = client.get_file_and_metadata(fileloc)
    #print f.read()
    #just saving

    with gzip.open('temp.gz', 'wb') as f_out:
        shutil.copyfileobj(f, f_out)
    with open('temp.gz', 'rb') as f_out:
        try:
            print "compressing "+fileloc
            client.put_file(fileloc+'.gz', f_out, overwrite=True)

        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
    conn = boto.sqs.connect_to_region("us-west-2")
    q = conn.create_queue('compressqueue', 30) # 30-second message visibility
    if q is None:
        print "could not create or connect to queue"


    else:
        while True:
            m = q.read(wait_time_seconds = 3) # wait up to 3 seconds for message
            if m is None:
                print "NO MESSAGE"
            else:
                print "message recieved"
                compress(m.get_body())
                q.delete_message(m)
