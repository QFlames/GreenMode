import psutil
import time
class BatteryMonitor:
	def __init__(self):
		print("Battery monitor started")
		
	def get_battery_info(self):
		try:
			battery = psutil.sensors_battery()
			if battery is None:
				return {
                    "percent": 100,
                    "charging": True,
                    "available": False,
                    "time_left": None,
                }
				return{
				    'percent': battery.percent,
				    'charging': battery.power_plugged,
				    'available':True,
				    'Time left': battery.secsleft if battery.secsleft  > 0 else None,
				}
		
		except Exception as e:
				    print(f"❌ Error reading battery: {e}")
				    return None

	def is_low_battery(self, threshold=15):
	       info = self.get_battery_info()
	       if info is None:
	       	return False
	       	return info["percent"] < threshold
        
	def should_save_energy(self):
				    info = self.get_battery_info()
				    if info is None:
				    	return False
				    low_battery = info["percent"] < threshold
				    not_charging = not info["charging"]
				    return low_battery and not_charging
				    			
	def print_status(self):
				    			    info = self.get_battery_info()
				    			    if info is None:
				    			    	print("cannot read battery info")
				    			    	return
				    			    
				    			    if not info["available"]:
				    			    	print("No battery detected (desktop mode)")
				    			    	return
				    			    	
				    			    percent = info["percent"]
				    			    bars = int(percent/10)
				    			    battery_bar = "█" * bars + "░" * (10 - bars)
				    			    charging_symbol = "⚡" if info['charging'] else "🔋"
				    			    print(f"\n{charging_symbol} Battery Status:")
				    			    print(f"  [{battery_bar}] {percent}%")
				    			    print(f"  Charging: {'Yes ⚡' if info['charging'] else 'No'}")
				    			    
				    			    if info["Time left"]:
				    			    	hours = info["Time left"] // 3600
				    			    	minutes = (info[" Time left"] % 3600) // 60
				    			    	print(f"Time left: {hours}h {minutes}m")
				    			    	
				    			    if self.should_save_energy():
				    			    	print("  💡 Recommendation: SAVE ENERGY!")
				    			    elif info['charging']:
				    			    	print("  💡 Recommendation: Good time for heavy tasks")
				    			    else:
				    			    	print("  💡 Recommendation: Normal operation")
				    			 
