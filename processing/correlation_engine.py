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


def event_type_distribution(grouped):
    """
    Count and sort event types per source
    """

    result = {}

    for source, events in grouped.items():
        event_counts = {}

        for event in events:
            event_type = event.get("event_type")

            # Handle missing values safely
            if not event_type:
                event_type = "unknown"

            if event_type not in event_counts:
                event_counts[event_type] = 0

            event_counts[event_type] += 1

        # Sort by frequency (descending)
        sorted_event_counts = dict(
            sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
        )

        result[source] = sorted_event_counts

    return result