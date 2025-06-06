import json
from datetime import datetime, timedelta


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
        self.due_date = due_date  
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
    def __str__(self):
        """Повертає форматований рядок для відображення завдання."""
        status = "Completed" if self.completed else "Pending"
        return f"{self.title:<20} {self.due_date:<12} {self.priority:<8} {status:<10} {self.description[:25]:<27}..." if len(self.description) > 25 else f"{self.description:<30}"
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks(TASKS_FILE) 

    def add_task(self):
        title = input("Enter task title: ").strip()
        while not title:
            title = input("Error: Title cannot be empty. Please enter task title: ").strip()

        description = input("Enter task description: ").strip()

        while True:
            due_date = input("Enter task due date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")

        while True:
            try:
                priority = int(input(f"Enter task priority ({PRIORITY_MIN}-{PRIORITY_MAX}): ").strip())
                if PRIORITY_MIN <= priority <= PRIORITY_MAX:
                    break
                else:
                    print(f"Error: Priority must be between {PRIORITY_MIN} and {PRIORITY_MAX}.")
            except ValueError:
                print("Error: Please enter a valid number for priority.")

        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        print("Task added successfully!")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print(f"{'Index':<6} {'Title':<20} {'Due Date':<12} {'Priority':<8} {'Status':<10} {'Description (partial)':<30}")
        print("=" * 87) # Збільшуємо ширину роздільника
        for idx, task in enumerate(self.tasks, 1):
            print(f"{idx:<6} {task}") 

    def mark_task_as_completed(self):
        self.list_tasks()
        if not self.tasks: # Додано перевірку, якщо немає завдань для позначки
            return
        try:
            index = int(input("Enter the task index to mark as completed: ")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].completed = True
                print(f"Task '{self.tasks[index].title}' marked as completed.")
            else:
                print("Error: Invalid task index.")
        except ValueError:
            print("Error: Please enter a valid number.")

    def save_tasks(self, filename=TASKS_FILE):
        """Зберігає список завдань у JSON-файл."""
        data_to_save = [task.to_dict() for task in self.tasks]
        try:
            with open(filename, 'w', encoding='utf-8') as f: # Додано encoding='utf-8'
                json.dump(data_to_save, f, indent=4) # indent=4 для красивого форматування JSON
            print(f"Tasks saved to {filename}")
        except IOError as e:
            print(f"Error saving tasks to {filename}: {e}")

    def load_tasks(self, filename=TASKS_FILE):
        """Завантажує список завдань з JSON-файлу."""
        try:
            with open(filename, 'r', encoding='utf-8') as f: # Додано encoding='utf-8'
                data = json.load(f)
                self.tasks = [Task(**item) for item in data] # **item розпаковує словник в аргументи конструктора
            print(f"Tasks loaded from {filename}")
        except FileNotFoundError:
            print(f"No save file '{filename}' found. Starting with empty tasks.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {filename}: {e}. File might be corrupted.")
            self.tasks = [] # Очищаємо список, якщо файл пошкоджений
        except Exception as e:
            print(f"An unexpected error occurred while loading tasks from {filename}: {e}")
            self.tasks = []

    def remove_task(self):
        self.list_tasks()
        if not self.tasks:
            return

        try:
            index = int(input("Enter the task index to remove: ")) - 1
            if 0 <= index < len(self.tasks):
                removed_task = self.tasks.pop(index)
                print(f"Task '{removed_task.title}' removed successfully.")
            else:
                print("Error: Invalid task index.")
        except ValueError:
            print("Error: Please enter a valid number.")

    def update_task(self):
        self.list_tasks()
        if not self.tasks:
            return

        try:
            index = int(input("Enter the task index to update: ")) - 1
            if not (0 <= index < len(self.tasks)):
                print("Error: Invalid task index.")
                return

            task_to_update = self.tasks[index]
            print(f"Currently updating task: '{task_to_update.title}'")
            print("Leave field empty to keep current value.")

            new_title = input(f"Enter new title (current: {task_to_update.title}): ").strip()
            if new_title:
                task_to_update.title = new_title

            new_description = input(f"Enter new description (current: {task_to_update.description}): ").strip()
            if new_description:
                task_to_update.description = new_description

            while True:
                new_due_date = input(f"Enter new due date (YYYY-MM-DD, current: {task_to_update.due_date}): ").strip()
                if not new_due_date:
                    break 
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    task_to_update.due_date = new_due_date
                    break
                except ValueError:
                    print("Error: Invalid date format. Please use YYYY-MM-DD.")

            while True:
                new_priority_str = input(f"Enter new priority ({PRIORITY_MIN}-{PRIORITY_MAX}, current: {task_to_update.priority}): ").strip()
                if not new_priority_str:
                    break 
                try:
                    new_priority = int(new_priority_str)
                    if PRIORITY_MIN <= new_priority <= PRIORITY_MAX:
                        task_to_update.priority = new_priority
                        break
                    else:
                        print(f"Error: Priority must be between {PRIORITY_MIN} and {PRIORITY_MAX}.")
                except ValueError:
                    print("Error: Please enter a valid number for priority.")

            print(f"Task '{task_to_update.title}' updated successfully.")

        except ValueError:
            print("Error: Please enter a valid number for the index.")

    def search_task(self):
        search_term = input("Enter keyword to search for (title or description): ").strip().lower()
        if not search_term:
            print("Search term cannot be empty.")
            return

        found_tasks = []
        for task in self.tasks:
            if search_term in task.title.lower() or search_term in task.description.lower():
                found_tasks.append(task)

        if not found_tasks:
            print(f"No tasks found matching '{search_term}'.")
            return

        print("\n--- Found Tasks ---")
        print(f"{'Index':<6} {'Title':<20} {'Due Date':<12} {'Priority':<8} {'Status':<10} {'Description (partial)':<30}")
        print("=" * 87)
        for idx, task in enumerate(found_tasks, 1):
            print(f"{idx:<6} {task}") # Використовуємо __str__ метод Task

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
        if not self.tasks:
            print("No tasks to sort.")
            return

        print("\nSort Tasks By:")
        print("1. Title")
        print("2. Due Date")
        print("3. Priority")
        print("4. Status (Completed First)")
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
            elif choice == 4:
                self.tasks.sort(key=lambda task: (not task.completed, task.title.lower())) # completed=False (Pending) йдуть першими
                print("Tasks sorted by status (completed tasks at the end).")
            else:
                print("Invalid choice. Sorting canceled.")
        except ValueError:
            print("Error: Please enter a valid number.")


def display_menu():
    print("\n--- Task Manager Menu ---")
   
    print(f"{MENU_OPTION_ADD}. Add Task")
    print(f"{MENU_OPTION_LIST}. List Tasks")
    print(f"{MENU_OPTION_REMOVE}. Remove Task")
    print(f"{MENU_OPTION_UPDATE}. Update Task")
    print(f"{MENU_OPTION_SEARCH}. Search Task")
    print(f"{MENU_OPTION_MARK_COMPLETED}. Mark Task as Completed")
    print(f"{MENU_OPTION_CHECK_DEADLINES}. Check Deadlines")
    print(f"{MENU_OPTION_SORT}. Sort Tasks")
    print(f"{MENU_OPTION_SAVE}. Save Tasks")
    print(f"{MENU_OPTION_LOAD}. Load Tasks")
    print(f"{MENU_OPTION_EXIT}. Exit")


def main():
    manager = TaskManager()
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == MENU_OPTION_ADD:
                manager.add_task()
            elif choice == MENU_OPTION_LIST:
                manager.list_tasks()
            elif choice == MENU_OPTION_REMOVE:
                manager.remove_task()
            elif choice == MENU_OPTION_UPDATE:
                manager.update_task()
            elif choice == MENU_OPTION_SEARCH:
                manager.search_task()
            elif choice == MENU_OPTION_MARK_COMPLETED:
                manager.mark_task_as_completed()
            elif choice == MENU_OPTION_CHECK_DEADLINES:
                manager.check_deadlines()
            elif choice == MENU_OPTION_SORT:
                manager.sort_tasks()
            elif choice == MENU_OPTION_SAVE:
                manager.save_tasks()
            elif choice == MENU_OPTION_LOAD:
                manager.load_tasks()
            elif choice == MENU_OPTION_EXIT:
                manager.save_tasks() 
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Error: Invalid choice. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number.")


if __name__ == "__main__":
    main()