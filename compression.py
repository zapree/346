#!/usr/bin/python
import gzip
import shutil
import dropbox
import sys, getopt


__author__ = 'Eugene'

settingsfile = 'settings.cfg'

def compress(fileloc):

#TODO:  open connection to dbx replace file with file location
    with open(fileloc, 'rb') as f_in, gzip.open(fileloc+'.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

#TODO:  write to dbx with compressed file


if __name__ == '__main__':
    compress(sys.argv[1])