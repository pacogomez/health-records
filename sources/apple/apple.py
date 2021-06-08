#!/usr/bin/env python3
import csv
from dateutil import parser as dateutil_parser
import sys
from datetime import datetime
import pytz

if len(sys.argv) < 2:
    csvfile = 'BodyMass.csv'
else:
    csvfile = sys.argv[1]

if len(sys.argv) < 3:
    before = pytz.utc.localize(datetime.now())
else:
    before = pytz.utc.localize(dateutil_parser.parse(sys.argv[2]))

metrics = {
    'BodyMass': 'body.weight',
}

data = dict()

with open(csvfile) as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[dateutil_parser.parse(row['startDate'])] = \
            {'source': row['sourceName'],
             'type': row['type'],
             'value': round(float(row['value'])*2.2046, 2)}

for k in sorted(data.keys()):
    if k < before:
        print(f'{k.strftime("%Y-%m-%d %I:%M:%S%p")} r \'{data[k]["source"]}\'')
        print(f'  {metrics[data[k]["type"]]} {data[k]["value"]}')
