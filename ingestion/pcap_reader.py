import pyshark


def read_pcap(file_path):
    """
    Generator function to read PCAP file and extract packet info
    """

    capture = pyshark.FileCapture(
        file_path,
        keep_packets=False
    )

    try:
        for pkt in capture:
            try:
                # Handle IPv4 / IPv6
                if hasattr(pkt, 'ip'):
                    src_ip = pkt.ip.src
                    dst_ip = pkt.ip.dst
                elif hasattr(pkt, 'ipv6'):
                    src_ip = pkt.ipv6.src
                    dst_ip = pkt.ipv6.dst
                else:
                    continue

                # Extract timestamp and length
                timestamp = float(pkt.sniff_timestamp)
                length = int(pkt.length)

                # Extract protocol
                protocol = pkt.transport_layer if hasattr(pkt, 'transport_layer') else None

                src_port = None
                dst_port = None

                # Extract ports safely
                if protocol:
                    try:
                        layer = pkt[protocol]
                        src_port = int(layer.srcport) if hasattr(layer, 'srcport') else None
                        dst_port = int(layer.dstport) if hasattr(layer, 'dstport') else None
                    except Exception as e:
                        print(f"[Port Extraction Error] {e}")

                # Yield instead of storing
                yield {
                    "timestamp": timestamp,
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "protocol": protocol,
                    "length": length,
                    "src_port": src_port,
                    "dst_port": dst_port
                }

            except Exception as e:
                print(f"[Packet Error] {e}")

    finally:
        capture.close()