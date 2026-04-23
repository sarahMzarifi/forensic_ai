def normalize_log(log):
    """
    Convert parsed log into common schema
    """

    return {
        "timestamp": log["timestamp"],
        "source": log["component"],  # who generated it
        "event": log["message"],     # what happened
        "metadata": {
            "level": log["level"],
            "pid": log["pid"]
        }
    }