#!/usr/bin/env python3
import csv

from datetime import datetime


data = csv.reader(open('Observations.csv', 'r'))
data = sorted(data, key = lambda row: datetime.strptime(row[1], "%d-%m-%Y"))

for line in data:
    new_date = datetime.strptime(line[1], "%d-%m-%Y")
    new_date = new_date.strftime('%d/%m/%Y')
    line[1] = new_date

file = open("result.csv", "w+")
for line in data:
    file.write(','.join(line))
    file.write('\n')
