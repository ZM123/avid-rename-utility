import re
import sys
import csv

# Parses the tab delimited ALE file into a list of lists
def read_ale(filename):
    return list(csv.reader(open(name, 'r'), delimiter='\t'))

# Retrieves the list containing the column names from an ALE as a list of lists
def get_columns(row_list):
    for index, row in enumerate(row_list):
        if len(row) == 1 and row[0] == 'Column' and index < len(row_list) - 1:
            return row_list[index + 1]

# Retrieves the data as a list of lists from an ALE as a list of lists
def get_data(row_list):
    for index, row in enumerate(row_list):
        if len(row) == 1 and row[0] == 'Data':
            if index == len(row_list) - 1:
                print('No data found')
                return []

            return row_list[index + 1:]

################################################################################
name = sys.argv[1]

row_list = read_ale(name)

columns = get_columns(row_list)

data = get_data(row_list)

# name_index = -1
#
# for index, heading in enumerate(column_headings):
#     if heading == 'Name':
#         name_index = index
#
# if name_index == -1:
#     print('No Name column found')
#     sys.exit(1)
