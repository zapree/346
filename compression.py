#!/usr/bin/python
import gzip
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


    with f.read() as f_in, gzip.open('temp.gz', 'wb') as f_out:
        try:
            client.put_file(fileloc+'.gz', gzip.GzipFile(fileobj=f),overwrite=True)
        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
    compress(sys.argv[1])