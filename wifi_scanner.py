import subprocess
import re

#my specific wifi, try not to push my wifi to github lol
TARGET_SSID = "MyAltice 0cd4a1"


def scan_wifi():
    """
    Scans nearby WiFi networks using 'iw' and returns a list of dicts:
    [{'ssid': ..., 'bssid': ..., 'rssi': ...}, ...]
    """
    try:
        result = subprocess.check_output(
            ["sudo", "iw", "dev", "wlan0", "scan"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8")

        networks = []
        current = {}

        for line in result.split("\n"):
            line = line.strip()

            # New network block
            if line.startswith("BSS"):
                if current:
                    networks.append(current)
                    current = {}

                # Extract BSSID
                current["bssid"] = line.split("(")[0].replace("BSS", "").strip()

            # SSID
            elif "SSID:" in line:
                current["ssid"] = line.split("SSID:")[1].strip()

            # Signal strength
            elif "signal:" in line:
                match = re.search(r"-\d+\.\d+", line)
                if match:
                    current["rssi"] = float(match.group())

        # Add last network
        if current:
            networks.append(current)

        return networks

    except Exception as e:
        print(f"[WiFi Scanner] Scan failed: {e}")
        return []


def get_target_rssi(networks):
    """
    Returns RSSI of the target SSID.
    If not found, returns None.
    """
    for net in networks:
        if net.get("ssid") == TARGET_SSID:
            return net.get("rssi")
    return None


def get_strongest_network(networks):
    """
    Returns the network with the strongest signal.
    """
    if not networks:
        return None
    return max(networks, key=lambda x: x.get("rssi", -100))


def debug_print(networks):
    """
    Prints all scanned networks (for debugging).
    """
    print("\n--- WiFi Networks ---")
    for net in networks:
        print(net)
    print("---------------------\n")
