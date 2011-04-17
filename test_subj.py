
import re

regex = re.compile('CDS-ISIS LOG(\d\d\d\d)')


for subject in open('subjects.txt'):
    subject = subject.strip()
    match = regex.search(subject)
    if match:
        print ' '*40, match.group(1), subject
    else:
        print subject
