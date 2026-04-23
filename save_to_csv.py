import csv
from pipeline import unified_pipeline

log_path = "data/raw_logs.log"
pcap_path = "data/first_sample.pcapng"

stream = unified_pipeline(
    log_file_path=log_path,
    pcap_file_path=pcap_path
)

output_file = "data/output.csv"

# CSV headers (union of log + pcap fields)
headers = [
    "type",
    "timestamp",
    "source",
    "event",
    "destination",
    "src_port",
    "dst_port",
    "length",
    "level",
    "pid"
]

with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()

    total = 0

    for event in stream:

        row = {
            "type": "log" if isinstance(event["timestamp"], str) else "pcap",
            "timestamp": event.get("timestamp"),
            "source": event.get("source"),
            "event": event.get("event"),

            # PCAP fields
            "destination": event.get("metadata", {}).get("destination"),
            "src_port": event.get("metadata", {}).get("src_port"),
            "dst_port": event.get("metadata", {}).get("dst_port"),
            "length": event.get("metadata", {}).get("length"),

            # LOG fields
            "level": event.get("metadata", {}).get("level"),
            "pid": event.get("metadata", {}).get("pid"),
        }

        writer.writerow(row)
        total += 1

print(f"Saved CSV to {output_file}")
print(f"Total events processed: {total}")