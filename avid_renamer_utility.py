import re
import sys
import csv

# Parses the tab delimited ALE file into a list of lists
def read_ale(filename):
    return list(csv.reader(open(name, 'r'), delimiter='\t'))

# Retrieves the list containing the column names from an ALE as a list of lists
def get_columns(row_list):
    for index, row in enumerate(row_list):
        if len(row) == 1 and row[0] == 'Column':
            return row_list[index + 1]

# Retrieves the data as a list of lists from an ALE as a list of lists
def get_data(row_list):
    for index, row in enumerate(row_list):
        if len(row) == 1 and row[0] == 'Data':
            if index == len(row_list) - 1:
                print('No data found')
                return []

            return row_list[index + 1:]

# Get the list of shot names given the data columns and data list
def get_shot_names(columns_list, data_list):
    name_index = -1

    for index, heading in enumerate(columns_list):
        if heading == 'Name':
            name_index = index

    if name_index == -1:
        print('No Name column found')
        return []

    return [x[name_index] for x in data_list]

################################################################################
name = sys.argv[1]

row_list = read_ale(name)

columns = get_columns(row_list)

data = get_data(row_list)

if len(columns) == 0 or len(data) == 0:
    sys.exit(1)

shot_names = get_shot_names(columns, data)
