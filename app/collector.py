
import time
from pathlib import Path

from app.database import initialize_database, save_alert
from app.parser import parse_alert

LOG_FILE = Path("/var/log/suricata/eve.json")


def monitor_alerts():
    initialize_database()

    print("[SYNTRA] Intrusion Detection Monitor Started")
    print("[SYNTRA] Waiting for new security alerts...")

    with LOG_FILE.open("r", encoding="utf-8") as file:
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line:
                time.sleep(0.5)
                continue

            alert = parse_alert(line)

            if alert:
                save_alert(alert)

                print(
                    f"[ALERT] {alert['signature']} | "
                    f"{alert['source_ip']} -> "
                    f"{alert['destination_ip']}"
                )


if __name__ == "__main__":
    try:
        monitor_alerts()
    except KeyboardInterrupt:
        print("\n[SYNTRA] Monitoring stopped.")

