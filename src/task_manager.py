from datetime import datetime
import time


class Task:
    def __init__(self, name, function, priority="low", energy_cost="low"):
        self.name = name
        self.function = function
        self.priority = priority
        self.energy_cost = energy_cost
        self.created_at = datetime.now()
        self.completed = False
        self.result = None

    def execute(self):
        try:
            print(f"⚙️  Executing: {self.name}")
            start_time = time.time()
            self.result = self.function()
            end_time = time.time()
            duration = end_time - start_time

            self.completed = True
            print(f"✅ Completed: {self.name} (took {duration:.2f}s)")
            return True

        except Exception as e:
            print(f"❌ Error in {self.name}: {e}")
            return False

    def __str__(self):
        status = "✓Done" if self.completed else "Pending..."
        return f"[{status}] {self.name} | Priority: {self.priority} | Energy: {self.energy_cost}"


class TaskManager:
    def __init__(self):
        self.tasks = []
        print("Task scheduler initiated!")

    def add_task(self, name, function, priority="low", energy_cost="low")
        task = Task(name, function, priority, energy_cost)
        self.tasks.append(task)
        print(f"Added task: {task.name}")
        return task

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def get_high_priority_tasks(self):
        return [task for task in self.get_pending_tasks() if task.priority == "high"]

    def get_low_energy_tasks(self):
        return [task for task in self.get_pending_tasks() if task.energy_cost == "low"]

    def get_heavy_tasks(self):
        return [task for task in self.get_pending_tasks() if task.energy_cost == "high"]

    def execute_task(self, task):
        return task.execute()

    def batch_execute(self, task_list):
        print(f"\n🔄 Batch executing {len(task_list)} tasks...")
        successful = 0

        for task in task_list:
            if self.execute_task(task):
                successful += 1
            time.sleep(0.5)

        print(f"✅ Batch complete: {successful}/{len(task_list)} successful\n")
        return successful

    def print_status(self):
        pending = self.get_pending_tasks()
        completed = [task for task in self.tasks if task.completed]

        print("\n📊 Task Manager Status:")
        print(f"  Total tasks: {len(self.tasks)}")
        print(f"  Completed: {len(completed)}")
        print(f"  Pending: {len(pending)}")

        if pending:
            print("\n Pending tasks:")
            for task in pending:
                print(f"  - {task}")

        if completed:
            print("\n Completed tasks:")
            for task in completed:
                print(f"  - {task}") 


#demo
if __name__ == "__main__":
    print("=" * 50)
    print("📋 🟢 GreenMode Task Manager Test")
    print("=" * 50)

    manager = TaskManager()

    def quick_task():
        time.sleep(0.5)
        return "Quick task done!"

    def medium_task():
        time.sleep(1)
        return "Medium task done!"

    def heavy_task():
        time.sleep(2)
        return "Heavy task done!"

    manager.add_task("Check messages", quick_task, priority="high", energy_cost="low")
    manager.add_task("Upload photo", heavy_task, priority="medium", energy_cost="high")
    manager.add_task("Sync notes", medium_task, priority="low", energy_cost="medium")
    manager.add_task("Emergency backup", heavy_task, priority="high", energy_cost="high")

    print("\n--- Initial Status ---")
    manager.print_status()

    print("\n--- Executing High Priority Tasks ---")
    manager.batch_execute(manager.get_high_priority_tasks())

    print("\n--- Executing Low Energy Tasks ---")
    manager.batch_execute(manager.get_low_energy_tasks())

    print("\n--- Final Status ---")
    manager.print_status()

    print("\n" + "=" * 50)
    print("✅ Test complete!")
    print("=" * 50)
