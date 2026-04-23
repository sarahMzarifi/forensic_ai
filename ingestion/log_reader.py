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
    except Exception as e:
        print(f"[Timestamp Error] {e} | Line: {line}")
        return None

    return {
        "timestamp": timestamp.isoformat(),  # readable format
        "pid": int(pid),
        "level": level,
        "component": component,
        "message": message
    }


def read_logs(file_path):
    """
    Generator function(memory efficient)
    """

    with open(file_path, "r") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()

            if not line:
                continue

            parsed = parse_log_line(line)

            if parsed:
                yield parsed
            else:
                # Debugging visibility (can be removed later)
                print(f"[Skipped Line {line_no}] {line}")