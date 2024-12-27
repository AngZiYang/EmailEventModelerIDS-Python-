# Email System Event Modeler & Intrusion Detection System (IDS)

This repository contains a Python-based implementation of an Email System Event Modeler and Intrusion Detection System (IDS). The system models email-related events, generates activity logs, analyzes event statistics, and detects anomalies based on baseline statistics.

---

## Features

### 1. **Initial Input Phase**
- Reads event parameters from `Events.txt` (e.g., event types, constraints, and weights).
- Reads statistical distributions from `Stats.txt` (e.g., mean and standard deviation for each event).
- Detects and reports inconsistencies between `Events.txt` and `Stats.txt`.

### 2. **Activity Engine**
- Simulates event data for a specified number of days based on input statistics.
- Logs events in JSON format for easy readability and processing.

### 3. **Analysis Engine**
- Processes the logged data to compute daily totals, mean, and standard deviation for each event.
- Saves processed statistics in a structured file for reference.

### 4. **Alert Engine**
- Detects anomalies by comparing generated event data against baseline statistics.
- Calculates an anomaly counter for each day and compares it against a threshold.
- Flags days with anomalies exceeding the threshold.

## How to Run
step 1 
Open a Terminal or Command Prompt:
Navigate to the folder where the IDS.py script and the input files (Events.txt and Stats.txt) are stored.

step 2
Run the Script: In the terminal : python3 IDS.py Events.txt Stats.txt <days>
Replace <days> with the number of days you want to generate. 
For example: python3 IDS.py Events.txt Stats.txt 10

step 3
Interact with the Script:
It will read the Events.txt and Stats.txt files.
Threshold Calculation: The script calculates a threshold for anomaly detection. This threshold is based on the sum of the weights of all the events.

step 4
Prompt to Load Another Statistics File:
If the user enters y, the script will ask for a new statistics file name and repeat the process.
Enter new statistics file name: Stats_new.txt

If the user enters n, the script will exit.

step 5
prompt to Enter number of days to generate events:
it must be integer

step 6
The anomaly detection results will be saved in a file called log.json
The status result will flag out if anomaly_counter is higher then threshold.
return back to step 4 (Prompt to Load Another Statistics File:)
