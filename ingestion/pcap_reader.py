import pyshark


def read_pcap(file_path):
    """
    Reads PCAP file and extracts basic packet info
    """

    capture = pyshark.FileCapture(
        file_path,
        keep_packets=False
    )

    packets = []

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

            timestamp = float(pkt.sniff_timestamp)
            length = int(pkt.length)

            protocol = pkt.transport_layer if hasattr(pkt, 'transport_layer') else None

            src_port = None
            dst_port = None

            if protocol:
                try:
                    layer = pkt[protocol]
                    src_port = int(layer.srcport) if hasattr(layer, 'srcport') else None
                    dst_port = int(layer.dstport) if hasattr(layer, 'dstport') else None
                except:
                    pass

            packets.append({
                "timestamp": timestamp,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "protocol": protocol,
                "length": length,
                "src_port": src_port,
                "dst_port": dst_port
            })

        except:
            continue

    capture.close()

    return packets