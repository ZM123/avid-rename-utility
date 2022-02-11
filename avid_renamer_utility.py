import re
import sys
import csv

# Parses the tab delimited ALE file into a list of lists
def read_ale(filename):
    return list(csv.reader(open(filename, 'r'), delimiter='\t'))

# Retrieves the data from a parsed ALE as a list of dictionaries
def get_data_dicts(row_list):
    dicts = []

    columns_index = row_list.index(['Column'])
    columns = row_list[columns_index + 1]

    # Exit if Name column not included
    if len(columns) == 0 or 'Name' not in columns:
        return dicts

    data_index = row_list.index(['Data'])
    data_rows = row_list[data_index + 1:]

    for item in data_rows:
        if len(item) != len(columns):
            continue
        new_dict = dict(zip(columns, item))
        dicts.append(new_dict)

    return dicts

# Modify a word given a search regex and sub regex
def modify_word(word, search_value, sub_value):
    if sub_value == 'UP':
        return re.sub(rf'{search_value}', lambda m: m.group().upper(), word)
    if sub_value == 'LO':
        return re.sub(rf'{search_value}', lambda m: m.group().lower(), word)
    return re.sub(rf'{search_value}', rf'{sub_regex}', word)

# Update the parsed ALE with the new data
def update_ale(row_list, data_dicts):
    columns_index = row_list.index(['Column'])
    columns = row_list[columns_index + 1]

    data_index = row_list.index(['Data'])
    for index, item in enumerate(row_list[data_index + 1:]):
        row_list[data_index + 1 + index] = [data_dicts[index][column] for column in columns]

# Write the data into an ALE file with the specified filename
def write_ale(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(data)

################################################################################
input_filename = sys.argv[1]

row_list = read_ale(input_filename)

data_dicts = get_data_dicts(row_list)

if len(data_dicts) == 0:
    sys.exit(1)

shot_names = [data['Name'] for data in data_dicts]

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
                print(re.sub(rf'{search_regex}', lambda m: f'\033[2;36;42m{m.group().upper()}\033[0;0m', name))
            elif sub_regex == 'LO':
                print(re.sub(rf'{search_regex}', lambda m: f'\033[2;36;42m{m.group().lower()}\033[0;0m', name))
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

for item in data_dicts:
    item['Name'] = modify_word(item['Name'], search_regex, sub_regex)

update_ale(row_list, data_dicts)

print('Writing to file...')
output_filename = input_filename
if len(sys.argv) > 2:
    output_filename = sys.argv[2]
write_ale(row_list, output_filename)
