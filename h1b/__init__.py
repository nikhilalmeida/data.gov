__author__ = 'nikhilalmeida'
import json
import csv
with open('/Users/nikhilalmeida/Downloads/EFILE_FY2007.txt') as readFile:
    reader = csv.reader(readFile, delimiter = ",")
    title = reader.next()
    print title
    print title[3], title[6], title[7], title[8]
    count = 0
    for line in reader:
        count +=1
        print line
        if count == 10:
            break