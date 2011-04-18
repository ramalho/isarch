#!/usr/bin/env python

DEST_DIR = '../data/logs/'

import os
import glob
from datetime import datetime
import logging

logging.basicConfig(filename='month_stats.log',level=logging.DEBUG)

'''
Date:         Mon, 22 Jun 92 20:37:48 -0400
Date:         Wed, 22 Jul 92 06:28:49 GMT
              Tue, 13 Apr 1993 22:40:00 +0000
'''

NO_MATCH_MSG = 'does not match format'
REMAINS_MSG = 'unconverted data remains:'

def parse_date(s):
    try:
        try:
            dt = datetime.strptime(s, '%a, %d %b %y %H:%M:%S')
        except ValueError as err:
            msg = str(err)
            if NO_MATCH_MSG in msg:
                dt = datetime.strptime(s, '%a, %d %b %Y %H:%M:%S')
            else:
                raise
    except ValueError as err:
        if msg.startswith(REMAINS_MSG):
            remainder = msg.replace(REMAINS_MSG,'').strip()
            s = s.replace(remainder, '').strip()
            try:
                dt = datetime.strptime(s, '%a, %d %b %y %H:%M:%S')
            except ValueError as err:
                msg = str(err)
                if NO_MATCH_MSG in msg:
                    dt = datetime.strptime(s, '%a, %d %b %Y %H:%M:%S')
                else:
                    raise
        else:
            raise
    return dt

for filename in sorted(glob.glob(DEST_DIR+'????-??.email')):
    ym_file = os.path.split(filename)[1][:7]
    with open(filename) as file:
        print '*'*40, filename
        for lin in file:
            if lin.startswith('Date:'):
                if 'Apr 2011' in lin: continue
                ds = lin[len('Date:'):].strip()
                try:
                    dt = parse_date(ds)
                except ValueError as err:
                    logging.debug(err)
                else:
                    ym = dt.strftime('%Y-%m')
                    flag = '=' if ym_file == ym else '!'
                    print ym_file, flag, ds


