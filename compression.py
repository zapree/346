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

    try:
        md, res = client.files_download(fileloc)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None
    data = res.content
    print data

    with gzip.open('temp.gz', 'wb') as f_out:
        f_out.write(data)
        try:
            client.files_upload(f_out, fileloc+'.gz', mode=dropbox.files.WriteMode.overwrite)
        except:
            print "Unexpected error:", sys.exc_info()[0]

if __name__ == '__main__':
    compress(sys.argv[1])
