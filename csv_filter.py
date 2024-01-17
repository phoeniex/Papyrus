import csv
import sys
import os
import re

def to_snake_case(string):
    string = re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', string).strip().replace(' ', '_')
    return ''.join(string.lower())

localized_path = sys.argv[1]
output_info_path = sys.argv[2] + os.sep
output_localized_path = sys.argv[2] + os.sep + 'FilteredCSV' + os.sep
silent = sys.argv[3].lower() == 'on'
dry_run = sys.argv[4].lower() == 'on'
no_prefix = sys.argv[5].lower() == 'on'

# table configure
languages = {'Thai': 'th', "English": 'en-US'}
ignored_elements = ['Text Input']
ignored_statuses = ['Obsolete', 'Missing Info']

template_sheet_name = '00 - Template Word'
template_title = 'Template'

element_sheet_name = '00 - Element'
element_key_title = 'UI Element'
element_value_title = 'Key'

status_title = 'Status'
screen_title = 'Screen'
element_title = 'Element'
description_title = 'Description'

if silent:
   sys.stdout = open(os.devnull, 'w')

if not os.path.exists(output_localized_path):
    os.makedirs(output_localized_path)

elements = {}
# element key from sheet
with open(os.path.join(localized_path, element_sheet_name + '.csv')) as csvfile:
    key_index = 0
    value_index = 0

    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = next(reader)

    # find column of key and value in each sheet
    for csv_key in header:
        if csv_key == element_key_title:
            key_index = header.index(csv_key)
        elif csv_key == element_value_title:
            value_index = header.index(csv_key)

    for row in reader:
        key = row[key_index]
        if key != '':
            elements[key] = row[value_index]

with open(output_info_path + 'element.info', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, ['key', 'value'])
    writer.writeheader()

    for key, value in elements.items():
        row = {}
        row['key'] = key
        row['value'] = value
        writer.writerow(row)

# localized key from sheet
localized_file_names = [file_name for file_name in os.listdir(localized_path) if (os.path.isfile(os.path.join(localized_path, file_name)) and not file_name.startswith("00"))]
localized_file_names.append(template_sheet_name + '.csv')
for file_name in localized_file_names:
    localized_values = {}
    localized_headers = {}
    screen_index = 0
    element_index = 0
    description_index = 0
    template_index = 0
    status_index = 0

    is_template_file = template_sheet_name in file_name
    output_path = output_info_path + 'template.info' if is_template_file else output_localized_path + file_name
    with open(localized_path + file_name) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)

        # find column of key and value in each sheet
        for csv_key in header:
            if csv_key in languages:
                # Get language denotation from header title e.g. 'TH/en-US' got 'en-US', 'TH/th' got 'th'
                value_key = 'value_{0}'.format(languages[csv_key])
                localized_headers[value_key] = header.index(csv_key)
            elif csv_key == screen_title:
                screen_index = header.index(csv_key)
            elif csv_key == element_title:
                element_index = header.index(csv_key)
            elif csv_key == description_title:
                description_index = header.index(csv_key)
            elif csv_key == template_title:
                template_index = header.index(csv_key)
            elif csv_key == status_title:
                status_index = header.index(csv_key)
        
        # Skip blank key
        if len(localized_headers) == 0:
            continue

        for row in reader:
            # skip empty row
            if len(row[0]) == 0:
                continue

            localized_key = ''
            if is_template_file:
                localized_key = row[template_index]
            
            # check and ignore some statuses and elements
            elif (row[element_index] not in ignored_elements) and (row[status_index] not in ignored_statuses):  
                module = to_snake_case(file_name.split(' - ')[-1].replace('.csv', ''))
                screen = to_snake_case(row[screen_index])
                element = to_snake_case(elements[row[element_index]])
                description = to_snake_case(row[description_index])
                localized_key = '_'.join(list(filter(None, [module, screen, element, description])))

            # skip empty key
            if len(localized_key) == 0:
                continue
                
            localized_object = {}
            for (value_key, value_index) in sorted(localized_headers.items()):
                value = row[value_index]
                localized_object[value_key] = value

            # if at lease one value
            if len(localized_object) > 0:
                localized_values[localized_key] = localized_object

    if len(localized_values) == 0:
        continue

    with open(output_path, 'w') as csvfile:
        values_and_key = ['key']
        values_and_key.extend(localized_headers.keys())

        writer = csv.DictWriter(csvfile, values_and_key)
        writer.writeheader()

        for key, value in localized_values.items():
            value['key'] = key
            writer.writerow(value)

    with open(output_info_path + 'lang.info', 'w') as info_file:
        info_file.write(','.join(localized_headers.keys()))

