from battery_monitor import BatteryMonitor
from task_manager import TaskManager
import time

class GreenScheduler:
    def __init__(self):
        self.battery_monitor = BatteryMonitor()
        self.task_manager = TaskManager()
        self.running = False
        print("Green scheduler initialized")

    def add_task(self, name, function, priority="low", energy_cost="low"):
        return self.task_manager.add_task(name, function, priority, energy_cost)

    def should_run_heavy_tasks(self):
        info = self.battery_monitor.get_battery_info()
        if info is None:
            return True 
        return info['charging'] or info['percent'] > 50

    def execute_with_energy_awareness(self):
        print("-" * 50)
        print("Analyzing energy state")
        print("-" * 50)
        
        self.battery_monitor.print_status()
        info = self.battery_monitor.get_battery_info()
        
        high_priority = self.task_manager.get_high_priority_tasks()
        low_energy = self.task_manager.get_low_energy_tasks()
        heavy_tasks = self.task_manager.get_heavy_tasks()
        all_pending = self.task_manager.get_pending_tasks()

        print(f"Pending: {len(all_pending)}")
        print(f"High Priority: {len(high_priority)}")
        print(f"Low Energy: {len(low_energy)}")

        if info is None or self.should_run_heavy_tasks():
            if info is None:
                print("Energy state: Unknown (Defaulting to full execution)")
            else:
                print("Energy state: Good")
            
            if all_pending:
                self.task_manager.batch_execute(all_pending)
            else:
                print("No pending tasks")

        elif self.battery_monitor.should_save_energy():
            print("Energy state: Critical")
            if high_priority:
                self.task_manager.batch_execute(high_priority)
            
            remaining_low = [t for t in self.task_manager.get_low_energy_tasks() if not t.completed]
            if remaining_low:
                self.task_manager.batch_execute(remaining_low)

        else:
            print("Energy state: Moderate")
            tasks_to_run = list(set(high_priority + low_energy))
            if tasks_to_run:
                self.task_manager.batch_execute(tasks_to_run)
            else:
                print("No suitable tasks")

        print("-" * 50)
        self.task_manager.print_status()

    def run_continuous(self, interval=10):
        self.running = True
        print(f"Starting scheduler (interval: {interval}s)")
        try:
            while self.running:
                self.execute_with_energy_awareness()
                print(f"Waiting {interval}s...")
                time.sleep(interval)
        except KeyboardInterrupt:
            self.running = False
            print("Scheduler stopped")

if __name__ == "__main__":
    scheduler = GreenScheduler()
    
    def task_a():
        time.sleep(0.5)
        return "Task A Success"
        
    def task_b():
        time.sleep(1)
        return "Task B Success"

    scheduler.add_task("Urgent Update", task_a, priority="high", energy_cost="low")
    scheduler.add_task("Heavy Backup", task_b, priority="low", energy_cost="high")
    
    print("Running single cycle test")
    scheduler.execute_with_energy_awareness()
        
