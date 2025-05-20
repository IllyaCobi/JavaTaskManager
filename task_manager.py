import json
from datetime import datetime, timedelta

# Додаємо константи для опцій меню та назви файлу
TASKS_FILE = 'tasks.json'

MENU_OPTION_ADD = 1
MENU_OPTION_LIST = 2
MENU_OPTION_REMOVE = 3
MENU_OPTION_UPDATE = 4
MENU_OPTION_SEARCH = 5
MENU_OPTION_MARK_COMPLETED = 6
MENU_OPTION_CHECK_DEADLINES = 7
MENU_OPTION_SORT = 8
MENU_OPTION_SAVE = 9
MENU_OPTION_LOAD = 10
MENU_OPTION_EXIT = 11

PRIORITY_MIN = 1
PRIORITY_MAX = 5

class Task:
    def __init__(self, title, description, due_date, priority, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date  # Зберігається як рядок YYYY-MM-DD
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        """Конвертує об'єкт Task у словник для збереження в JSON."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed,
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks(TASKS_FILE) # Автоматичне завантаження при старті

    def add_task(self):
        title = input("Enter task title: ").strip()
        while not title:
            title = input("Title cannot be empty. Enter task title: ").strip()

        description = input("Enter task description: ").strip()

        while True:
            due_date = input("Enter task due date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        while True:
            try:
                priority = int(input("Enter task priority (1-5): ").strip())
                if 1 <= priority <= 5:
                    break
                else:
                    print("Priority must be between 1 and 5.")
            except ValueError:
                print("Please enter a valid number between 1 and 5.")

        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        print("Task added successfully!")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print(f"{'Index':<6} {'Title':<20} {'Due Date':<12} {'Priority':<8} {'Status':<10}")
        print("=" * 60)
        for idx, task in enumerate(self.tasks, 1):
            status = "Completed" if task.completed else "Pending"
            print(f"{idx:<6} {task.title:<20} {task.due_date:<12} {task.priority:<8} {status:<10}")

    def mark_task_as_completed(self):
        self.list_tasks()
        try:
            index = int(input("Enter the task index to mark as completed: ")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].completed = True
                print(f"Task '{self.tasks[index].title}' marked as completed.")
            else:
                print("Invalid task index.")
        except ValueError:
            print("Please enter a valid number.")

    def check_deadlines(self):
        today = datetime.now()
        print("\nTask Deadlines:")
        for task in self.tasks:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
            if due_date < today:
                print(f"🔴 Overdue: {task.title} (Due: {task.due_date})")
            elif due_date - today <= timedelta(days=3):
                print(f"🟡 Due Soon: {task.title} (Due: {task.due_date})")
        print()

    def sort_tasks(self):
        print("\nSort Tasks By:")
        print("1. Title")
        print("2. Due Date")
        print("3. Priority")
        try:
            choice = int(input("Enter your choice: ").strip())
            if choice == 1:
                self.tasks.sort(key=lambda task: task.title.lower())
                print("Tasks sorted by title.")
            elif choice == 2:
                self.tasks.sort(key=lambda task: datetime.strptime(task.due_date, "%Y-%m-%d"))
                print("Tasks sorted by due date.")
            elif choice == 3:
                self.tasks.sort(key=lambda task: task.priority)
                print("Tasks sorted by priority.")
            else:
                print("Invalid choice. Sorting canceled.")
        except ValueError:
            print("Please enter a valid number.")


def display_menu():
    print("\nTask Manager Menu:")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Remove Task")
    print("4. Update Task")
    print("5. Search Task")
    print("6. Mark Task as Completed")
    print("7. Check Deadlines")
    print("8. Sort Tasks")
    print("9. Save Tasks")
    print("10. Load Tasks")
    print("11. Exit")


def main():
    manager = TaskManager()
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                manager.add_task()
            elif choice == 2:
                manager.list_tasks()
            elif choice == 6:
                manager.mark_task_as_completed()
            elif choice == 7:
                manager.check_deadlines()
            elif choice == 8:
                manager.sort_tasks()
            elif choice == 11:
                print("Exiting Task Manager.")
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
