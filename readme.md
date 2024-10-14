
# Tast Data Parser

This script parses results from various benchmark tests (Speedometer, Speedometer3, MotionMark1_3, and WebXPRT4) into a structured table. The data is extracted from `results-chart.json` files located in the specified directory and outputted in CSV format.

## Features

- Supports multiple benchmarks: Speedometer, Speedometer3, MotionMark1_3, and WebXPRT4.
- Automatically identifies and sorts benchmark runs based on the directory structure.
- Calculates averages for each test and pads missing values to maintain uniform table structure.
- Outputs the results as a CSV file.

## Usage

Run the script by providing the path to the test directory:

```bash
python3 tast_parser.py path/to/tast_tests/
```

To save the output to a file:

```bash
python3 tast_parser.py path/to/tast_tests/ | tee output.csv
```

## Example Output

If your test data contains multiple runs for Speedometer3, the CSV output will look like:

```
Speedometer3,R1,R2,R3,Avg
TEST_A,342.45,234.34,123.34,233.37
TEST_B,123.34,567.89,,345.61
```

## Script Breakdown

1. **Argument Parsing**: Checks if the directory path is provided and valid.
2. **Data Extraction**: Scans the directory for `results-chart.json` files and extracts benchmark scores.
3. **Sorting & Padding**: Sorts the results based on the directory structure and adds padding to ensure all rows have the same number of columns.
4. **CSV Output**: Formats the results into CSV format, including headers and calculated averages.

## Requirements

- Python 3
- Ensure the directory structure includes `results-chart.json` files for each test run.

## Author

- **Rix Woodling**  
  Created: October 11, 2024

## License

This project is open-source and available under the MIT License.
