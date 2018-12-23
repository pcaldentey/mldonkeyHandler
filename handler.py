#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from mldonkey import MLDonkey
from ConfigParser import ConfigParser


def main():
    actual_dir = os.path.dirname(__file__)
    configfile = actual_dir + '/donkeylinkscrawler.ini'

    # Get configuration
    config = ConfigParser()
    config.read([configfile])

    ml_ip = config.get('conf', 'ml_IP').strip()
    ml_port = config.get('conf', 'ml_PORT').strip()
    ml_user = config.get('conf', 'ml_USER').strip()
    ml_pass = config.get('conf', 'ml_PASS').strip()

    try:
        donkey = MLDonkey(ml_ip, ml_port, ml_user, ml_pass)
        # donkey.clean_searches()
    except Exception as e:
        print("Connection error with ip:{} port:{} !!!".format(ml_ip, ml_port))
        print("Unexpected error: {}".format(sys.exc_info()[0]))
    else:
        new_searchwords = ['cachurulo', 'lerele']
        donkey.run_search(new_searchwords)
        searches = donkey.get_searches()
        for search in searches:
            print(search)
            res = donkey.download_search(int(search[0]))
            if not res:
                print("\t\"{}\" downloaded".format(search[1]))
            else:
                print("Empty search {} {}".format(search[1], res))

        donkey.clean_searches()

    return


if __name__ == '__main__':
    main()
