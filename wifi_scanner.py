import subprocess
import re

def scan_wifi():
    try:
        result = subprocess.check_output(
            ["sudo", "iw", "dev", "wlan0", "scan"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")

        networks = []
        current = {}

        for line in result.split("\n"):
            line = line.strip()

            if line.startswith("BSS"):
                if current:
                    networks.append(current)
                    current = {}

                current["bssid"] = line.split("(")[0].replace("BSS", "").strip()

            elif "SSID:" in line:
                current["ssid"] = line.split("SSID:")[1].strip()

            elif "signal:" in line:
                signal = re.findall(r"-\d+\.\d+", line)
                if signal:
                    current["rssi"] = float(signal[0])

        if current:
            networks.append(current)

        return networks

    except Exception as e:
        print(f"WiFi scan failed: {e}")
        return []