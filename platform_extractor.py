import subprocess
import sys
import os
import csv

def extract_string(string, platform):
    if string[:6].upper == '<CODE>':
        return string[6:]

    extracted_string = string
    if platform == 'ios':
        extracted_string = string.replace('%s', '%@')
    elif platform == 'android':
        extracted_string = string.replace('&', '&amp;')
        extracted_string = extracted_string.replace("'", "\\'")
        extracted_string = extracted_string.replace('"', '\\"')
    
    return extracted_string

input_path = sys.argv[1]
output_path = sys.argv[2]
platform = sys.argv[3]

localizes = []
values = {}
header = []
with open(input_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(reader)

    for csv_key in header:
        if 'value_' in csv_key:
            values[csv_key] = header.index(csv_key)

    for row in reader:
        localize = row
        for (value_key, value_index) in sorted(values.items()):
            value = row[value_index]
            localize[value_index] = extract_string(row[value_index], platform)
        localizes.append(localize)

with open(output_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(localizes)
        


