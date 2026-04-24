def extract_size_category(length):
    """
    Categorize packet size
    """

    if length < 100:
        return "small"
    elif length < 500:
        return "medium"
    else:
        return "large"


def extract_time_bucket(timestamp):
    """
    Extract hour bucket from UNIX timestamp
    """

    try:
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%H")
    except:
        return None


def normalize_pcap(pkt):
    """
    Normalize a single packet into enriched schema
    """

    try:
        protocol = pkt.get("protocol")

        return {
            "timestamp": pkt["timestamp"],
            "source": pkt["src_ip"],
            "event": f"{protocol} connection" if protocol else "network activity",

            # 🔥 NEW FEATURES
            "event_type": "connection" if protocol else "network_activity",
            "entity_type": "ip",
            "time_bucket": extract_time_bucket(pkt["timestamp"]),
            "size_category": extract_size_category(pkt["length"]),

            "metadata": {
                "destination": pkt["dst_ip"],
                "src_port": pkt["src_port"],
                "dst_port": pkt["dst_port"],
                "length": pkt["length"]
            }
        }

    except KeyError as e:
        print(f"[Normalization Error] Missing key: {e} | Packet: {pkt}")
        return None


def normalize_pcaps(packets):
    """
    Generator function to normalize packets
    """

    for pkt in packets:
        normalized = normalize_pcap(pkt)

        if normalized:
            yield normalized