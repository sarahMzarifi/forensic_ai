from pipeline import unified_pipeline

#paths
log_path = "data/raw_logs.log"
pcap_path = "data/first_sample.pcapng"

stream = unified_pipeline(
    log_file_path=log_path,
    pcap_file_path=pcap_path
)

print("\n--- SAMPLE OUTPUT ---\n")

count = 0

for event in stream:
    if count < 10:   # print first 10 events only
        print(event)

    count += 1

print(f"\nTotal events processed: {count}")