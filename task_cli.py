import sys
import json
import os
from datetime import datetime
from tabulate import tabulate

# Define the path for storing tasks
DATABASE_PATH = 'tasks.json'


# Load tasks from the database (tasks.json)
def load_database(path: str):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return {}


# Save tasks to the database (tasks.json)
def save_database(database: dict, path: str):
    with open(path, 'w') as file:
        json.dump(database, file, indent=4)


# Get supported queries and commands
def get_supported_queries():
    return {
        "add": {
            "args": 1,
            "func": add_task,
            "desc": "Add a new task."
        },
        "update": {
            "args": 2,
            "func": update_task,
            "desc": "Update an existing task."
        },
        "delete": {
            "args": 1,
            "func": delete_task,
            "desc": "Delete a task."
        },
        "list": {
            "args": 0,
            "func": list_tasks,
            "desc": "List all tasks."
        },
        "mark-in-progress": {
            "args": 1,
            "func": mark_in_progress_task,
            "desc": "Mark a task as in-progress."
        },
        "mark-done": {
            "args": 1,
            "func": mark_done_task,
            "desc": "Mark a task as done."
        },
        "clear-tasks": {
            "args": (0, 1),  # allow 0 or 1 argument (optional --force)
            "func": clear_tasks,
            "desc": "Clear all tasks (use --force to skip confirmation)."
        },
    }


# Parse the arguments and return the corresponding function and arguments
def get_query_function_and_args(supported_queries: dict):
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        sys.exit(1)

    query = sys.argv[1]
    if query not in supported_queries:
        print(f"Unknown command: {query}")
        sys.exit(1)

    args_count = len(sys.argv) - 2
    expected_args = supported_queries[query]["args"]

    # Handle flexible number of args (for clear-tasks)
    if isinstance(expected_args, tuple):
        if args_count not in expected_args:
            print(f"Invalid number of arguments for '{query}'")
            print(f"Usage: {query} {supported_queries[query]['desc']}")
            sys.exit(1)
    else:
        if args_count != expected_args:
            print(f"Invalid number of arguments for '{query}'")
            print(f"Usage: {query} {supported_queries[query]['desc']}")
            sys.exit(1)

    return supported_queries[query]["func"], sys.argv[2:]


# Add a new task to the database
def add_task(database: dict, description: str):
    task_id = str(len(database) + 1)
    created_at = updated_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": created_at,
        "updatedAt": updated_at,
    }
    database[task_id] = task
    save_database(database, DATABASE_PATH)
    print(f"Task added: {task['description']}")
    print_task_table([task])


# Update an existing task in the database
def update_task(database: dict, task_id: str, new_description: str):
    if task_id not in database:
        print(f"Task with ID {task_id} not found!")
        sys.exit(1)

    task = database[task_id]
    task["description"] = new_description
    task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    save_database(database, DATABASE_PATH)
    print(f"Task updated: {task['description']}")
    print_task_table([task])


# Delete a task from the database
def delete_task(database: dict, task_id: str):
    if task_id not in database:
        print(f"Task with ID {task_id} not found!")
        sys.exit(1)

    del database[task_id]
    save_database(database, DATABASE_PATH)
    print(f"Task with ID {task_id} deleted.")


# List all tasks, optionally filtering by status
def list_tasks(database: dict, status: str = 'all'):
    if status != 'all' and status not in ['todo', 'in-progress', 'done']:
        print("Invalid status filter. Use 'all', 'todo', 'in-progress', or 'done'.")
        sys.exit(1)

    tasks = [task for task in database.values() if status == 'all' or task['status'] == status]
    print_task_table(tasks)


# Mark a task as in-progress
def mark_in_progress_task(database: dict, task_id: str):
    if task_id not in database:
        print(f"Task with ID {task_id} not found!")
        sys.exit(1)

    task = database[task_id]
    task["status"] = "in-progress"
    task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    save_database(database, DATABASE_PATH)
    print(f"Task with ID {task_id} marked as in-progress.")
    print_task_table([task])


# Mark a task as done
def mark_done_task(database: dict, task_id: str):
    if task_id not in database:
        print(f"Task with ID {task_id} not found!")
        sys.exit(1)

    task = database[task_id]
    task["status"] = "done"
    task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    save_database(database, DATABASE_PATH)
    print(f"Task with ID {task_id} marked as done.")
    print_task_table([task])


# Clear all tasks from the database
def clear_tasks(database: dict, *args):
    force = False
    if args and args[0] == '--force':
        force = True

    if not force:
        confirmation = input("Are you sure you want to delete all tasks? (yes/no): ")
        if confirmation.lower() != "yes":
            print("Clear operation cancelled.")
            return

    database.clear()
    save_database(database, DATABASE_PATH)
    print("All tasks cleared.")


# Helper function to display tasks in a formatted table
def print_task_table(tasks):
    if tasks:
        headers = ["Id", "Description", "Status", "Created At", "Updated At"]
        table = [(task["id"], task["description"], task["status"], task["createdAt"], task["updatedAt"]) for task in tasks]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    else:
        print("No tasks to display.")


# Main function to run the task tracker
def main():
    supported_queries = get_supported_queries()
    func, args = get_query_function_and_args(supported_queries)
    database = load_database(DATABASE_PATH)

    func(database, *args)


if __name__ == "__main__":
    main()
