#!/usr/bin/env python

DEST_DIR = '../data/logs/'

import os
import glob

for file in sorted(glob.glob(DEST_DIR+'*.email')):
     path, name = os.path.split(file)
     new_name = '19'+name if name.startswith('9') else '20'+name
     new_name = new_name[:4] + '-' + new_name[4:]
     print name, file.replace(name, new_name)
     os.rename(file, file.replace(name, new_name))

