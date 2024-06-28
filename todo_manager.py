# todo_manager.py

TODO_FILE = "todo.txt"

def add_to_todo(task):
    with open(TODO_FILE, "a") as file:
        file.write(f"{task}\n")

def get_todo_list():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = file.readlines()
            if tasks:
                return [task.strip() for task in tasks]
            else:
                return []
    except FileNotFoundError:
        return []

def remind_todo():
    tasks = get_todo_list()
    if tasks:
        tasks_text = "\n".join(tasks)
        return f"You have pending tasks:\n{tasks_text}"
    else:
        return "Your to-do list is empty."
