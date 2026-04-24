from pipeline import unified_pipeline
from processing.correlation_engine import group_by_source, event_type_distribution

# input paths
log_path = "data/raw_logs.log"
pcap_path = "data/first_sample.pcapng"

# get event stream
stream = unified_pipeline(
    log_file_path=log_path,
    pcap_file_path=pcap_path
)

# group events
grouped = group_by_source(stream)

print("\n--- TOP ACTIVE SOURCES ---\n")

# sort by activity
sorted_sources = sorted(
    grouped.items(),
    key=lambda x: len(x[1]),
    reverse=True
)

#Separate IPs and system sources
ip_sources = []
system_sources = []

for source, events in sorted_sources:
    if source and (":" in source or "." in source):
        ip_sources.append((source, events))
    else:
        system_sources.append((source, events))


#PRINT TOP IP SOURCES
print("TOP NETWORK SOURCES (IPs):\n")
for source, events in ip_sources[:5]:
    print(f"{source} → {len(events)} events")

#PRINT TOP SYSTEM SOURCES
print("\nTOP SYSTEM SOURCES:\n")
for source, events in system_sources[:5]:
    print(f"{source} → {len(events)} events")


#EVENT TYPE DISTRIBUTION
distribution = event_type_distribution(grouped)

print("\n--- EVENT TYPE BREAKDOWN (TOP 3 SOURCES) ---\n")

for source, _ in sorted_sources[:3]:
    print(f"\n{source}:")

    for event_type, count in distribution[source].items():
        print(f"  {event_type} → {count}")