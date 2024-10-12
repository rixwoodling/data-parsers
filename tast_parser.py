#!/usr/bin/env python3
#
# Author:      Rix Woodling
# Created:     2024-10-11
# Description: Parse Speedometer, Speedometer3, MotionMark1_3, and WebXPRT4 tast data into a table 
# Version:     1.0
#


import os
import sys
import json

# Function to check if the argument is provided
def check_argument():
    if len(sys.argv) < 2:
        print("# how to use")
        print("python3 tast_parser.py path/to/tast_tests/")
        print("python3 tast_parser.py path/to/tast_tests/ | tee mytest.csv")
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

# Function to find all "results-chart.json" files in the directory
def find_results_json(path_arg):
    results = []
    # Use os.walk to search the directory
    for root, dirs, files in os.walk(path_arg):
        for file in files:
            if file == "results-chart.json":
                results.append(os.path.join(root, file))
    return results

# Function to print the results
def print_results(results):
    # Output the found results
    if results:
        print("Found the following results-chart.json files:")
        for result in results:
            print(result)
    else:
        print("No results-chart.json files found.")

# Function to count "/" characters in the first result path
def count_slashes(results):
    if results:
        first_result = results[0]  # Get the first file path
        slash_count = first_result.count('/')  # Count the "/" characters
#        print(f"Number of '/' characters in the first result: {slash_count}")
        return slash_count
    else:
        print("No results to calculate '/' count.")
        return 0

# Function to identify the first non-unique column (separated by '/')
def find_non_unique_column(results):
    # Split each result path into components
    split_results = [result.split('/') for result in results]

    # Iterate through the columns of the paths
    for i in range(len(split_results[0])):
        # Extract the i-th element from each split path
        column_elements = [path[i] for path in split_results]

        # Check if all elements in this column are the same
        if len(set(column_elements)) > 1:
#            print(f"Non-unique column is: {i + 1}")  # Adding 1 to make it 1-based index
            return i + 1

#    print("All columns are unique or no variation found.")
    return None

# Function to collect unique values from the varying column
def collect_unique_column(results, column_index):
    # Split each path into components
    split_results = [result.split('/') for result in results]

    # Extract the elements in the specified column (column_index is 1-based)
    column_values = [path[column_index - 1] for path in split_results]

    # Get unique values and sort them numerically (convert to int where possible)
    unique_values = sorted(set(column_values), key=lambda x: (len(x), x))  # Sorting by length then value
    return unique_values

# Function to check the argument and return the specific JSON key to use
def process_based_on_argument(path_arg):
    if "speedometer3" in path_arg:
#        print("Processing for speedometer3...")
        return "Benchmark.Speedometer3.Score"
    elif "speedometer" in path_arg:
#        print("Processing for speedometer...")
        return "Benchmark.Speedometer.Score"
    elif "webxprt4" in path_arg:
#        print("Processing for webxprt4...")
        return "Benchmark.WebXPRT4.Score"
    elif "motionmark1_3" in path_arg:
#        print("Processing for motionmark1_3...")
        return "Benchmark.MotionMark.Score"
    else:
        print("No recognized keyword (speedometer, speedometer3, webxprt4, motionmark1_3) found in the argument.")
        sys.exit(1)

# Function to sort the results by header and subdirectory, using the last unique component
def sort_results_by_header_and_last_unique_component(results, headers):
    sorted_results = []

    # Loop through each header in the header list
    for header in headers:
        # Filter results that match the current header
        header_results = [result for result in results if f"/{header}/" in result]

        if header_results:
            # Split each path into components (using '/' as the delimiter)
            split_results = [result.split('/') for result in header_results]

            # Determine the length of the shortest path
            max_depth = min(len(path) for path in split_results)

            # If there's only one result for this header, append it directly
            if len(header_results) == 1:
                sorted_results.extend(header_results)
                continue

            # Start comparing components from the end, going backwards
            for i in range(1, max_depth + 1):
                # Get the i-th component from the end for all paths (e.g., run1, run2)
                components = [path[-i] for path in split_results]

                # Check if all components are the same
                if len(set(components)) > 1:
                    # Found the first non-unique component, now sort by this component
                    sorted_header_results = sorted(header_results, key=lambda x: x.split('/')[-i])
                    sorted_results.extend(sorted_header_results)  # Add sorted header-specific results to the overall list
                    break
            else:
                # If all components are the same (e.g., all run1), append them directly
                sorted_results.extend(header_results)
        else:
            # If there are no header results, just skip
            continue

    return sorted_results

# Function to load and extract the 'value' from each JSON file, using the provided key
def extract_value_from_json(json_file_path, json_key):
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            # Use the provided key to navigate through the JSON structure
            return data[json_key]["summary"]["value"]
    except (KeyError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error processing file {json_file_path}: {e}")
        return None  # Return None if there's an error

# Function to parse data and return a main list of sublists with headers and values
def parse_data(headers, sorted_results, json_key):
    main_list = []

    # Loop through each header
    for header in headers:
        header_list = [header]  # Start with the header name (e.g., 'TEST_A')

        # Filter results that match the current header
        header_results = [result for result in sorted_results if f"/{header}/" in result]

        # For each result (JSON file path), extract the value using the provided JSON key
        for result in header_results:
            value = extract_value_from_json(result, json_key)
            if value is not None:
                header_list.append(f"{value:.2f}")  # Append the value to the header list

        # Append the header list (with values) to the main list
        main_list.append(header_list)

    return main_list

# Function to find the largest sublist in main_list and return its size
def find_largest_sublist(main_list):
    max_length = 0  # Initialize the max length variable

    # Loop through each sublist in the main_list
    for sublist in main_list:
        # Compare the current sublist length with the max length
        if len(sublist) > max_length:
            max_length = len(sublist)  # Update max length if this sublist is larger

    return max_length  # Return the size of the largest sublist

# Function to calculate the average for sublist values and pad sublists
def pad_and_average_sublists(main_list):
    max_length = find_largest_sublist(main_list)  # Find the largest sublist size

    for sublist in main_list:
        # Convert values (from second item onward) to floats for averaging
        values_to_average = [float(value) for value in sublist[1:]]

        # Calculate the average if there are values
        avg_value = sum(values_to_average) / len(values_to_average) if values_to_average else 0

        # Pad the sublist with empty strings until it matches the largest sublist size
        sublist.extend([''] * (max_length - len(sublist)))

        # Append the average at the end of the sublist
        sublist.append(f"{avg_value:.2f}")

    return main_list

# Function to create the header and insert it into the main list
def insert_header(main_list, json_key, largest_sublist_size):
    # Strip "Benchmark." and ".Score" from the process_based_on_argument value
    header_key = json_key.replace("Benchmark.", "").replace(".Score", "")

    # Create a list for the header, starting with the stripped key
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

    # Check if the path exists
    check_path_exists(path_arg)

    # Check if the path is a directory
    directory = check_directory(path_arg)

    # Find all instances of "results-chart.json"
    results = find_results_json(directory)

    # Output the results using the new print_results function
#    print_results(results)

    # Count the "/" characters in the first result
    count_slashes(results)

    # Find the non-unique column in the results
    non_unique_column = find_non_unique_column(results)

    # Collect and sort the unique values from that column
    headers = collect_unique_column(results, non_unique_column)
#    print(f"Headers: {headers}")

    # Sort the results by header and subdirectory (merged logic)
    sorted_results = sort_results_by_header_and_last_unique_component(results, headers)

    # Print the sorted results
#    print_results(sorted_results)

    # Call process_based_on_argument to process and parse the results
    #process_based_on_argument(path_arg)

    # Get the appropriate key for JSON parsing (e.g., 'Benchmark.Speedometer.Score')
    json_key = process_based_on_argument(path_arg)

    # Parse data and get the main list of headers and values
    main_list = parse_data(headers, sorted_results, json_key)

    largest_sublist_size = find_largest_sublist(main_list)
#    print(f"Largest sublist contains {largest_sublist_size} items")

    # Modify each sublist by padding and adding the average
    updated_main_list = pad_and_average_sublists(main_list)

    # Insert the header based on the largest sublist size
    main_list_with_header = insert_header(main_list, json_key, largest_sublist_size)
#    print(json_key)

    # Print each sublist in CSV format
    print_as_csv(main_list)

if __name__ == "__main__":
    main()


#
