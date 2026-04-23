def normalize_pcap(pkt):
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