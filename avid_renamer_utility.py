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
def modify_word(word, search_value, sub_value, highlight_colour = None):
    if sub_value == 'UP':
        sub = lambda m: f'\033[{highlight_colour}m{m.group().upper()}\033[0;0m' if highlight_colour else lambda m: m.group().upper()
        return re.sub(rf'{search_value}', sub, word)
    if sub_value == 'LO':
        sub = lambda m: f'\033[{highlight_colour}m{m.group().lower()}\033[0;0m' if highlight_colour else lambda m: m.group().lower()
        return re.sub(rf'{search_value}', sub, word)

    sub = rf'\033[{highlight_colour}m{sub_value}\033[0;0m' if highlight_colour else rf'{sub_value}'
    return re.sub(rf'{search_value}', sub, word)

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

# Main logic loop
def run_avid_renamer_utility(input_filename, output_filename):
    row_list = read_ale(input_filename)

    data_dicts = get_data_dicts(row_list)

    if len(data_dicts) == 0:
        return 1

    shot_names = [data['Name'] for data in data_dicts]

    if len(shot_names) == 0:
        print('No shot names found')
        return 1

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
            print(modify_word(name, rf'({search_regex})', r'\1', '2;31;43'))

        # Sub input loop
        while should_commit is False:
            sub_regex = input('Enter substitution regex, UP for uppercase, LO for lowercase, RE to restart:')

            if sub_regex == 'RE':
                break

            print('Substitution preview:')
            for name in shot_names:
                print(modify_word(name, search_regex, sub_regex, '2;36;42'))

            commit_input = input('Do you want to commit this? Y/N:')
            if commit_input == 'Y' or commit_input == 'y':
                should_commit = True
            else:
                restart_point = input('Type SE to change search value, SU to change sub value:')
                if restart_point == 'SU':
                    continue
                else:
                    break

    # Update the name for each data item
    for item in data_dicts:
        item['Name'] = modify_word(item['Name'], search_regex, sub_regex)

    update_ale(row_list, data_dicts)

    print('Writing to file...')
    write_ale(row_list, output_filename)
    return 0

################################################################################
input_filename = sys.argv[1]

output_filename = input_filename
if len(sys.argv) > 2:
    output_filename = sys.argv[2]

ret = run_avid_renamer_utility(input_filename, output_filename)
sys.exit(ret)
