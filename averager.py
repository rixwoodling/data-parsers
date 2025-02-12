#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Averager / computes averages from multiple csv files and outputs a new csv
# Author / Rix Woodling
# updated 2025-01-23

import sys
import csv
from datetime import datetime



def print_help():
    print("python3 averager.py --help")
    print("python3 averager.py file1.csv file2.csv ...")
    print("python3 averager.py *.csv")

def output_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d-averaged-%H%M%S")
    return f"{timestamp}.csv"

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def read_csv_files(csv_files):
    all_data = []
    max_rows = 0
    max_cols = 0

    for file_path in csv_files:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.reader(csvfile))
            all_data.append(reader)
            if len(reader) > max_rows:
                max_rows = len(reader)
            local_max_cols = max((len(row) for row in reader), default=0)
            if local_max_cols > max_cols:
                max_cols = local_max_cols

    #print(all_data, max_rows, max_cols)
    return all_data, max_rows, max_cols

def create_output_matrix(rows, cols):
    #print([['' for x in range(cols)] for x in range(rows)])
    return [['' for x in range(cols)] for x in range(rows)]

def gather_cell_values(all_data, r, c):
    numeric_vals = []
    text_vals = []
    for data in all_data:
        if r < len(data) and c < len(data[r]):
            cell_val = data[r][c].strip()
            if is_float(cell_val):
                numeric_vals.append(float(cell_val))
            else:
                text_vals.append(cell_val)
    #print(numeric_vals, text_vals)
    return numeric_vals, text_vals

def compute_cell_value(numeric_vals, text_vals):
    # decide how to fill a single cell based on numeric vs text values
    if numeric_vals:
        return str(sum(numeric_vals) / len(numeric_vals))
    elif text_vals:
        return text_vals[0]
    else:
        return ""

def compute_averages(all_data, max_rows, max_cols):
    # compute averaged matrix given all_data from multiple csv files
    output_matrix = create_output_matrix(max_rows, max_cols)

    for r in range(max_rows):
        for c in range(max_cols):
            numeric_vals, text_vals = gather_cell_values(all_data, r, c)
            output_matrix[r][c] = compute_cell_value(numeric_vals, text_vals)
    #print(output_matrix)
    return output_matrix

def write_output_csv(output_matrix, output_filename):
    # write the final matrix to a csv file
    with open(output_filename, "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_matrix)
    print(f"Done! CSV averages written to {output_filename}")

def main():
    # Collect command line args, ignoring script name
    csv_files = sys.argv[1:]

    # Check if no arguments or help requested
    if not csv_files or "-h" in csv_files or "--help" in csv_files:
        print_help()
        sys.exit(0)

    # Pass list of CSV files to read_csv_files
    all_data, max_rows, max_cols = read_csv_files(csv_files)

    # compute the average matrix
    output_matrix = compute_averages(all_data, max_rows, max_cols)

    # generate output filename
    output_file = output_filename()

    # write out results
    write_output_csv(output_matrix, output_file)

if __name__ == "__main__":
    main()


