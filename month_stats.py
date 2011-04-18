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

def parse_date_format(s, format):
    try:
        dt = datetime.strptime(s, format)
    except ValueError as err:
        msg = str(err)
        if msg.startswith(REMAINS_MSG):
            remainder = msg.replace(REMAINS_MSG,'').strip()
            s = s.replace(remainder, '').strip()
            dt = datetime.strptime(s, format)
        else:
            raise
    return dt

def parse_date(s):
    formats = [ '%a, %d %b %y %H:%M:%S', # Mon, 22 Jun 92 20:37:48 -0400
                '%a, %b %d, %Y at %I:%M %p', # Wed, May 12, 2010 at 9:55 AM
                '%a, %d %b %y %H:%M', # Thu, 2 Sep 93  14:59 GMT
                '%a %b %d, %Y %H:%M%p', #Sun Jul 3, 2005 0:59pm
                '%a, %d %b %Y %H:%M:%S', # Tue, 13 Apr 1993 22:40:00 +0000
                                         # Mon, 11 Jul 1994 07:29:00 +0000
                '%a %d %b %Y %H:%M:%S', # Mon  1 Nov 2010 20:55:22 -0700
                '%a, %d %b %Y', #Wed, 3 Sep 2003
                '%a, %d %b %Y %H:%M', # Tue, 31 Jan 1995 09:15 +0530 (GMT +0530)
                '%a, %B %d, %Y %H:%M', # Thu, October 28, 2010 14:16
                '%d %B %y, %H:%M:%S', # 16 September 92, 12:55:59 ITA
                '%d. %B %Y %H:%M', # 8. september 1999 12:18
                '%d %B %Y', # 12 October 2000
                '%d %b %y %H:%M:%S', # 24 Jan 95 10:02:57
                '%d %b %Y %H:%M', # 01 Jun 1993 11:44 +1000
                '%d %b %Y, %H:%M', # 07 OCT 1994, 12:19 CET
                '%Y-%m-%d %H:%M:%S', # 1995-02-28 09:46:14
                '%Y/%m/%d', # 2010/3/15
                '%Y%m%d', # 20010511
                '%A, %B %d, %Y %I:%M%p', # Tuesday, April 25, 1995 9:08AM
                '%A, %d %B, %Y, %H:%M', # Thursday, 28 October, 2010, 8:34
                '%A, %B %d, %Y %I:%M %p', # Monday, December 08, 1997 10:54 PM
                '%A, %B %d, %Y, %I:%M %p', # Thursday, October 28, 2010, 10:19 AM
                '%A, %B %d, %Y %H:%M:%S', # Friday, September  1, 1995  9:12:00 CET
                '%A %d %B %Y %H.%M', # Friday 19 November 1999 12.46
                '%A, %d. %B %Y %H:%S', # Wednesday, 8. January 1997 09:40
                '%A %d %b, %Y %H', # Wednesday 13 May, 1998 05:09
                '%A, %d-%b-%y %I:%M %p', # Tuesday, 16-Sep-97 04:43 PM
                '%m/%d/%y %I:%M %p', # 10/17/95 3:41 PM
                '%m/%d/%y %H:%M:%S', # 06/22/04 18:26:25=3D0D
                '%m/%d/%y %I:%M%p', # 6/14/96 9:31PM
                '%d/%m/%y %I:%M', #14/06/96 9:31 a
                '%d/%m/%Y %H:%M', #01/06/1999 06:16 ^YS
                '%d.%m.%Y %H:%M:%S', # 12.12.2003 11:41:21=3D0D
              ]
    for i, format in enumerate(formats):
        try:
            dt = parse_date_format(s, format)
        except ValueError as err:
            #logging.debug('TRIED: '+repr(err))
            if i == len(formats) - 1:
                msg = '"{0}" does not match any of the {1} expected date formats'
                raise ValueError(msg.format(s, len(formats)))
        else:
            #logging.debug('SOLVED: '+repr(dt))
            return dt

DATE_IGNORE_LIST = ['1/1/4', 'Signature:', '---', '5 =F4=E5=E2=',
    '15 =EE=EA=', 'maandag 22',
    'Jeudi 14', 'Wed =3D', 'S=3D',
    'Jueves 7', '5. j=FAl 2000', '6. j=FAl',
    '13 Januari', '21 Desember', '19. j?l 1999',
    '=3D20', 'M=3D', '=3D',
    'Tue, 26 Jun 0103 07:14:06 +0000',
    'Wed, 10 Nov 0100 13:59:46 +0100',
    'Wed, 23 Jun 0100 04:19:24 PDT',
    '15 =EC=E0=F0=F2=E0 1999',
    # probably not date headers:
    '29-31 October 2007', 'October 13th - 16th',
    'November 5 to 9, 2007', 'November 26 to 30, 2007',
    '11 - 12 April 2007', 'May 3 to 5, 2005', '6th-8th November 2000',
    '&nbsp;', '"v934})',
    ]

# 'Viernes', 'Lunes', 'quinta-feira', 'Mercredi',

m_stats = {}

for filename in sorted(glob.glob(DEST_DIR+'????-??.email')):
    ym_file = os.path.split(filename)[1][:7]
    with open(filename) as file:
        print '*'*40, filename
        for lin in file:
            if lin.startswith('Date:'):
                if '<' in lin or 'Apr 2011' in lin: continue
                m_stats[ym_file] = m_stats.get(ym_file, 0) + 1
                ds = lin[len('Date:'):]
                ds = ds.replace('=3D2C', ' ') # what is this gremlin?
                ds = ds.replace('=C2=A0 =C2=A0 =C2=A0 =C2=A0', ' ')
                ds = ds.replace('marec', 'March')
                ds = ds.replace('maart', 'March')
                ds = ds.replace('apr=EDl', 'April')
                ds = ds.replace('m=E1j', 'May')
                ds = ds.replace('j=FAn', 'June')
                ds = ds.replace('maandag', '')
                ds = ds.replace('donderdag', '')
                ds = ds.replace('Viernes', '')
                ds = ds.replace('Mercredi', '')
                ds = ds.replace('Lunes', '')
                ds = ds.replace('Mardi', '')
                ds = ds.replace('Lundi', '')
                ds = ds.replace('Jeudi', '')
                ds = ds.replace('Jueves', '')
                ds = ds.replace('quinta-feira,', '')
                ds = ds.replace(' de ', ' ')
                ds = ds.replace('janu_r', 'January')
                ds = ds.replace('Janvier', 'January')
                ds = ds.replace('Januari', 'January')
                ds = ds.replace('febru_r', 'February')
                ds = ds.replace('februari', 'February')
                ds = ds.replace('Julio', 'July')
                ds = ds.replace('Juin', 'June')
                ds = ds.replace('julho', 'July')
                ds = ds.replace('Agosto', 'August')
                ds = ds.replace('Mars', 'March')
                ds = ds.replace('Octobre', 'October')
                ds = ds.replace('okt=F3ber', 'October')
                ds = ds.replace('Septembre', 'September')
                ds = ds.replace('D=3DC3=3DA9cembre', 'December')
                ds = ds.replace('Desember', 'December')
                ds = ds.replace('Diciembre', 'December')
                while '&nbsp;' in ds:
                    ds = ds.replace('&nbsp;',' ')
                ds = ds.strip()
                if ds == '' or ds == 'Mon, 11' or any(ds.startswith(garbage)
                                   for garbage
                                   in DATE_IGNORE_LIST):
                    logging.debug('UNABLE TO PARSE: '+lin.strip())
                    continue
                dt = parse_date(ds)
                assert dt.year > 1900, lin
                ym = dt.strftime('%Y-%m')
                flag = '=' if ym_file == ym else '!'
                #print ym_file, flag, ds

for ym in sorted(m_stats):
    print '{0}\t{1}'.format(ym, m_stats[ym])
