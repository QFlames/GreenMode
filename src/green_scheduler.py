from battery_monitor import BatteryMonitor
from task_manager import TaskManager
import time


class GreenScheduler:
    def __init__(self):
        self.battery_monitor = BatteryMonitor()
        self.task_manager = TaskManager()
        self.running = False
        print("Green scheduler initialized!")  

    def add_task(self, name, function, priority="low", energy_cost="low"):
        return self.task_manager.add_task(name, function, priority, energy_cost)

    def should_run_heavy_tasks(self):
        battery_info = self.battery_monitor.get_battery_info()
        if battery_info is None:
            return False
        return battery_info["charging"] or battery_info["percent"] > 50

    def execute_with_energy_awareness(self):
        print("\n" + "=" * 50)
        print("Analysing energy state...")
        print("=" * 50)

        self.battery_monitor.print_status()

        high_priority = self.task_manager.get_high_priority_tasks()
        low_energy = self.task_manager.get_low_energy_tasks()
        heavy_tasks = self.task_manager.get_heavy_tasks()
        all_pending = self.task_manager.get_pending_tasks()

        print(f"\n📊 Task Analysis:")
        print(f"  Total pending: {len(all_pending)}")
        print(f"  High priority: {len(high_priority)}")
        print(f"  Low energy: {len(low_energy)}")
        print(f"  Heavy tasks: {len(heavy_tasks)}")

        if self.should_run_heavy_tasks():
            print("\n✅ Energy state: GOOD")
            print("💡 Strategy: Execute all pending tasks")
            if all_pending:
                self.task_manager.batch_execute(all_pending)
            else:
                print("ℹ️ No pending tasks to execute")

        elif self.battery_monitor.should_save_energy():
            print("\n⚠️ Energy state: CRITICAL")
            print("💡 Strategy: Only high-priority and low-energy tasks")

            if high_priority:
                print("\n🚨 Executing high-priority tasks:")
                self.task_manager.batch_execute(high_priority)

            remaining_low_energy = [t for t in low_energy if not t.completed]
            if remaining_low_energy:
                print("\n🔋 Executing low-energy tasks:")
                self.task_manager.batch_execute(remaining_low_energy)

            deferred = [t for t in heavy_tasks if not t.completed and t.priority != "high"]
            if deferred:
                print(f"\n⏸️ Deferred {len(deferred)} heavy tasks")

        else:
            print("\n🟡 Energy state: MODERATE")
            print("💡 Strategy: High-priority and low-energy tasks only")

            tasks_to_run = []
            tasks_to_run.extend(high_priority)

            for task in low_energy:
                if task not in tasks_to_run:
                    tasks_to_run.append(task)

            if tasks_to_run:
                self.task_manager.batch_execute(tasks_to_run)
            else:
                print("ℹ️ No suitable tasks for current conditions")

        print("\n" + "=" * 50)
        self.task_manager.print_status()
        print("=" * 50)

    def run_continuous(self, check_interval=30):
        self.running = True
        print(f"\n🚀 Starting continuous scheduler (every {check_interval}s)")
        print("Press Ctrl+C to stop\n")

        try:
            while self.running:
                self.execute_with_energy_awareness()
                print(f"\n⏰ Waiting {check_interval} seconds...")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n⏹️ Scheduler stopped by user")
            self.running = False

#demo
if __name__ == "__main__":
    print("=" * 60)
    print("🟢 GreenMode Scheduler Test")
    print("=" * 60)

    scheduler = GreenScheduler()

    def send_message():
        time.sleep(0.3)
        print("📱 Message sent!")
        return "success"

    def backup_photos():
        time.sleep(2)
        print("📸 Photos backed up!")
        return "success"

    def sync_large_file():
        time.sleep(3)
        print("📁 File synced!")
        return "success"

    def check_updates():
        time.sleep(0.5)
        print("🔄 Updates checked!")
        return "success"

    def compress_video():
        time.sleep(4)
        print("🎥 Video compressed!")
        return "success"

    print("\n➕ Adding tasks...\n")

    scheduler.add_task("Send urgent message", send_message, "high", "low")
    scheduler.add_task("Check for updates", check_updates, "low", "low")
    scheduler.add_task("Backup photos", backup_photos, "medium", "high")
    scheduler.add_task("Sync large file", sync_large_file, "low", "high")
    scheduler.add_task("Compress video", compress_video, "medium", "high")

    print("\n🎯 Running one scheduling cycle...")
    scheduler.execute_with_energy_awareness()

    print("\n" + "=" * 60)
    print("✅ Test complete!")
    print("💡 Tip: Call scheduler.run_continuous() to run continuously")
    print("=" * 60)
