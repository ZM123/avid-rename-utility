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

# Modify a word given a search regex and sub regex
def modify_word(word, search_value, sub_value):
    if sub_value == 'UP':
        return re.sub(rf'{search_value}', lambda m: m.group().upper(), word)
    if sub_value == 'LO':
        return re.sub(rf'{search_value}', lambda m: m.group().lower(), word)
    return re.sub(rf'{search_value}', rf'{sub_regex}', word)

# Update the shot names in the data list given the search regex and sub regex
def update_shot_names(row_list, search_value, sub_value):
    name_index = -1
    data_index = -1
    for index, row in enumerate(row_list):
        if len(row) == 1 and row[0] == 'Column':
            columns = row_list[index + 1]
            try:
                name_index = columns.index('Name')
            except ValueError:
                print('Name column not found')
                return False
        if len(row) == 1 and row[0] == 'Data':
            data_index = index + 1

    if name_index == -1 or data_index == -1:
        return

    for row in row_list[data_index:]:
        row[name_index] = modify_word(row[name_index], search_value, sub_value)

# Write the data into an ALE file with the specified filename
def write_ale(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)

################################################################################
input_filename = sys.argv[1]

row_list = read_ale(input_filename)

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

should_commit = False
search_regex = ''
sub_regex = ''
# Search input loop
while should_commit is False:
    search_regex = input('Enter search regex:')

    # Add surrounding capture group if none specified
    if re.compile(search_regex).groups < 1:
        search_regex = f'({search_regex})'

    print('Found matches:')
    for name in shot_names:
        print(re.sub(rf'({search_regex})', r'\033[2;31;43m\1\033[0;0m', name))

    # Sub input loop
    while should_commit is False:
        sub_regex = input('Enter substitution regex, UP for uppercase, LO for lowercase, RE to restart:')

        if sub_regex == 'RE':
            break

        print('Substitution preview:')
        for name in shot_names:
            if sub_regex == 'UP':
                print(re.sub(rf'{search_regex}', lambda m: '\033[2;36;42m{}\033[0;0m'.format(m.group().upper()), name))
            elif sub_regex == 'LO':
                print(re.sub(rf'{search_regex}', lambda m: '\033[2;36;42m{}\033[0;0m'.format(m.group().lower()), name))
            else:
                print(re.sub(rf'{search_regex}', rf'\033[2;36;42m{sub_regex}\033[0;0m', name))

        commit_input = input('Do you want to commit this? Y/N:')
        if commit_input == 'Y' or commit_input == 'y':
            should_commit = True
        else:
            restart_point = input('Type SE to change search value, SU to change sub value:')
            if restart_point == 'SU':
                continue
            else:
                break

update_shot_names(row_list, search_regex, sub_regex)

print('Writing to file...')
output_filename = input_filename
if len(sys.argv) > 2:
    output_filename = sys.argv[2]
write_ale(row_list, output_filename)
