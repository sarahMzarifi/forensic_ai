from datetime import datetime
import re


def extract_event_type(message):
    """
    Improved rule-based event classification
    """

    msg = message.lower()

    if "received block" in msg or "receiving block" in msg:
        return "block_transfer"
    elif "packetresponder" in msg:
        return "packet_response"
    elif "addstoredblock" in msg:
        return "block_update"
    elif "error" in msg or "fail" in msg:
        return "error_event"
    else:
        return "system_event"


def extract_time_bucket(timestamp):
    """
    Extract hour bucket from ISO timestamp
    """

    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%H")
    except:
        return None


def extract_ip_from_log(message):
    """
    Extract IP address from log message (if present)
    """

    match = re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", message)
    return match.group() if match else None


def normalize_log(log):
    """
    Convert parsed log into enriched schema
    """

    try:
        timestamp = log["timestamp"]
        message = log["message"]

        extracted_ip = extract_ip_from_log(message)

        return {
            "timestamp": timestamp,
            "source": log["component"],
            "event": message,

            # 🔥 FEATURES
            "event_type": extract_event_type(message),
            "entity_type": "system",
            "time_bucket": extract_time_bucket(timestamp),
            "log_ip": extracted_ip,  # 🔥 NEW (IMPORTANT)

            "metadata": {
                "level": log["level"],
                "pid": log["pid"]
            }
        }

    except KeyError as e:
        print(f"[Normalization Error] Missing key: {e} | Log: {log}")
        return None


def normalize_logs(logs):
    """
    Generator function to normalize logs lazily
    """

    for log in logs:
        normalized = normalize_log(log)

        if normalized:
            yield normalized