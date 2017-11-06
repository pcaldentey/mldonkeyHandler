#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import urllib
import cookielib
import os
import commands
import sys
import re
import time
from mldonkey import *
import datetime
from ConfigParser import ConfigParser
from sgmllib import SGMLParser

def main():
    actual_dir = os.path.dirname( __file__ )
    configfile = actual_dir + '/donkeylinkscrawler.ini'

    # Get configuration
    config = ConfigParser()
    config.read([configfile])

    ml_ip = config.get('conf', 'ml_IP').strip()
    ml_port = config.get('conf', 'ml_PORT').strip()
    ml_user = config.get('conf', 'ml_USER').strip()
    ml_pass = config.get('conf', 'ml_PASS').strip()

    try :
        donkey = MLDonkey(ml_ip,ml_port, ml_user, ml_pass)
        donkey.clean_searches()
    except:
        print "Connection error with ip:%s port:%s !!!" % (ml_ip, ml_port)
        print "Unexpected error:", sys.exc_info()[0]

    else:
        new_searchwords = ['cachurulo', 'lerele']
        donkey.run_search(new_searchwords)
        searches = donkey.get_searches()
        for search in searches:
            print search
            res = donkey.download_search(int(search[0]))
            if not res:
                print "\t\"",search[1],"\" downloaded"
            else:
                print "Empty search ",search[1]," ",res

        donkey.clean_searches()

    return

if __name__ == '__main__':
    main()
