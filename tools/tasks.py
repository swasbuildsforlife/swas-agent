import json
from pathlib import Path
from datetime import datetime


TASKS_FILE = Path("tasks.json")


def load_tasks():
    """Load all saved tasks."""
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save tasks to disk."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)


def add_task(title, due_date=None, priority="medium"):
    """Create a new task."""

    tasks = load_tasks()

    task_id = max(
        [task.get("id", 0) for task in tasks],
        default=0
    ) + 1

    task = {
        "id": task_id,
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def list_tasks(include_completed=False):
    """Return saved tasks."""

    tasks = load_tasks()

    if not include_completed:
        tasks = [
            task for task in tasks
            if not task.get("completed", False)
        ]

    return tasks


def complete_task(task_id):
    """Mark a task as completed."""

    tasks = load_tasks()

    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return task

    return None


def delete_task(task_id):
    """Delete a task."""

    tasks = load_tasks()

    updated_tasks = [
        task for task in tasks
        if task.get("id") != task_id
    ]

    if len(updated_tasks) == len(tasks):
        return False

    save_tasks(updated_tasks)
    return True


if __name__ == "__main__":
    task = add_task(
        "Test Swas Task",
        "2026-09-16 18:00",
        "high"
    )

    print("Task created:")
    print(json.dumps(task, indent=4))

    print("\nCurrent tasks:")
    print(json.dumps(list_tasks(), indent=4))