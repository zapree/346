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
    client = dropbox.Dropbox(token)

    metadata, f = client.files_download(fileloc)
    print f.content

    with gzip.open('temp.gz', 'wb') as f_out:
        shutil.copyfileobj(f.content, f_out)
        try:
            filename = '/'+fileloc+'.gz'
            print filename
            client.files_upload(f_out, filename, mode=dropbox.files.WriteMode.overwrite)
        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
    compress(sys.argv[1])