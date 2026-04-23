def normalize_pcap(pkt):
    """
    Normalize a single packet into common schema
    """

    try:
        return {
            "timestamp": pkt["timestamp"],
            "source": pkt["src_ip"],
            "event": f"{pkt['protocol']} connection" if pkt["protocol"] else "network activity",
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