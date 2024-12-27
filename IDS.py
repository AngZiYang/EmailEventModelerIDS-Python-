# Import required modules
import sys  # For handling command-line arguments and system exit
import os  # For file and directory operations
import json  # For handling JSON data (reading/writing logs)
import math  # For mathematical operations (mean, variance, standard deviation)
import random  # For generating random values based on distributions

# Directory where logs will be stored
LOG_DIR = "logs"

# Data structures to store events and statistics
events = {}  # Stores event definitions from Events.txt
statistics = {}  # Stores statistical parameters from Stats.txt


# Reads event definitions from the Events.txt file
def read_events(file_path):
    """
    Reads and parses the Events.txt file to populate the `events` dictionary.

    Args:
        file_path (str): Path to the Events.txt file.

    Example:
        events = {
            "Logins": {"type": "D", "min": 0, "max": float("inf"), "weight": 2},
            ...
        }
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    # First line indicates the number of events
    num_events = int(lines[0].strip())
    
    for line in lines[1:num_events + 1]:
        parts = line.strip().split(":")
        if len(parts) != 5:
            print(f"Skipping invalid line in Events.txt: {line.strip()}")
            continue
        
        name, event_type, min_val, max_val, weight = parts
        events[name] = {
            "type": event_type,
            "min": float(min_val) if min_val else 0,
            "max": float(max_val) if max_val else float("inf"),
            "weight": int(weight)
        }


# Reads statistical data from the Stats.txt file
def read_statistics(file_path):
    """
    Reads and parses the Stats.txt file to populate the `statistics` dictionary.

    Args:
        file_path (str): Path to the Stats.txt file.

    Example:
        statistics = {
            "Logins": {"mean": 4.0, "std_dev": 1.5},
            ...
        }
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    # First line indicates the number of statistics
    num_stats = int(lines[0].strip())
    
    for line in lines[1:num_stats + 1]:
        parts = line.strip().split(":")
        if len(parts) != 4:
            print(f"Skipping invalid line in Stats.txt: {line.strip()}")
            continue
        
        name, mean, std_dev, _ = parts  # The last underscore ignores the empty part
        statistics[name] = {
            "mean": float(mean),
            "std_dev": float(std_dev)
        }


# Generates events based on input data and logs them
def generate_events(days):
    """
    Generates event data for the specified number of days and logs them.

    Args:
        days (int): Number of days to generate event data for.

    Returns:
        list: List of daily event data dictionaries.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    all_events = []  # Holds all events across days
    
    for day in range(days):
        log_file = os.path.join(LOG_DIR, f"day_{day + 1}.log")
        daily_events = {"Day": day + 1}  # Initialize dictionary for daily events
        
        for event_name, event_info in events.items():
            if event_name in statistics:
                mean = statistics[event_name]["mean"]
                std_dev = statistics[event_name]["std_dev"]
                if event_info["type"] == "C":  # Continuous event
                    value = max(event_info["min"], min(random.gauss(mean, std_dev), event_info["max"]))
                    value = round(value, 2)  # Round continuous values to 2 decimal places
                else:  # Discrete event
                    value = max(int(event_info["min"]), min(int(random.gauss(mean, std_dev)), int(event_info["max"])))
                
                daily_events[event_name] = value  # Add the event value to daily data
        
        # Write daily events to a log file
        with open(log_file, "w") as file:
            json.dump(daily_events, file, indent=4)
        
        all_events.append(daily_events)  # Add daily data to the list
    
    return all_events


# Analyzes baseline statistics from generated event logs
def analyze_stats():
    """
    Analyzes baseline statistics for events from the log files.

    Returns:
        dict: Baseline statistics for each event.
    """
    daily_totals = {name: [] for name in events.keys()}
    log_files = [f for f in os.listdir(LOG_DIR) if f.startswith("day_") and f.endswith(".log")]
    log_files.sort()  # Ensure files are processed in order

    for log_file in log_files:
        try:
            with open(os.path.join(LOG_DIR, log_file), "r") as file:
                daily_data = json.load(file)

            for event_name, value in daily_data.items():
                if event_name in daily_totals:
                    daily_totals[event_name].append(value)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading log file {log_file}: {e}")
            continue

    baseline_statistics = {}
    for event_name, values in daily_totals.items():
        if values:
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = math.sqrt(variance)
            total = sum(values)
            baseline_statistics[event_name] = {
                "total": total,
                "mean": round(mean, 2),
                "std_dev": round(std_dev, 2)
            }

    return baseline_statistics


# Main entry point for the program
def main():
    """
    Main function to execute the IDS program. Handles reading inputs,
    generating events, analyzing statistics, and detecting anomalies.
    """
    if len(sys.argv) != 4:
        print("Usage: python IDS.py <Events.txt> <Stats.txt> <days>")
        sys.exit(1)

    events_file = sys.argv[1]
    stats_file = sys.argv[2]

    try:
        days = int(sys.argv[3])
    except ValueError:
        print(f"Error: '{sys.argv[3]}' is not a valid number of days.")
        sys.exit(1)

    if not os.path.isfile(events_file) or not os.path.isfile(stats_file):
        print("Error: Input files not found.")
        sys.exit(1)

    read_events(events_file)
    read_statistics(stats_file)

    print("Generating events...")
    events_data = generate_events(days)
    for daily_events in events_data:
        print(json.dumps(daily_events, indent=4))

    print("Analyzing statistics...")
    baseline_statistics = analyze_stats()
    print(json.dumps(baseline_statistics, indent=4))


if __name__ == "__main__":
    main()
