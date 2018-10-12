import subprocess
import sys
import os
import csv

def call_localizer():
    command = './csv-localizer -p ' + platform_string + ' -i ' + csv_path + ' -o ' + output_path
    subprocess.call(command, shell=True)

csv_original_path = sys.argv[1] + os.sep + 'merged_extracted.csv'
csv_path = sys.argv[1] + os.sep + 'merged_removed.csv'
info_path = sys.argv[1] + os.sep + 'lang.info'
output_path = sys.argv[2]
platform = sys.argv[3].lower()
platform_string = 'ios' if platform == 'ios' else 'android'

os.makedirs(output_path, exist_ok=True)

lang_list = []
with open(info_path) as info_file:
    lang_list = info_file.readline().split(',')

# Remove 'key' (header of each file) from merged csv file
localized = []
with open(csv_original_path) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(reader)

    for row in reader:
        if row[0] != 'key' and row not in localized:
            localized.append(row)

with open(csv_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(localized)

call_localizer()