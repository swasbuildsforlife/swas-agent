import os
import json
from dotenv import load_dotenv
from google import genai

from calendar_tools import create_calendar_event


# Load environment variables
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()


# Create Gemini client
client = genai.Client(api_key=api_key)


# ============================================================
# CALCULATOR TOOL
# ============================================================

def calculator(expression: str):
    """Safely calculate a mathematical expression."""

    allowed_characters = "0123456789+-*/().% "

    if not all(char in allowed_characters for char in expression):
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
    "description": "Calculates mathematical expressions accurately.",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A mathematical expression such as 25 * 4 + 10"
            }
        },
        "required": ["expression"]
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
        "or remember an event in their calendar. "
        "The start time must be in YYYY-MM-DD HH:MM format. "
        "Use Asia/Kolkata timezone."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Title of the calendar event."
            },
            "start_time": {
                "type": "string",
                "description": (
                    "Event start time in YYYY-MM-DD HH:MM format. "
                    "Example: 2026-09-15 17:00"
                )
            },
            "duration_minutes": {
                "type": "integer",
                "description": "Duration of the event in minutes."
            },
            "description": {
                "type": "string",
                "description": "Optional description for the event."
            }
        },
        "required": [
            "title",
            "start_time"
        ]
    }
}


# ============================================================
# AVAILABLE FUNCTIONS
# ============================================================

available_functions = {
    "calculator": calculator,
    "create_calendar_event": create_calendar_event
}


# ============================================================
# SWAS AGENT
# ============================================================

print("=" * 50)
print("🤖 SWAS AGENT")
print("Your personal AI Agent")
print("=" * 50)
print("🧮 Calculator tool enabled")
print("📅 Google Calendar tool enabled")
print("Type 'exit' to stop the agent.\n")


while True:

    user_input = input("You: ")

    if user_input.lower().strip() == "exit":
        print("🤖 Agent: Goodbye bhai! 👋")
        break

    if not user_input.strip():
        continue

    try:

        # ----------------------------------------------------
        # FIRST INTERACTION
        # ----------------------------------------------------

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=user_input,
            tools=[
                calculator_tool,
                calendar_tool
            ]
        )


        # ----------------------------------------------------
        # FIND FUNCTION CALL
        # ----------------------------------------------------

        function_call = None

        for step in interaction.steps:

            if step.type == "function_call":
                function_call = step
                break


        # ----------------------------------------------------
        # TOOL EXECUTION
        # ----------------------------------------------------

        if function_call:

            print(
                f"🔧 Tool used: {function_call.name}"
            )

            function_name = function_call.name

            arguments = function_call.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)


            function = available_functions.get(
                function_name
            )


            if function:

                tool_result = function(**arguments)


                # ------------------------------------------------
                # SEND TOOL RESULT BACK TO GEMINI
                # ------------------------------------------------

                final_interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    previous_interaction_id=interaction.id,
                    input=[
                        {
                            "type": "function_result",
                            "name": function_name,
                            "call_id": function_call.id,
                            "result": tool_result
                        }
                    ],
                    tools=[
                        calculator_tool,
                        calendar_tool
                    ]
                )


                print(
                    "🤖 Agent:",
                    final_interaction.output_text
                )

                print()


            else:

                print("❌ Unknown tool requested.")
                print()


        else:

            # ------------------------------------------------
            # NORMAL RESPONSE
            # ------------------------------------------------

            print(
                "🤖 Agent:",
                interaction.output_text
            )

            print()


    except Exception as e:

        print("❌ Error:", e)
        print()