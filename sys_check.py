import os
import subprocess

def get_pi_stats():
    # 1. Check Temperature
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = int(f.read()) / 1000
    
    # 2. Check Throttling (Voltage/Heat issues)
    # 0x0 means everything is perfect. 
    # Anything else means your MacBook charger or battery is struggling.
    throttled = subprocess.check_output(['vcgencmd', 'get_throttled']).decode('utf-8').strip()
    
    # 3. Check for the Active Cooler
    fan_speed = "Unknown"
    if os.path.exists("/sys/class/thermal/cooling_device0/cur_state"):
        with open("/sys/class/thermal/cooling_device0/cur_state", "r") as f:
            fan_speed = f.read().strip()

    print(f"\n--- Rover System Health ---")
    print(f"CPU Temp:   {temp:.1f}°C")
    print(f"Fan State:  {fan_speed} (0=off, 1-4=spinning)")
    print(f"Voltage:    {throttled}")
    print(f"---------------------------\n")

if __name__ == "__main__":
    get_pi_stats()