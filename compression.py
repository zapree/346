#!/usr/bin/python
import gzip
import shutil
import dropbox
import sys
import ConfigParser



__author__ = 'Eugene'

settingsfile = 'settings.cfg'

def compress(fileloc):

    config = ConfigParser.RawConfigParser()
    config.read("settings.cfg")

    token = config.get('Dropbox', 'token')
    client = dropbox.client.DropboxClient(token)

    f, metadata = client.get_file_and_metadata(fileloc)
    print f.read()
    #just saving

    with gzip.open('temp.gz', 'wb') as f_out:
        shutil.copyfileobj(f, f_out)
    with open('temp.gz', 'rb') as f_out:
        try:
            client.put_file(fileloc+'.gz', f_out, overwrite=True)

        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
    compress(sys.argv[1])
