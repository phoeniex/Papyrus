import subprocess
import sys
import os
import csv

def extract_string(string, platform):
    # ignore code "<CODE>" syntax
    if string[:6].upper == '<CODE>':
        return string[6:]

    extracted_string = string
    if platform == 'ios':
        extracted_string = string.replace('%s', '%@')
        extracted_string = extracted_string.replace('$s', '$@')
        extracted_string = extracted_string.replace('"', '\\"')
    elif platform == 'android':
        extracted_string = string.replace('&', '&amp;')
        extracted_string = extracted_string.replace("'", "\\'")
        extracted_string = extracted_string.replace('"', '\\"')
    
    return extracted_string

def check_platform_localized(language, platform):
    return True

def convert_csv_to_dict(csv_path):
    values = {}
    header = []
    localizes = []

    if not os.path.exists(csv_path):
        return[], []
        
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)

        for csv_key in header:
            if 'value_' in csv_key and check_platform_localized(csv_key, platform):
                values[csv_key] = header.index(csv_key)

        for row in reader:
            localize = row
            for (_, value_index) in sorted(values.items()):
                localize[value_index] = extract_string(row[value_index], platform)
            localizes.append(localize)
    return header, localizes

def apply_template_key(header, templates, localizes): 
    valueIndices = []
    keyIndex = 0
    appliedLocalizes = []

    for csv_key in header:
        if 'value_' in csv_key:
            valueIndices.append(header.index(csv_key))
        elif 'key' in csv_key:
            keyIndex = header.index(csv_key)

    for localize in localizes:
        appliedLocalize = localize

        for valueIndex in valueIndices:
            for template in templates:
                # if some of value in localize match with template key
                if appliedLocalize[valueIndex] == template[keyIndex]:
                    print('Replace Template ', appliedLocalize[keyIndex], ' with ', template[valueIndex])
                    appliedLocalize[valueIndex] = template[valueIndex]
        
        appliedLocalizes.append(appliedLocalize)
    return appliedLocalizes

input_path = sys.argv[1]
template_info_path = sys.argv[2]
output_path = sys.argv[3]
platform = sys.argv[4]
silent = sys.argv[5].lower() == 'on'
dry_run = sys.argv[6].lower() == 'on'

if silent:
   sys.stdout = open(os.devnull, 'w')

header, localizes = convert_csv_to_dict(input_path)
_, templates = convert_csv_to_dict(template_info_path)

localizes = apply_template_key(header, templates, localizes)

with open(output_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(localizes)
        


