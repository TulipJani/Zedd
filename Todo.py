from chat import speak_response
import time
from colorama import Fore


TODO_FILE = "todo.txt"
def add_to_todo(task):
    with open(TODO_FILE, "a") as file:
        file.write(f"{task}\n")

def get_todo_list():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = [task.strip() for task in file.readlines()]
            pending_tasks = [task for task in tasks if not task.startswith("[Completed]")]
            completed_tasks = [task for task in tasks if task.startswith("[Completed]")]
            return pending_tasks, completed_tasks
    except FileNotFoundError:
        return [], []
    
def delete_task(task_index):
    pending_tasks, completed_tasks = get_todo_list()
    if task_index < len(pending_tasks):
        del pending_tasks[task_index]
        with open(TODO_FILE, "w") as file:
            file.write("\n".join(pending_tasks + completed_tasks))

def mark_task_completed(task_index):
    pending_tasks, completed_tasks = get_todo_list()
    if task_index < len(pending_tasks):
        completed_tasks.append(f"[Completed] {pending_tasks[task_index]}")
        del pending_tasks[task_index]
        with open(TODO_FILE, "w") as file:
            file.write("\n".join(pending_tasks + completed_tasks))

def remind_todo():
    while True:
        time.sleep(60 * 30)

        tasks = get_todo_list()
        if tasks:
            pending_tasks = "\n".join(f"- {task}" for task in tasks)
            speak_response("You have pending tasks in your to-do list.")
            print(Fore.GREEN + f"Zedd: You have pending tasks:\n{pending_tasks}")
