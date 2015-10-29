import dropbox
import ConfigParser

__author__ = 'Eugene'


def dbxconnect(settingsfile):
    """connect to dropbox"""

    config = ConfigParser.RawConfigParser()
    try:
        config.read(settingsfile)
    except:
        print "invalid settings file"
        return None

    _token = config.get('Dropbox', 'token')

    try:
        dbx = dropbox.Dropbox(_token)
    except:
        print "could not connect"
        return None

    return dbx