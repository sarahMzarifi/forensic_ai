from ingestion.pcap_reader import read_pcap
from processing.pcap_normaliser import normalize_pcaps
import os


def get_file_path():
    path = input("Enter PCAP path (or press Enter to use default): ").strip()

    if path:
        return path

    return "data/first_sample.pcapng"


file_path = get_file_path()

if not os.path.exists(file_path):
    print("[ERROR] File not found")
    exit()


# Step 1: Read packets (generator)
packets = read_pcap(file_path)


# Step 2: Normalize packets (generator pipeline)
normalized_stream = normalize_pcaps(packets)


# Step 3: Debug print first 5 events
print("\nSample normalized packets:\n")

count = 0
total = 0

for event in normalized_stream:
    if count < 5:
        print(event)
        count += 1

    total += 1


print(f"\nTotal normalized packets: {total}")