import psutil
import time

class BatteryMonitor:
    def __init__(self):
        pass
        
    def get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                print("Error: OS does not provide battery sensors")
                return None
            
            return {
                "percent": battery.percent,
                "charging": battery.power_plugged,
                "available": True,
                "time_left": battery.secsleft if battery.secsleft > 0 else None,
            }
        except PermissionError:
            print("Error: Permission denied accessing battery path")
            return None
        except Exception as e:
            print(f"Error: Unexpected battery error - {e}")
            return None

    def is_low_battery(self, threshold=15):
        info = self.get_battery_info()
        if info is None:
            return False
        return info["percent"] < threshold
        
    def should_save_energy(self):
        info = self.get_battery_info()
        if info is None or not info["available"]:
            return False
        return info["percent"] < 20 and not info["charging"]
                            
    def print_status(self):
        info = self.get_battery_info()
        if info is None:
            print("Status: Battery information unavailable due to system errors")
        else:
            print(f"Battery: {info['percent']}% | Charging: {info['charging']}")

if __name__ == "__main__":
    monitor = BatteryMonitor()
    monitor.print_status()
			
