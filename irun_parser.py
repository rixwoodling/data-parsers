#!/usr/bin/env python3
#
# Author:       Rix Woodling
# Created:      2024-10-15
# Description:  Parse browserbench interactive runner html data into a table
# Last changed: 2024-10-15, tested for Speedometer 2.1 only
#

import os
import sys
from html.parser import HTMLParser
from collections import defaultdict

def check_argument():
    # Ensure an HTML file argument is provided.
    if len(sys.argv) < 2:
        print("Usage: python3 irun_parser.py path/to/file.html")
        sys.exit(1)
    return sys.argv[1]

def check_path_exists(path_arg):
    # Ensure the provided path exists and is an HTML file.
    if not os.path.exists(path_arg):
        print(f"Error: File '{path_arg}' does not exist.")
        sys.exit(1)
    if not path_arg.endswith(".html"):
        print("Error: The provided file must be an HTML file.")
        sys.exit(1)
    return path_arg

def parse_pre_content(html_file):
    # Extract content inside the <pre> tag from an HTML file.
    pre_content = ""
    recording = False  # Track if we're inside the <pre> tag

    def handle_starttag(tag, attrs):
        nonlocal recording
        if tag == "pre":
            recording = True

    def handle_endtag(tag):
        nonlocal recording
        if tag == "pre":
            recording = False

    def handle_data(data):
        nonlocal pre_content
        if recording:
            pre_content += data  # Collect all content inside the <pre> block

    # Create the parser and assign handlers
    parser = HTMLParser()
    parser.handle_starttag = handle_starttag
    parser.handle_endtag = handle_endtag
    parser.handle_data = handle_data

    # Parse the HTML content
    with open(html_file, 'r') as f:
        parser.feed(f.read())

    return pre_content.strip()  # Return the content inside <pre>

def replace_colons_with_commas(pre_content):
    # Replace all colons with commas and remove surrounding whitespace.
    lines = pre_content.splitlines()
    updated_lines = []

    for line in lines:
        # Split by colon and join with commas, removing extra whitespace
        parts = [part.strip() for part in line.split(':')]
        updated_lines.append(','.join(parts))

    return updated_lines  # Return list of updated lines

def group_lines_by_first_value(lines):
    # Group lines into sublists based on the first CSV value.
    grouped_content = defaultdict(list)

    # Group lines by the first value in each line (CSV format)
    for line in lines:
        first_value = line.split(',')[0]
        grouped_content[first_value].append(line)

    grouped_sublists = []

    # Modify the last item in each group and add the group to the final list
    for group in grouped_content.values():
        if group:
            # Modify the last item in the group
            last_item_parts = group[-1].split(',', 1)
            modified_last_item = f"{last_item_parts[0]},,,{last_item_parts[1]}"
            group[-1] = modified_last_item

        grouped_sublists.append(group)  # Add the group without a blank line

    return grouped_sublists

def split_into_nested_sublists(grouped_sublists):
    """Split each item in the grouped sublists into nested sublists."""
    nested_sublists = []

    # Loop through each group
    for group in grouped_sublists:
        nested_group = [line.split(',') for line in group]  # Split each line by ','
        nested_sublists.append(nested_group)  # Add the nested group to the list

    return nested_sublists

def round_third_item_in_nested_sublists(nested_sublists):
    """Round the fourth item (index 3) in each nested sublist to the nearest hundredth."""
    for group in nested_sublists:
        for sub in group:
            if len(sub) > 3:
                item = sub[3]
                # Check if the item has any suffix (e.g., ' ms', ' rpm')
                for suffix in [' ms', ' rpm']:  # Add more suffixes as needed
                    if item.endswith(suffix):
                        try:
                            # Remove the suffix and strip any extra spaces
                            number_str = item.replace(suffix, '').strip()
                            # Convert to float and round to 2 decimal places
                            rounded_number = f"{float(number_str):.2f}"
                            # Reassemble the rounded number with the suffix
                            sub[3] = f"{rounded_number}{suffix}"
                        except ValueError as e:
                            print(f"Error rounding item '{item}': {e}")  # Debug if needed
                        break  # Stop checking suffixes once a match is found
    return nested_sublists

def filter_out_last_four_sublists(nested_sublists):
    # Filter out the last four nested sublists from the output.
    if len(nested_sublists) > 4:
        return nested_sublists[:-4]  # Exclude the last four sublists
    return []  # If there are 4 or fewer sublists, return an empty list

def print_header():
    # Print the header for the output.
    header = ['test', 'step', 'a/sync', 'value']
    print(','.join(header))  # Join and print the header with commas

def print_nested_sublists(nested_sublists):
    # Print each nested sublist, joining items with commas.
    for i, group in enumerate(nested_sublists):
        for sub in group:
            print(','.join(sub))  # Join each sublist with commas and print

        # Add a blank line only between groups (not after the last group)
        if i < len(nested_sublists) - 1:
            print()

def print_last_item_of_each_sublist(nested_sublists):
    # Print the last item from each nested sublist.
    for group in nested_sublists:
        if group:  # Ensure the group is not empty
            last_item = group[-1]  # Get the last item of the current group
            print(','.join(last_item))  # Print the last item joined by commas



def main():
    # Get the argument and validate the path
    path_arg = check_path_exists(check_argument())
#    print(path_arg)

    # Parse the HTML file for <pre> tag content
    pre_content = parse_pre_content(path_arg)
#    print(pre_content)

    # Replace colons with commas in the content
    updated_lines = replace_colons_with_commas(pre_content)
#    print(updated_lines)

    # Group lines by the first CSV value
    grouped_lines = group_lines_by_first_value(updated_lines)
#    print(grouped_lines)

    # Split the grouped lines into nested sublists
    nested_sublists = split_into_nested_sublists(grouped_lines)
#    print(nested_sublists)

    # Round the third item (index 3) in each nested sublist
    rounded_sublists = round_third_item_in_nested_sublists(nested_sublists)
#    print(rounded_sublists)

    # Filter out the last four sublists
    filtered_sublists = filter_out_last_four_sublists(rounded_sublists)
#    print(filtered_sublists)

# ->|
    print_header()

    print_nested_sublists(filtered_sublists)

    print("")

    print_last_item_of_each_sublist(nested_sublists)

    print("")
# ->|

if __name__ == "__main__":
    main()
