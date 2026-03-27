import os
import subprocess
from datetime import datetime

def get_pi_stats():
    try:
        # Temperature
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000

        # Throttling
        throttled = subprocess.check_output(
            ['vcgencmd', 'get_throttled']
        ).decode('utf-8').strip()

        # Fan
        fan_speed = "Unknown"
        if os.path.exists("/sys/class/thermal/cooling_device0/cur_state"):
            with open("/sys/class/thermal/cooling_device0/cur_state", "r") as f:
                fan_speed = f.read().strip()

    except Exception:
        # Simulation 
        temp = 45.0
        throttled = "0x0"
        fan_speed = "0"

    return {
        "temp": temp,
        "throttled": throttled,
        "fan": fan_speed
    }


def print_stats(stats):
    print(f"\n--- Rover System Health ---")
    print(f"CPU Temp:   {stats['temp']:.1f}°C")
    print(f"Fan State:  {stats['fan']} (0=off, 1-4=spinning)")
    print(f"Voltage:    {stats['throttled']}")
    print(f"---------------------------\n")


def log_stats(stats):
    log_dir = "logs"
    log_file = os.path.join(log_dir, "system_health.log")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #with open(log_file, "a") as f:
    #    f.write(
    #        f"[{timestamp}] Temp: {stats['temp']}C | Voltage: {stats['throttled']}\n"
    #    )

if __name__ == "__main__":
    stats = get_pi_stats()
    print_stats(stats)
    