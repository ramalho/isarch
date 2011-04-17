#!/usr/bin/env python

SUBJ = 'CDS-ISIS LOG'
SRC_PATH = '../data/isisarch.mbox'
DEST_DIR = '../data/logs/'

import logging
logging.basicConfig(filename='subjects.log',level=logging.DEBUG)

import mailbox
from email.generator import Generator
import os
import re

regex = re.compile(r'CDS-ISIS LOG(\d\d\d\d)')

for msg in mailbox.mbox(SRC_PATH):
    subject = msg.get('subject', '[NO_SUBJECT]').strip()
    match = regex.search(subject)
    if match:
        lognum = match.group(1)
        copy_num = 0
        while True:
            copy = '-'+str(copy_num) if copy_num else ''
            try_name = '{0}{1}{2}.email'.format(DEST_DIR, lognum, copy)
            print '.' * copy_num, try_name
            if not os.path.exists(try_name):
                dest_name = try_name
                break
            copy_num += 1
        print dest_name
        dest = open(dest_name, 'w')
        Generator(dest).flatten(msg)
        dest.close()
    else:
        logging.debug(subject)

