#!/usr/bin/env python3

import csv
from datetime import datetime, timedelta
import time
import argparse
from urllib.parse import urlparse, parse_qs
import sys

def delta_to_minutes(td):
    return td.days*1440 + td.seconds//60

def delta_to_hours(td):
    return td.days*24 + td.seconds/1440

def delta_to_hours_minutes(td):
    return td.days*24 + td.seconds//3600, (td.seconds//60)%60

def main() -> None:
    if len(sys.argv) < 2:
        csvfile = 'zero.csv'
    else:
        csvfile = sys.argv[1]

    with open(csvfile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            FMT = '%H:%M'
            if row['End'] is not None:
                tdelta = timedelta(days=1) + datetime.strptime(row['End'], FMT) - datetime.strptime(row['Start'], FMT)
                k = datetime.strptime(row['Date']+' '+row['Start'], '%m/%d/%y %H:%M')
                print(f'{k.strftime("%Y-%m-%d %I:%M:%S%p")} r \'zero\'')
                d = delta_to_hours_minutes(tdelta)
                print(f'  acti.fasting.time {d[0]:02}:{d[1]:02}')


if __name__ == '__main__':
    main()
