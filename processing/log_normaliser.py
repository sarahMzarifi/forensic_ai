def normalize_log(log):
    """
    Convert parsed log into common schema
    """

    try:
        return {
            "timestamp": log["timestamp"],
            "source": log["component"],  # who generated it
            "event": log["message"],     # what happened
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