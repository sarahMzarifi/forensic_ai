from ingestion.log_reader import read_logs
from ingestion.pcap_reader import read_pcap

from processing.log_normaliser import normalize_logs
from processing.pcap_normaliser import normalize_pcaps


# LOG PIPELINE

def log_pipeline(log_file_path):
    """
    Stream normalized log events
    """

    logs = read_logs(log_file_path)
    normalized_logs = normalize_logs(logs)

    for event in normalized_logs:
        yield event



# PCAP PIPELINE

def pcap_pipeline(pcap_file_path):
    """
    Stream normalized packet events
    """

    packets = read_pcap(pcap_file_path)
    normalized_packets = normalize_pcaps(packets)

    for event in normalized_packets:
        yield event


# UNIFIED PIPELINE

def unified_pipeline(log_file_path=None, pcap_file_path=None):
    """
    Combine logs and pcap into one unified stream
    """

    # Process logs
    if log_file_path:
        for event in log_pipeline(log_file_path):
            yield event

    # Process PCAP
    if pcap_file_path:
        for event in pcap_pipeline(pcap_file_path):
            yield event