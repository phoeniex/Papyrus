import sys
import appscript
import datetime
import os
import csv

from appscript import k

numbers_path = sys.argv[1]
import_csv_path = sys.argv[2] + os.sep
import_spreadsheet = sys.argv[3].split('/')[-1]
business_unit = sys.argv[4].upper()
jira_ticket = sys.argv[5]
column_key_indexes = list(map(int, sys.argv[6].split(',')))
silent = sys.argv[7] == 'on'
dry_run = sys.argv[8] == 'on'

if silent:
   sys.stdout=open(os.devnull, 'w')

update_color = (3476, 27123, 25436)
default_color = (0, 0, 0)

column_key = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Open Numbers file
appscript.app('Numbers').open(numbers_path)

document = appscript.app('Numbers').documents.first()

files = [file for file in os.listdir(import_csv_path) if os.path.isfile(os.path.join(import_csv_path, file))]

 # clear text color
if not dry_run:
    for sheet in document.sheets()[1:]:
        table = sheet.tables()[0]
        cells = table.cells[(appscript.its.column.address > 4).AND(appscript.its.column.address <= len(table.columns())).AND(appscript.its.row.address > 1)].text_color.set(default_color)

# Get data from import csv
for file in files:
    localizes = []
    csv_langs = {}
    numbers_langs = {}
    
    with open(import_csv_path + file) as csvfile:
         # Example of file name '01 - Table Name-Foo', Use 2nd index when split by '-'
        number, sheet_name, _ = file.split('-')
        sheet_name = number + '-' + sheet_name
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Get header
        headers = next(reader)
        for header in headers:
            # Check if this field is translated field, get language code behide dash '-'
            if '-' in header:
                lang_name = header.split('-')[-1].strip()
                lang_index = headers.index(header)
                csv_langs[lang_name] = lang_index

        # Travel through value, key in CSV to import localize dict
        for row in reader:
            key = row[0]
            localize = {'key': key}

            for (lang_name, lang_index) in csv_langs.items():
                value = row[lang_index]
                if len(value) == 0:
                    #print('Warning: Found empty translated on "' + key + '" for ' + lang_name.upper())
                    continue

                localize[lang_name] = row[lang_index]

            # only key, no need to add
            if len(localize) > 1:
                localizes.append(localize)

        # if no localize in this file skip applying 
        if len(localizes) == 0:
            continue

        # Update Files
        try:
            print('sheet ' + sheet_name)
            data_table = document.sheets[sheet_name].tables.first()
        
            # Match business unit with column
            for column in data_table.columns():
                header = data_table.cells[column_key[column.address()] + '1'].value()

                # Focus on translated column only
                if '-' not in header:
                    continue

                header_business_unit, header_language = header.split('-')
                if header_business_unit == business_unit:
                    for (lang_name, lang_index) in csv_langs.items():
                        numbers_langs[lang_name] = column.address()

            # Travel through value, key in numbers to apply imported dict
            for row in data_table.rows():
                row_name = str(row.address())

                # If key that match with import key
                found_localize = {}
                for localize in localizes:
                    for column_key_index in column_key_indexes:
                        key = data_table.cells[column_key[column_key_index] + row_name].value()
                        if localize['key'] == data_table.cells[column_key[column_key_index] + row_name].value():
                            found_localize = localize
                            for (lang_name, lang_index) in numbers_langs.items():
                                print('> apply translation for key "' + data_table.cells[column_key[column_key_index] + row_name].value() + '"')
                                if not dry_run:
                                    cell = data_table.cells[column_key[lang_index] + row_name]
                                    cell.value.set(localize[lang_name])
                                    cell.text_color.set(update_color)
            
                # Also remove found localize to avoid duplicate run loop
                if len(found_localize) > 0:
                    localizes.remove(found_localize)

        except appscript.CommandError:
            print('ERROR: sheet "' + sheet_name + '" does not exist.')

# Check if log row avaliable, if no create new row
log_table = document.sheets()[0].tables()[0]
if log_table.cells[column_key[1] + str(log_table.rows()[-1].address())].value() != k.missing_value:
    log_table.rows()[-1].add_row_below()

# Add log
for row in log_table.rows()[2:]:
    row_name = str(row.address())

    # Clear color
    start_cell_index = (len(log_table.column()) * 2) + 1
    log_table.cells[start_cell_index : -1].text_color.set(default_color)

    # Find next avaliable row
    if log_table.cells[column_key[1] + row_name].value() == k.missing_value:
        print('update log')
        log_table.cells[column_key[1] + row_name : column_key[4] + row_name].text_color.set(update_color)
        log_table.cells[column_key[1] + row_name].value.set(datetime.datetime.now())
        log_table.cells[column_key[2] + row_name].value.set(os.getlogin().title())
        log_table.cells[column_key[3] + row_name].value.set('Imported from "' + import_spreadsheet + '" to ' + business_unit)
        log_table.cells[column_key[4] + row_name].value.set(jira_ticket)
        break



