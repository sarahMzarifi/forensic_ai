from ingestion.log_reader import read_logs
from processing.log_normaliser import normalize_logs


# Step 1: Create generator stream
logs = read_logs("data/raw_logs.log")

# Step 2: Normalize using generator pipeline
normalized_stream = normalize_logs(logs)


print("\nSample normalized logs:\n")

count = 0
total = 0

# Step 3: Iterate (stream processing)
for event in normalized_stream:
    if count < 5:
        print(event)
        count += 1

    total += 1


print(f"\nTotal normalized events: {total}")