import openpyxl
import csv
import sys
import os

excel_path = sys.argv[1]
csv_path = sys.argv[2] + os.sep

# create csv dir
if not os.path.exists(csv_path):
    os.makedirs(csv_path)

workbook = openpyxl.load_workbook(excel_path)
for sheet in workbook.worksheets:
    filename = sheet.title + '-Table 1.csv'
    with open(csv_path + filename, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in sheet.rows:
            writer.writerow([cell.value for cell in row])