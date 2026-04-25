import re


def is_ip(source):
    """
    Check if source is an IP address (IPv4 or IPv6)
    """
    if not source:
        return False

    # IPv4
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", source):
        return True

    # IPv6
    if ":" in source:
        return True

    return False


def group_by_source(events):
    """
    Groups events by source
    """
    grouped = {}

    for event in events:
        source = event.get("source")

        if not source:
            continue

        if source not in grouped:
            grouped[source] = []

        grouped[source].append(event)

    return grouped


def build_correlation_summary(grouped):
    """
    Build a structured summary per source
    """
    summary = {}

    for source, events in grouped.items():
        event_counts = {}

        for event in events:
            event_type = event.get("event_type") or "unknown"

            if event_type not in event_counts:
                event_counts[event_type] = 0

            event_counts[event_type] += 1

        sorted_event_counts = dict(
            sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
        )

        summary[source] = {
            "total_events": len(events),
            "event_distribution": sorted_event_counts
        }

    return summary


def detect_suspicious_sources(summary):
    """
    Final refined suspicious detection:
    - Focus only on network sources (IPs)
    - High activity + behavior patterns
    - Deviation-based refinement
    """

    suspicious = []

    #Compute average activity
    total_events_all = sum(data["total_events"] for data in summary.values())
    avg_events = total_events_all / len(summary)

    HIGH_ACTIVITY_THRESHOLD = avg_events * 2
    MIN_EVENTS = 50

    #Compute average dominance
    dominance_list = []

    for source, data in summary.items():
        if not is_ip(source):
            continue  # only consider IPs

        total = data["total_events"]
        if total == 0:
            continue

        max_event = max(data["event_distribution"].values())
        dominance_list.append(max_event / total)

    avg_dominance = sum(dominance_list) / len(dominance_list) if dominance_list else 0

    #Detection loop
    for source, data in summary.items():
        #Ignore system components
        if not is_ip(source):
            continue

        total = data["total_events"]
        distribution = data["event_distribution"]

        # Ignore low activity
        if total < MIN_EVENTS:
            continue

        reasons = []

        #Rule 1: High activity
        is_high_activity = total > HIGH_ACTIVITY_THRESHOLD
        if is_high_activity:
            reasons.append("High activity")

        #Behavior analysis
        max_event = max(distribution.values())
        dominance = max_event / total

        if is_high_activity and dominance > 0.95:
            reasons.append("Highly repetitive behavior")

        if is_high_activity and dominance > (avg_dominance + 0.1):
            reasons.append("Behavior deviation")

        #Final decision
        if reasons:
            suspicious.append({
                "source": source,
                "total_events": total,
                "reasons": reasons,
                "dominance": round(dominance, 3)
            })

    return suspicious