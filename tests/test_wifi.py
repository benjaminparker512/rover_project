import sys
import os

# 1. Add the parent directory (rover_project) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Correct the import (No '.py' and only import what you need)
from wifi_scanner import scan_wifi, get_target_rssi, debug_print

nets = scan_wifi()

debug_print(nets)

rssi = get_target_rssi(nets)
print("Target RSSI:", rssi)
