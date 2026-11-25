
import json


def parse_alert(line):
    try:
        event = json.loads(line)

        if event.get("event_type") != "alert":
            return None

        alert = event.get("alert", {})

        return {
            "timestamp": event.get("timestamp"),
            "source_ip": event.get("src_ip"),
            "destination_ip": event.get("dest_ip"),
            "protocol": event.get("proto"),
            "signature": alert.get("signature"),
            "severity": alert.get("severity"),
            "signature_id": alert.get("signature_id")
        }

    except (json.JSONDecodeError, TypeError):
        return None

