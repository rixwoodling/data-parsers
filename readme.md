## Parsers
- [Tast Data Parser](#features-of-tast-data-parser)
- [Multi-Benchmark Support](#multi-benchmark-support)
- [Data Extraction](#data-extraction)
- [Sorting and Padding](#sorting-and-padding)
- [CSV Output](#csv-output)


---
#### Tast Data Parser
This script processes benchmark results (Speedometer, Speedometer3, MotionMark1_3, WebXPRT4) by extracting data from results-chart.json files, calculating averages, and formatting output as CSV to stdout. It identifies and sorts runs based on directory structure, pads missing values, and ensures uniform columns.
```
python3 tast_parser.py path/to/tast_tests/ | tee output.csv
```
- Multi-Benchmark Support: Detects and processes results from Speedometer, Speedometer3, MotionMark1_3, and WebXPRT4 benchmarks.
- Data Extraction: Extracts relevant benchmark scores from results-chart.json files within the specified directories.
- Sorting and Padding: Organizes benchmark runs based on directory structure, fills missing values, and calculates averages.
- CSV Output: Outputs the structured results with headers and averages to stdout in CSV format.

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
#### Get Device Info
A Bash script to retrieve system device information for local or remote machines, output-friendly to CSV format.
```
bash ./get_device_info.sh | tee myspecs.csv
```
```
bash ./get_device_info.sh user@remote_ip
```
- Retrieves model name, memory details, OS version, build ID, and kernel release.
- Extracts CPU information, core counts, max frequencies, and GFX frequencies.
- Includes CBI settings and TME status.
- Supports local and remote execution via SSH.
---

