
---
#### Tast Data Parser
This script processes benchmark results (Speedometer, Speedometer3, MotionMark1_3, WebXPRT4) by extracting data from results-chart.json files, calculating averages, and formatting output as CSV to stdout. It identifies and sorts runs based on directory structure, pads missing values, and ensures uniform columns.
```
python3 tast_parser.py path/to/tast_tests/ | tee output.csv
```
```
Speedometer3,R1,R2,Avg
TEST_A,342.45,234.34,233.37
TEST_B,123.34,567.89,345.61
```
---
#### Crossmark Data Parser
A Python script that parses Speedometer 3.0 benchmark data (and future benchmarks) into a structured table with averages and outputs it in CSV format.
```
python3 crossbench_parser.py path/to/speedometer3.0/ | tee mytest.csv
```
- Flexible JSON Handling: Detects JSON files dynamically based on directory structure.
- Data Extraction: Extracts "average" scores from nested JSON data.
- Sorting and Padding: Sorts results by directories, pads missing values, and calculates averages.
- CSV Format: Outputs the final table with headers and averages to stdout.
---
  
