import re
import sys
import csv

name = sys.argv[1]

list_of_rows = list(csv.reader(open(name, 'r'), delimiter='\t'))

# print(list_of_rows)

column_headings = []

for index, row in enumerate(list_of_rows):
   if len(row) == 1 and row[0] == 'Column':
       column_headings = list_of_rows[index + 1]

name_index = -1

for index, heading in enumerate(column_headings):
    if heading == 'Name':
        name_index = index

if name_index == -1:
    print('No Name column found')
    sys.exit(1)

data_rows = []

for index, row in enumerate(list_of_rows):
    if len(row) == 1 and row[0] == 'Data':
        if index == len(list_of_rows) - 1:
            print('No data found')
            sys.exit(1)

        data_rows = list_of_rows[index + 1:]

# print(data_rows)
