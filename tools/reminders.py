from pathlib import Path
from datetime import datetime
import json


# ============================================================
# CONFIG
# ============================================================

REMINDERS_FILE = Path("reminders.json")


# ============================================================
# STORAGE
# ============================================================

def load_reminders():
    """Load reminders from local JSON storage."""
    if not REMINDERS_FILE.exists():
        return []

    try:
        with open(REMINDERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_reminders(reminders):
    """Save reminders to local JSON storage."""
    with open(REMINDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(reminders, file, indent=4, ensure_ascii=False)


# ============================================================
# ADD REMINDER
# ============================================================

def add_reminder(title, remind_at):
    """
    Add a reminder.

    remind_at format:
    YYYY-MM-DD HH:MM
    """

    reminders = load_reminders()

    next_id = 1

    if reminders:
        next_id = max(reminder["id"] for reminder in reminders) + 1

    reminder = {
        "id": next_id,
        "title": title,
        "remind_at": remind_at,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }

    reminders.append(reminder)
    save_reminders(reminders)

    return reminder


# ============================================================
# LIST REMINDERS
# ============================================================

def list_reminders(include_completed=False):
    """Return reminders."""

    reminders = load_reminders()

    if include_completed:
        return reminders

    return [
        reminder
        for reminder in reminders
        if not reminder.get("completed", False)
    ]


# ============================================================
# COMPLETE REMINDER
# ============================================================

def complete_reminder(reminder_id):
    """Mark a reminder as completed."""

    reminders = load_reminders()

    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminder["completed"] = True
            save_reminders(reminders)
            return True

    return False


# ============================================================
# DELETE REMINDER
# ============================================================

def delete_reminder(reminder_id):
    """Delete a reminder."""

    reminders = load_reminders()

    updated_reminders = [
        reminder
        for reminder in reminders
        if reminder["id"] != reminder_id
    ]

    if len(updated_reminders) == len(reminders):
        return False

    save_reminders(updated_reminders)
    return True


# ============================================================
# DUE REMINDERS
# ============================================================

def get_due_reminders():
    """
    Return reminders whose time has arrived.

    Expected format:
    YYYY-MM-DD HH:MM
    """

    reminders = load_reminders()

    now = datetime.now()
    due = []

    for reminder in reminders:
        if reminder.get("completed", False):
            continue

        try:
            remind_at = datetime.strptime(
                reminder["remind_at"],
                "%Y-%m-%d %H:%M"
            )

            if remind_at <= now:
                due.append(reminder)

        except (ValueError, TypeError, KeyError):
            continue

    return due