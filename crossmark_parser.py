#!/usr/bin/env python3
#
# Author:       Rix Woodling
# Created:      2024-10-14
# Description:  Parse Speedometer 3.0 ( soon to be more ) crossbench data into a table
# Last changed: 2024-10-14, Speedometer 3.0 and Score only output
#

import os
import sys
import json

# Function to check if the argument is provided
def check_argument():
    if len(sys.argv) < 2:
        print("# how to use")
        print("python3 crossbench_parser.py path/to/speedometer3.0/")
        print("python3 crossbench_parser.py path/to/speedometer3.0/ | tee mytest.csv")
        sys.exit(1)  # Exit if no argument is provided
    return sys.argv[1]

# Function to check if the path exists
def check_path_exists(path_arg):
    if os.path.exists(path_arg):
        return True
    else:
        print("Path doesn't exist.")
        sys.exit(1)

# Function to check if the path is a directory or file
def check_directory(path_arg):
    if os.path.isdir(path_arg):
#        print("Path exists and is a directory.")
        return path_arg  # Return the directory path
    elif os.path.isfile(path_arg):
        print("Please select a directory as the argument, not a file.")
        sys.exit(1)

# Get the target JSON filename based on keywords in the path
def get_target_filename(path_arg):
    # Determine which JSON file to look for based on the path.
    if "speedometer3.0" in path_arg:
        return "speedometer_3.0.json"
#    elif "speedometer" in path_arg:
#        return "speedometer_3.0.json"
#    elif "webxprt4" in path_arg:
#        return "webxprt4_results.json"
#    elif "motionmark1_3" in path_arg:
#        return "motionmark1_3.json"
    else:
        print("No recognized keyword found (speedometer3.0, speedometer, webxprt4, motionmark1_3).")
        sys.exit(1)

# Find the shallowest occurrence of the target JSON file and return its depth
def find_shallowest_depth(path_arg, json_file):
    # Find the shallowest occurrence of the target JSON file and return its depth.
    shallowest_depth = float('inf')

    # Walk the directory tree starting from the given path
    for root, _, files in os.walk(path_arg):
        if json_file in files:
            current_depth = root.count(os.sep)
            if current_depth < shallowest_depth:
                shallowest_depth = current_depth

    if shallowest_depth == float('inf'):
        print(f"No '{json_file}' file found in {path_arg}.")
        sys.exit(1)  # Exit if no valid JSON is found

    return shallowest_depth

# Find all occurrences of the target JSON file up to the specified depth
def find_results_json(path_arg, json_file, max_depth):
    # Find all occurrences of the target JSON file up to the specified depth.
    results = []

    # Walk the directory tree starting from the given path
    for root, dirs, files in os.walk(path_arg):
        current_depth = root.count(os.sep)

        # Stop traversal if the depth exceeds the max depth
        if current_depth > max_depth:
            del dirs[:]  # Prevent deeper traversal
            continue

        if json_file in files:
            results.append(os.path.join(root, json_file))

    return results

# Function to identify the first non-unique column (separated by '/')
def find_non_unique_column(results):
    if not results:
        print("No results to process.")
        return None  # Handle the case where the input is empty

    # Split each result path into components
    split_results = [result.split('/') for result in results]

    # Iterate through the columns of the paths
    for i in range(len(split_results[0])):
        # Extract the i-th element from each split path
        column_elements = [path[i] for path in split_results]

        # Check if all elements in this column are the same
        if len(set(column_elements)) > 1:
            # Adding 1 to make it 1-based index
            return i + 1

    print("All columns are unique across the paths.")
    return None  # If no non-unique column is found

def collect_unique_column(results, non_unique_column):
    # Collect unique values from the specified non-unique column.
    if non_unique_column is None:
        print("No non-unique column found.")
        return []  # Return an empty list if no non-unique column is found

    # Split each path into components
    split_results = [result.split('/') for result in results]

    # Extract the elements from the specified column (1-based index)
    column_values = [path[non_unique_column - 1] for path in split_results]

    # Get unique values and sort them (by length and then lexicographically)
    unique_values = sorted(set(column_values), key=lambda x: (len(x), x))

    return unique_values  # Always return a list of unique values

# Function to sort the results based on unique values
def sort_results_by_unique_values(results, unique_values):
    # Sort results within each group of unique values.
    sorted_results = []

    # Loop through each unique value
    for value in unique_values:
        # Filter results that contain the current unique value as a component
        value_results = [result for result in results if f"/{value}/" in result]

        if value_results:
            # Split each path into components
            split_results = [result.split('/') for result in value_results]

            # Determine the length of the shortest path
            max_depth = min(len(path) for path in split_results)

            # If only one result exists for this unique value, add it directly
            if len(value_results) == 1:
                sorted_results.extend(value_results)
                continue

            # Compare components starting from the end, moving backwards
            for i in range(1, max_depth + 1):
                # Get the i-th component from the end for all paths
                components = [path[-i] for path in split_results]

                # Check if the components differ
                if len(set(components)) > 1:
                    # Sort by this non-unique component and add to the sorted list
                    sorted_value_results = sorted(value_results, key=lambda x: x.split('/')[-i])
                    sorted_results.extend(sorted_value_results)
                    break
            else:
                # If all components are identical, just add the unsorted results
                sorted_results.extend(value_results)

    return sorted_results

def parse_data_from_json_files(unique_values, sorted_results, json_key="Score"):
    # Parse JSON files and return a nested list of headers with extracted average values.
    main_list = []

    # Loop through each unique value (e.g., 'BLUE', 'RED')
    for value in unique_values:
        value_list = [value]  # Start the sublist with the unique value as the header

        # Filter results that match the current unique value
        value_results = [result for result in sorted_results if f"/{value}/" in result]

        # Process each matching JSON file and extract the 'average' value
        for result in value_results:
            try:
                with open(result, 'r') as f:
                    data = json.load(f)

                    # Dynamically get the first key at the top level (e.g., "chrome", "firefox", etc.)
                    top_level_key = next(iter(data))

                    # Navigate to the 'average' value
                    score = data[top_level_key]["data"][json_key]["average"]

                    value_list.append(f"{score:.2f}")  # Add the formatted score to the list
            except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error processing file {result}: {e}")
                continue  # Skip to the next result if there's an error

        # Append the completed sublist to the main list
        main_list.append(value_list)

    return main_list

# Function to find the largest sublist in main_list and return its size
def find_largest_sublist(main_list):
    # Find the largest sublist in main_list and return its size.
    max_length = 0  # Initialize the max length variable

    # Loop through each sublist in the main_list
    for sublist in main_list:
        # Compare the current sublist length with the max length
        if len(sublist) > max_length:
            max_length = len(sublist)  # Update max length if this sublist is larger

    return max_length  # Return the size of the largest sublist

# Function to calculate the average for sublist values and pad sublists
def pad_and_average_sublists(main_list):
    # Pad sublists to the same length and append the average of their values.
    max_length = find_largest_sublist(main_list)  # Find the largest sublist size

    for sublist in main_list:
        # Convert values (from the second item onward) to floats for averaging
        values_to_average = [float(value) for value in sublist[1:]]

        # Calculate the average if there are values, otherwise set to 0
        avg_value = sum(values_to_average) / len(values_to_average) if values_to_average else 0

        # Pad the sublist with empty strings until it matches the largest sublist size
        sublist.extend([''] * (max_length - len(sublist)))

        # Append the average (formatted to 2 decimal places) at the end of the sublist
        sublist.append(f"{avg_value:.2f}")

    return main_list

# Function to create the header and insert it into the main list
def insert_header(main_list, json_file, largest_sublist_size):
    # Create the header and insert it into the main list.

    # Use the target filename as the base for the header key
    # Remove underscores, capitalize the first word, and strip ".json"
    header_key = json_file.replace("_", " ").replace(".json", "").capitalize()

    # Create a list for the header, starting with the formatted key
    header = [header_key]

    # Add "R1", "R2", ..., up to "R{largest_sublist_size - 1}"
    for i in range(1, largest_sublist_size):
        header.append(f"R{i}")

    # Append 'Avg' as the last column
    header.append("Avg")

    # Insert the header at the start of the main list
    main_list.insert(0, header)

    return main_list

# Function to print each sublist in CSV format
def print_as_csv(main_list):
    for sublist in main_list:
        # Join the sublist elements into a single CSV-formatted string
        csv_line = ','.join(sublist)
        print(csv_line)


def main():
    # Get the argument and check if it's valid
    path_arg = check_argument()
#    print(path_arg)

    # Check if the path exists
    check_path_exists(path_arg)
#    print(check_path_exists(path_arg))

    # Check if the path is a directory
    directory = check_directory(path_arg)
#    print(directory)

    # Determine the target JSON filename
    json_file = get_target_filename(path_arg)
#    print(json_file)

    # Find the shallowest depth of the target JSON file
    shallowest_depth = find_shallowest_depth(directory, json_file)
#    print(shallowest_depth)

    # Find all occurrences of the target JSON file up to the shallowest depth
    results = find_results_json(path_arg, json_file, shallowest_depth)
#    print(results)

    # Identify the first non-unique column in the results
    non_unique_column = find_non_unique_column(results)
#    print(non_unique_column)

    # Collect and print unique values from the non-unique column
    unique_values = collect_unique_column(results, non_unique_column)
#    print(unique_values)

    # Sort the results by unique values
    sorted_results = sort_results_by_unique_values(results, unique_values)
#    print(sorted_results)

    # Parse the JSON files and extract average values
    main_list = parse_data_from_json_files(unique_values, sorted_results)
#    print(main_list)

    # Find the largest sublist in the parsed data
    largest_sublist_size = find_largest_sublist(main_list)
#    print(largest_sublist_size)

    # Pad and average the sublists
    padded_main_list = pad_and_average_sublists(main_list)
#    print(padded_main_list)

    # Insert the header into the main list
    final_list = insert_header(padded_main_list, json_file, largest_sublist_size)
#    print(final_list)

    # Print each sublist in CSV format
    print_as_csv(main_list)


if __name__ == "__main__":
    main()


#
