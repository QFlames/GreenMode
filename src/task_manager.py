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
            print(f"Executing: {self.name}")
            start_time = time.time()
            self.result = self.function()
            end_time = time.time()
            duration = end_time - start_time
            self.completed = True
            print(f"Completed: {self.name} (took {duration:.2f}s)")
            return True
        except Exception as e:
            print(f"Error in {self.name}: {e}")
            return False
    
    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status:^8}] {self.name:<20} | Priority: {self.priority:<7} | Energy: {self.energy_cost}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        print("Task manager initiated")

    def add_task(self, name, function, priority="low", energy_cost="low"):
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
        if not task_list:
            return 0
        print(f"Batch executing {len(task_list)} tasks")
        successful = 0
        for task in task_list:
            if not task.completed:
                if self.execute_task(task):
                    successful += 1
                time.sleep(0.1)
        print(f"Batch complete: {successful}/{len(task_list)} successful")
        return successful     	 		  		       	

    def print_status(self):
        pending = self.get_pending_tasks()
        completed = [task for task in self.tasks if task.completed]
        print("TASK MANAGER STATUS")
        print("-" * 30)
        print(f"Total: {len(self.tasks)} | Completed: {len(completed)} | Pending: {len(pending)}")
        
        if pending:
            print("PENDING TASKS:")
            for task in pending:
                print(f"  - {task}")  
        
        if completed:
            print("COMPLETED TASKS:")
            for task in completed:
                print(f"  - {task}")

if __name__ == "__main__":
    def sample_work():
        time.sleep(0.2)
        return True

    manager = TaskManager()
    manager.add_task("System Update", sample_work, priority="high", energy_cost="low")
    manager.add_task("Cloud Sync", sample_work, priority="low", energy_cost="high")
    
    print("\nStarting execution test")
    high_prio = manager.get_high_priority_tasks()
    manager.batch_execute(high_prio)
    
    print("\nFinal status check")
    manager.print_status()
    
