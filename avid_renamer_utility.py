import re
import sys
import csv

# Parses the tab delimited ALE file into a list of lists
def read_ale(filename):
    return list(csv.reader(open(filename, 'r'), delimiter='\t'))

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
filename = sys.argv[1]

row_list = read_ale(filename)

columns = get_columns(row_list)

data = get_data(row_list)

if len(columns) == 0 or len(data) == 0:
    sys.exit(1)

shot_names = get_shot_names(columns, data)

if len(shot_names) == 0:
    print('No shot names found')
    sys.exit(1)

print('Found shot names:')
for name in shot_names:
    print(name)

search_regex = input('Enter search regex:')

# Add surrounding capture group if none specified
if re.compile(search_regex).groups < 1:
    search_regex = f'({search_regex})'

print('Found matches:')
for name in shot_names:
    print(re.sub(rf'({search_regex})', r'\033[2;31;43m\1\033[0;0m', name))

sub_regex = input('Enter substitution regex, UP for uppercase, LO for lowercase:')

to_lower = False
to_upper = False
if sub_regex == 'UP':
    to_upper = True
if sub_regex == 'LO':
    to_lower = True

print('Substitution preview:')
for name in shot_names:
    if to_upper:
        print(re.sub(rf'{search_regex}', lambda m: '\033[2;36;42m{}\033[0;0m'.format(m.group().upper()), name))
    elif to_lower:
        print(re.sub(rf'{search_regex}', lambda m: '\033[2;36;42m{}\033[0;0m'.format(m.group().lower()), name))
    else:
        print(re.sub(rf'{search_regex}', rf'{sub_regex}', name))
