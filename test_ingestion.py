from ingestion.pcap_reader import read_pcap
from processing.pcap_normaliser import normalize_pcap
import os
import json


def get_file_path():
    path = input("Enter PCAP path (or press Enter to use default): ").strip()

    if path:
        return path

    return "data/first_sample.pcapng"


file_path = get_file_path()

if not os.path.exists(file_path):
    print("[ERROR] File not found")
    exit()


# Step 1: Read packets
packets = read_pcap(file_path)
print(f"Total packets: {len(packets)}")


# Step 2: Normalize packets
normalized_packets = []

for pkt in packets:
    normalized_packets.append(normalize_pcap(pkt))


print(f"Total normalized packets: {len(normalized_packets)}")


# Step 3: Print sample normalized output
for event in normalized_packets[:5]:
    print(event)