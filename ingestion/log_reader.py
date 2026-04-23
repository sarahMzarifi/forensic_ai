import re
from datetime import datetime

def parse_log_line(line):
    """
    Parses HDFS log line into structured format
    """

    pattern = r"(\d{6}) (\d{6}) (\d+) (\w+) ([\w\.$]+): (.*)"

    match = re.match(pattern, line)
    if not match:
        return None

    date_str, time_str, pid, level, component, message = match.groups()

    # Convert timestamp
    try:
        timestamp = datetime.strptime(date_str + time_str, "%y%m%d%H%M%S")
    except:
        return None

    return {
        "timestamp": timestamp.isoformat(),  # keep readable for now
        "pid": int(pid),
        "level": level,
        "component": component,
        "message": message
    }


def read_logs(file_path):
    """
    Reads log file and returns structured events
    """

    events = []

    with open(file_path, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                events.append(parsed)

    return events