from ingestion.log_reader import read_logs
from processing.log_normaliser import normalize_log

logs = read_logs("data/raw_logs.log")

normalized = []

for log in logs:
    normalized.append(normalize_log(log))

print(f"Total normalized events: {len(normalized)}")

for event in normalized[:5]:
    print(event)