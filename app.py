import os
import json
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from calendar_tools import create_calendar_event

from tools.tasks import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
)

from tools.reminders import (
    add_reminder,
    list_reminders,
    complete_reminder,
    delete_reminder,
)


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env"
    )


MODEL = "gemini-3.6-flash"

client = genai.Client(
    api_key=api_key
)


# ============================================================
# SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTIONS = """
You are Swas Agent, a personal AI assistant.

Your job is to help the user intelligently and naturally.

You have access to tools for:
- calculations
- Google Calendar
- personal tasks
- personal reminders

CURRENT DATE:
Use the actual current date and time provided by the application.

IMPORTANT RULES:

1. Be helpful, concise and natural.

2. If the user asks for a calculation,
   ALWAYS use the calculator tool.

3. If the user asks to create, schedule, add, book,
   or remember an event in their calendar,
   use Google Calendar.

4. For calendar requests involving words like:
   - today
   - tomorrow
   - next Monday
   - this evening
   - tonight
   resolve the date using the current date.

5. If the user asks to create/add a task,
   use the add_task tool.

6. If the user asks:
   - what tasks do I have?
   - show my tasks
   - list my tasks
   - pending tasks
   use the list_tasks tool.

7. If the user asks to complete, finish, or mark a task as done,
   use the complete_task tool.

8. If the user asks to delete or remove a task,
   use the delete_task tool.

9. When creating a task:
   - title is required
   - due_date is optional
   - priority can be low, medium, or high
   - if the user does not specify priority, use medium
   - if the user gives a relative date such as tomorrow,
     resolve it using the current date.

10. If the user asks to create or set a reminder,
    use the add_reminder tool.

11. If the user asks:
    - what reminders do I have?
    - show my reminders
    - list my reminders
    - pending reminders
    use the list_reminders tool.

12. If the user asks to complete, finish, or dismiss a reminder,
    use the complete_reminder tool.

13. If the user asks to delete or remove a reminder,
    use the delete_reminder tool.

14. When creating a reminder:
    - title is required
    - remind_at is required
    - remind_at must use YYYY-MM-DD HH:MM format
    - if the user says tomorrow, today, tonight, etc.,
      resolve it using the current date and time.

15. Tasks and reminders are different:
    - A task is something the user needs to do.
    - A reminder is something the user wants to be reminded about.

16. Never invent that a task, reminder, or calendar event was created.
    Only say it was created if the tool actually succeeds.

17. After a tool is executed, explain the result naturally.

18. If no tool is required, answer normally.

19. You are an agent, not just a chatbot.

20. Prefer taking action with the available tools when appropriate.
"""


# ============================================================
# CALCULATOR TOOL
# ============================================================

def calculator(expression: str):
    """
    Safely calculate a mathematical expression.
    """

    allowed_characters = (
        "0123456789"
        "+-*/().% "
    )

    if not expression:
        return {
            "error": "Empty mathematical expression."
        }

    if not all(
        char in allowed_characters
        for char in expression
    ):
        return {
            "error": "Invalid mathematical expression."
        }

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return {
            "expression": expression,
            "result": result
        }

    except Exception:

        return {
            "error": "Could not calculate the expression."
        }


calculator_tool = {
    "type": "function",
    "name": "calculator",
    "description": (
        "Calculates mathematical expressions accurately. "
        "Use this tool whenever the user asks for arithmetic "
        "or mathematical calculations."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "A mathematical expression such as "
                    "25 * 4 + 10"
                )
            }
        },
        "required": [
            "expression"
        ]
    }
}


# ============================================================
# GOOGLE CALENDAR TOOL
# ============================================================

calendar_tool = {
    "type": "function",
    "name": "create_calendar_event",
    "description": (
        "Creates an event in the user's Google Calendar. "
        "Use this when the user asks to schedule, add, create, "
        "book or remember an event in their calendar. "
        "The start time must be in YYYY-MM-DD HH:MM format. "
        "Use Asia/Kolkata timezone."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "title": {
                "type": "string",
                "description": (
                    "Title of the calendar event."
                )
            },

            "start_time": {
                "type": "string",
                "description": (
                    "Event start time in "
                    "YYYY-MM-DD HH:MM format."
                )
            },

            "duration_minutes": {
                "type": "integer",
                "description": (
                    "Duration of the event in minutes. "
                    "Default is 60 minutes."
                )
            },

            "description": {
                "type": "string",
                "description": (
                    "Optional description for the event."
                )
            }

        },

        "required": [
            "title",
            "start_time"
        ]
    }
}


# ============================================================
# TASK TOOLS
# ============================================================

add_task_tool = {
    "type": "function",
    "name": "add_task",
    "description": (
        "Creates a personal task for the user. "
        "Use this when the user asks to add, create, "
        "remember, or save a task."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "title": {
                "type": "string",
                "description": (
                    "The task title."
                )
            },

            "due_date": {
                "type": "string",
                "description": (
                    "Optional task due date/time in "
                    "YYYY-MM-DD HH:MM format."
                )
            },

            "priority": {
                "type": "string",
                "enum": [
                    "low",
                    "medium",
                    "high"
                ],
                "description": (
                    "Task priority. Use medium if not specified."
                )
            }

        },

        "required": [
            "title"
        ]
    }
}


list_tasks_tool = {
    "type": "function",
    "name": "list_tasks",
    "description": (
        "Lists the user's saved tasks. "
        "Use this when the user asks to see, show, "
        "check, or list their tasks."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "include_completed": {
                "type": "boolean",
                "description": (
                    "If true, include completed tasks. "
                    "Default is false."
                )
            }

        },
        "required": []
    }
}


complete_task_tool = {
    "type": "function",
    "name": "complete_task",
    "description": (
        "Marks a specific task as completed. "
        "Use this when the user says they finished "
        "or completed a task."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "task_id": {
                "type": "integer",
                "description": (
                    "The numeric ID of the task to complete."
                )
            }

        },
        "required": [
            "task_id"
        ]
    }
}


delete_task_tool = {
    "type": "function",
    "name": "delete_task",
    "description": (
        "Deletes a specific task. "
        "Use this when the user asks to remove or delete the task."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "task_id": {
                "type": "integer",
                "description": (
                    "The numeric ID of the task to delete."
                )
            }

        },
        "required": [
            "task_id"
        ]
    }
}


# ============================================================
# REMINDER TOOLS
# ============================================================

add_reminder_tool = {
    "type": "function",
    "name": "add_reminder",
    "description": (
        "Creates a personal reminder for the user. "
        "Use this when the user asks to remind them about "
        "something at a specific date or time."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "title": {
                "type": "string",
                "description": (
                    "The reminder title."
                )
            },

            "remind_at": {
                "type": "string",
                "description": (
                    "Reminder date and time in "
                    "YYYY-MM-DD HH:MM format."
                )
            }

        },
        "required": [
            "title",
            "remind_at"
        ]
    }
}


list_reminders_tool = {
    "type": "function",
    "name": "list_reminders",
    "description": (
        "Lists the user's saved reminders. "
        "Use this when the user asks to see, show, "
        "check, or list their reminders."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "include_completed": {
                "type": "boolean",
                "description": (
                    "If true, include completed reminders. "
                    "Default is false."
                )
            }

        },
        "required": []
    }
}


complete_reminder_tool = {
    "type": "function",
    "name": "complete_reminder",
    "description": (
        "Marks a specific reminder as completed or dismissed."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "reminder_id": {
                "type": "integer",
                "description": (
                    "The numeric ID of the reminder to complete."
                )
            }

        },
        "required": [
            "reminder_id"
        ]
    }
}


delete_reminder_tool = {
    "type": "function",
    "name": "delete_reminder",
    "description": (
        "Deletes a specific reminder."
    ),
    "parameters": {
        "type": "object",
        "properties": {

            "reminder_id": {
                "type": "integer",
                "description": (
                    "The numeric ID of the reminder to delete."
                )
            }

        },
        "required": [
            "reminder_id"
        ]
    }
}


# ============================================================
# ALL AVAILABLE FUNCTIONS
# ============================================================

available_functions = {

    "calculator": calculator,

    "create_calendar_event": create_calendar_event,

    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,

    "add_reminder": add_reminder,
    "list_reminders": list_reminders,
    "complete_reminder": complete_reminder,
    "delete_reminder": delete_reminder,
}


# ============================================================
# ALL GEMINI TOOLS
# ============================================================

all_tools = [

    calculator_tool,
    calendar_tool,

    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,

    add_reminder_tool,
    list_reminders_tool,
    complete_reminder_tool,
    delete_reminder_tool,
]


# ============================================================
# TOOL EXECUTOR
# ============================================================

def execute_tool(function_name, arguments):
    """
    Executes a tool requested by Gemini.
    """

    function = available_functions.get(
        function_name
    )

    if not function:
        return {
            "error": f"Unknown tool: {function_name}"
        }

    try:

        if isinstance(arguments, str):
            arguments = json.loads(arguments)

        return function(**arguments)

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# AGENT ENGINE
# ============================================================

def run_agent(user_input: str):
    """
    Main Swas Agent engine.

    Takes user input and returns the final AI response.
    """

    if not user_input or not user_input.strip():
        return {
            "response": "Tell me what you need help with.",
            "tool_used": None,
            "tool_result": None
        }

    # --------------------------------------------------------
    # CURRENT DATE / TIME
    # --------------------------------------------------------

    current_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    input_with_context = f"""
{SYSTEM_INSTRUCTIONS}

Current date and time:
{current_datetime}

User request:
{user_input}
"""

    # --------------------------------------------------------
    # FIRST GEMINI INTERACTION
    # --------------------------------------------------------

    interaction = client.interactions.create(
        model=MODEL,
        input=input_with_context,
        tools=all_tools
    )

    # --------------------------------------------------------
    # FIND FUNCTION CALL
    # --------------------------------------------------------

    function_call = None

    for step in interaction.steps:

        if step.type == "function_call":
            function_call = step
            break

    # --------------------------------------------------------
    # NO TOOL REQUIRED
    # --------------------------------------------------------

    if not function_call:

        return {
            "response": interaction.output_text,
            "tool_used": None,
            "tool_result": None
        }

    # --------------------------------------------------------
    # TOOL EXECUTION
    # --------------------------------------------------------

    function_name = function_call.name
    arguments = function_call.arguments

    tool_result = execute_tool(
        function_name,
        arguments
    )

    # --------------------------------------------------------
    # SEND TOOL RESULT BACK TO GEMINI
    # --------------------------------------------------------

    final_interaction = client.interactions.create(
        model=MODEL,
        previous_interaction_id=interaction.id,
        input=[
            {
                "type": "function_result",
                "name": function_name,
                "call_id": function_call.id,
                "result": tool_result
            }
        ],
        tools=all_tools
    )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "response": final_interaction.output_text,
        "tool_used": function_name,
        "tool_result": tool_result
    }


# ============================================================
# TERMINAL MODE
# ============================================================

def run_cli():
    """
    Optional terminal interface for testing Swas Agent.
    """

    print("=" * 55)
    print("🤖 SWAS AGENT")
    print("Your Personal AI Agent")
    print("=" * 55)

    print("🧮 Calculator tool enabled")
    print("📅 Google Calendar tool enabled")
    print("✅ Task Manager enabled")
    print("🔔 Reminder Manager enabled")
    print()

    print("Type 'exit' to stop.")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower().strip() == "exit":

            print(
                "🤖 Agent: Goodbye bhai! 👋"
            )

            break

        if not user_input.strip():
            continue

        try:

            result = run_agent(
                user_input
            )

            if result["tool_used"]:

                print(
                    f"🔧 Tool used: "
                    f"{result['tool_used']}"
                )

            print(
                "🤖 Agent:",
                result["response"]
            )

            print()

        except Exception as e:

            print(
                "❌ Error:",
                e
            )

            print()


# ============================================================
# RUN ONLY WHEN app.py IS EXECUTED DIRECTLY
# ============================================================

if __name__ == "__main__":
    run_cli()