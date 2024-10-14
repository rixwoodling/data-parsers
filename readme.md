
---
#### Tast Data Parser
This script processes benchmark results (Speedometer, Speedometer3, MotionMark1_3, WebXPRT4) by extracting data from results-chart.json files, calculating averages, and formatting output as CSV to stdout. It identifies and sorts runs based on directory structure, pads missing values, and ensures uniform columns.
```
python3 tast_parser.py path/to/tast_tests/ | tee output.csv
```
> Speedometer3,R1,R2,Avg
> TEST_A,342.45,234.34,233.37
> TEST_B,123.34,567.89,345.61
---

