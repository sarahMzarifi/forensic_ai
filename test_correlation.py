from pipeline import unified_pipeline
from processing.correlation_engine import (
    group_by_source,
    build_correlation_summary,
    detect_suspicious_sources,
    is_ip
)

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

# build structured summary
summary = build_correlation_summary(grouped)

print("\n--- TOP ACTIVE SOURCES ---\n")

# sort by total_events
sorted_sources = sorted(
    summary.items(),
    key=lambda x: x[1]["total_events"],
    reverse=True
)

# Separate IPs and system sources
ip_sources = []
system_sources = []

for source, data in sorted_sources:
    if is_ip(source):
        ip_sources.append((source, data))
    else:
        system_sources.append((source, data))


#PRINT TOP IP SOURCES
print("TOP NETWORK SOURCES (IPs):\n")
for source, data in ip_sources[:5]:
    print(f"{source} → {data['total_events']} events")


#PRINT TOP SYSTEM SOURCES
print("\nTOP SYSTEM SOURCES:\n")
for source, data in system_sources[:5]:
    print(f"{source} → {data['total_events']} events")


#EVENT TYPE BREAKDOWN
print("\n--- EVENT TYPE BREAKDOWN (TOP 3 SOURCES) ---\n")

for source, data in sorted_sources[:3]:
    print(f"\n{source} (Total: {data['total_events']}):")

    for event_type, count in data["event_distribution"].items():
        print(f"  {event_type} → {count}")


#STEP 2 — SUSPICIOUS DETECTION
suspicious = detect_suspicious_sources(summary)

print("\n--- SUSPICIOUS SOURCES ---\n")

if not suspicious:
    print("No suspicious sources detected\n")

for item in suspicious:
    print(f"{item['source']} → {item['total_events']} events")
    print(f"  Reasons: {', '.join(item['reasons'])}")
    print(f"  Dominance: {item['dominance']}\n")