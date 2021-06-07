#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import os
from mldonkey import MLDonkey, MLDonkeyException, MLDonkeyError


def main():
    actual_dir = os.path.dirname(__file__)
    configfile = actual_dir + '/donkeylinkscrawler.ini'

    # Get configuration
    config = configparser.ConfigParser()
    config.read([configfile])

    ml_ip = config.get('conf', 'ml_IP').strip()
    ml_port = config.get('conf', 'ml_PORT').strip()
    ml_user = config.get('conf', 'ml_USER').strip()
    ml_pass = config.get('conf', 'ml_PASS').strip()
    try:
        with MLDonkey(ml_ip, ml_port, ml_user, ml_pass) as donkey:
            donkey.clean_searches()
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

    except MLDonkeyException as e:
        print(e)

    except MLDonkeyError as e:
        print(e)


if __name__ == '__main__':
    main()
