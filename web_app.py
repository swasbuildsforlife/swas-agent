import os
import json
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai

from calendar_tools import create_calendar_event


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Swas Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# PREMIUM DARK APPLE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    );

    html,
    body,
    [class*="css"] {
        font-family:
            'Inter',
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -15%,
                rgba(255,255,255,0.08),
                transparent 32%
            ),
            radial-gradient(
                circle at 10% 20%,
                rgba(120,120,255,0.035),
                transparent 28%
            ),
            linear-gradient(
                180deg,
                #090a0c 0%,
                #050608 55%,
                #020304 100%
            );

        color: #f5f5f7;
    }


    /* ========================================================
       HIDE STREAMLIT CHROME
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .block-container {
        max-width: 900px !important;

        padding-top: 42px !important;
        padding-bottom: 130px !important;
    }


    /* ========================================================
       TITLE
       ======================================================== */

    .main-title {
        text-align: center;

        font-size: 38px;
        font-weight: 700;

        letter-spacing: -1.8px;

        color: #f5f5f7;

        margin-top: 10px;
        margin-bottom: 7px;
    }

    .main-subtitle {
        text-align: center;

        font-size: 14px;

        color: #86868b;

        letter-spacing: 0.1px;

        margin-bottom: 20px;
    }


    /* ========================================================
       LOGO
       ======================================================== */

    .logo-wrap {
        display: flex;
        justify-content: center;

        margin-bottom: 15px;
    }

    .logo {
        width: 52px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                #24262b,
                #0b0c0f
            );

        border: 1px solid rgba(255,255,255,0.12);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.55),
            inset 0 1px 0 rgba(255,255,255,0.08);

        color: #ffffff;

        font-size: 24px;
        font-weight: 600;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-wrap {
        display: flex;
        justify-content: center;

        margin-bottom: 38px;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 7px 13px;

        border-radius: 999px;

        background:
            rgba(255,255,255,0.035);

        border:
            1px solid rgba(255,255,255,0.08);

        color: #8e8e93;

        font-size: 12px;
    }

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #34c759;

        box-shadow:
            0 0 12px rgba(52,199,89,0.75);
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: transparent !important;

        border: none !important;

        padding-top: 8px;
        padding-bottom: 8px;
    }

    [data-testid="stChatMessageContent"] {
        color: #e9e9eb;

        font-size: 15px;

        line-height: 1.7;
    }


    /* ========================================================
       USER CHAT BUBBLE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] {

        background:
            rgba(255,255,255,0.075);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius: 18px;

        padding:
            11px 15px;

        color: #f5f5f7;
    }


    /* ========================================================
       ASSISTANT CHAT
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] {

        color: #dedee2;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        position: fixed;

        bottom: 22px;

        left: 50%;

        transform: translateX(-50%);

        width:
            min(
                850px,
                calc(100% - 32px)
            );

        z-index: 999;
    }

    [data-testid="stChatInput"] > div {

        background:
            rgba(24,25,29,0.90);

        border:
            1px solid rgba(255,255,255,0.12);

        border-radius: 20px;

        box-shadow:
            0 25px 70px rgba(0,0,0,0.65),
            inset 0 1px 0 rgba(255,255,255,0.05);

        backdrop-filter:
            blur(25px);

        -webkit-backdrop-filter:
            blur(25px);
    }

    [data-testid="stChatInput"] textarea {

        color: #f5f5f7 !important;

        font-size: 15px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {

        color: #6e6e73 !important;
    }


    /* ========================================================
       TOOL CARD
       ======================================================== */

    .tool-card {

        margin-top: 10px;
        margin-bottom: 12px;

        padding: 13px 15px;

        border-radius: 15px;

        background:
            rgba(255,255,255,0.035);

        border:
            1px solid rgba(255,255,255,0.075);

        color: #8e8e93;

        font-size: 13px;
    }

    .tool-title {

        color: #f5f5f7;

        font-weight: 600;

        margin-bottom: 3px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {

        text-align: center;

        color: #454549;

        font-size: 10px;

        letter-spacing: 0.5px;

        margin-top: 75px;

        margin-bottom: 20px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left: 18px !important;

            padding-right: 18px !important;

            padding-top: 28px !important;
        }

        .main-title {

            font-size: 30px;

            letter-spacing: -1.2px;
        }

        .main-subtitle {

            font-size: 13px;
        }

        .logo {

            width: 48px;
            height: 48px;

            border-radius: 15px;
        }

        [data-testid="stChatInput"] {

            width:
                calc(100% - 20px);

            bottom: 10px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="logo-wrap">
        <div class="logo">✦</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Swas Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">Your personal AI assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="status-wrap">
        <div class="status">
            <span class="status-dot"></span>
            Online · Gemini powered
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CALCULATOR
# ============================================================

def calculator(expression: str):

    allowed_characters = "0123456789+-*/().% "

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


# ============================================================
# TOOL DECLARATIONS
# ============================================================

calculator_tool = {

    "type": "function",

    "name": "calculator",

    "description":
        "Calculates mathematical expressions accurately.",

    "parameters": {

        "type": "object",

        "properties": {

            "expression": {

                "type": "string",

                "description":
                    "A mathematical expression."

            }

        },

        "required": [
            "expression"
        ]
    }
}


calendar_tool = {

    "type": "function",

    "name": "create_calendar_event",

    "description": (

        "Creates an event in the user's Google Calendar. "

        "Use this whenever the user asks to schedule, "
        "add, create, book, or remember an event. "

        "Convert relative dates such as tomorrow, "
        "today, next Monday, etc. into exact dates "
        "using the current date provided to you. "

        "The start time must be in "
        "YYYY-MM-DD HH:MM format. "

        "Timezone is Asia/Kolkata."
    ),

    "parameters": {

        "type": "object",

        "properties": {

            "title": {

                "type": "string",

                "description":
                    "Title of the calendar event."
            },

            "start_time": {

                "type": "string",

                "description":
                    "Event start time in YYYY-MM-DD HH:MM format."
            },

            "duration_minutes": {

                "type": "integer",

                "description":
                    "Duration in minutes."
            },

            "description": {

                "type": "string",

                "description":
                    "Optional event description."
            }
        },

        "required": [
            "title",
            "start_time"
        ]
    }
}


available_functions = {

    "calculator":
        calculator,

    "create_calendar_event":
        create_calendar_event
}


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Message Swas Agent..."
)


if user_input:

    # ========================================================
    # USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    try:

        # ====================================================
        # CURRENT DATE / TIME
        # ====================================================

        now = datetime.now()

        current_date = now.strftime(
            "%Y-%m-%d"
        )

        current_time = now.strftime(
            "%H:%M"
        )


        # ====================================================
        # AGENT CONTEXT
        # ====================================================

        agent_input = f"""

You are Swas Agent, a helpful personal AI assistant.

Current date:
{current_date}

Current time:
{current_time}

Timezone:
Asia/Kolkata


IMPORTANT:

1. Understand natural language dates.

2. "Today" means the current date.

3. "Tomorrow" means one day after
   the current date.

4. "Yesterday" means one day before
   the current date.

5. Resolve phrases such as
   "next Monday" using the current date.

6. When creating calendar events,
   convert dates and times into:

   YYYY-MM-DD HH:MM

7. Use the calendar tool whenever
   the user asks to create or schedule
   a Google Calendar event.

8. Do not ask the user for today's date.
   It is already provided above.

9. Use Asia/Kolkata timezone.

10. After a successful tool call,
    clearly confirm what was done.


USER REQUEST:

{user_input}

"""


        # ====================================================
        # GEMINI
        # ====================================================

        interaction = client.interactions.create(

            model="gemini-3.6-flash",

            input=agent_input,

            tools=[
                calculator_tool,
                calendar_tool
            ]
        )


        # ====================================================
        # FIND TOOL CALL
        # ====================================================

        function_call = None

        for step in interaction.steps:

            if step.type == "function_call":

                function_call = step

                break


        # ====================================================
        # TOOL EXECUTION
        # ====================================================

        if function_call:

            function_name = (
                function_call.name
            )

            arguments = (
                function_call.arguments
            )


            if isinstance(
                arguments,
                str
            ):

                arguments = json.loads(
                    arguments
                )


            function = (
                available_functions.get(
                    function_name
                )
            )


            if function:

                # ============================================
                # TOOL STATUS
                # ============================================

                if function_name == "create_calendar_event":

                    st.markdown(
                        """
                        <div class="tool-card">
                            <div class="tool-title">
                                📅 Calendar
                            </div>
                            Creating your event...
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif function_name == "calculator":

                    st.markdown(
                        """
                        <div class="tool-card">
                            <div class="tool-title">
                                🧮 Calculator
                            </div>
                            Calculating...
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ============================================
                # RUN TOOL
                # ============================================

                tool_result = function(
                    **arguments
                )


                # ============================================
                # SEND RESULT BACK TO GEMINI
                # ============================================

                final_interaction = (
                    client.interactions.create(

                        model="gemini-3.6-flash",

                        previous_interaction_id=
                            interaction.id,

                        input=[
                            {
                                "type":
                                    "function_result",

                                "name":
                                    function_name,

                                "call_id":
                                    function_call.id,

                                "result":
                                    tool_result
                            }
                        ],

                        tools=[
                            calculator_tool,
                            calendar_tool
                        ]
                    )
                )


                response = (
                    final_interaction.output_text
                )


            else:

                response = (
                    "❌ Unknown tool requested."
                )


        else:

            response = (
                interaction.output_text
            )


    except Exception as e:

        response = (
            f"❌ Something went wrong: {str(e)}"
        )


    # ========================================================
    # ASSISTANT RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        st.markdown(
            response
        )


    # ========================================================
    # SAVE RESPONSE
    # ========================================================

    st.session_state.messages.append(

        {
            "role": "assistant",
            "content": response
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        SWAS AGENT · PRIVATE AI ASSISTANT
    </div>
    """,
    unsafe_allow_html=True
)