import os
import json
from datetime import datetime
from textwrap import dedent

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
    initial_sidebar_state="collapsed",
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=api_key)


# ============================================================
# PREMIUM CSS
# ============================================================

st.html(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                700px 420px at 50% -100px,
                rgba(125,125,255,0.12),
                transparent 70%
            ),
            radial-gradient(
                500px 350px at 0% 30%,
                rgba(80,150,255,0.045),
                transparent 70%
            ),
            radial-gradient(
                500px 350px at 100% 55%,
                rgba(180,80,255,0.035),
                transparent 70%
            ),
            linear-gradient(
                180deg,
                #08090b 0%,
                #050608 48%,
                #020304 100%
            );

        color: #f5f5f7;
        min-height: 100vh;
    }

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1080px !important;
        padding-top: 26px !important;
        padding-bottom: 150px !important;
    }


    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 10px 4px 22px 4px;
        margin-bottom: 20px;

        border-bottom: 1px solid rgba(255,255,255,0.055);
    }

    .brand-mini {
        display: flex;
        align-items: center;
        gap: 11px;
    }

    .brand-mark {
        width: 34px;
        height: 34px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                145deg,
                #30323a,
                #101115
            );

        border: 1px solid rgba(255,255,255,0.13);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.10);

        color: white;
        font-size: 17px;
        font-weight: 700;
    }

    .brand-name {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: -0.3px;
        color: #f5f5f7;
    }

    .brand-version {
        color: #636369;
        font-size: 10px;
        margin-left: 5px;
    }

    .connection {
        display: flex;
        align-items: center;
        gap: 7px;

        padding: 6px 11px;

        border-radius: 999px;

        background: rgba(52,199,89,0.055);

        border: 1px solid rgba(52,199,89,0.12);

        color: #8f9690;

        font-size: 10px;
        letter-spacing: 0.2px;
    }

    .connection-dot {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #34c759;

        box-shadow:
            0 0 12px rgba(52,199,89,0.8);
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        text-align: center;
        padding-top: 44px;
        padding-bottom: 30px;
    }

    .hero-orb {
        width: 76px;
        height: 76px;

        margin: 0 auto 25px auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 25px;

        background:
            radial-gradient(
                circle at 30% 25%,
                rgba(255,255,255,0.18),
                transparent 32%
            ),
            linear-gradient(
                145deg,
                #282b33,
                #0b0c0f
            );

        border: 1px solid rgba(255,255,255,0.14);

        box-shadow:
            0 25px 70px rgba(0,0,0,0.65),
            0 0 70px rgba(120,120,255,0.055),
            inset 0 1px 0 rgba(255,255,255,0.09);

        font-size: 32px;
        color: white;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.05;

        font-weight: 700;
        letter-spacing: -2.5px;

        margin: 0;

        background:
            linear-gradient(
                180deg,
                #ffffff 0%,
                #b9b9c0 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        margin-top: 13px;

        color: #77777f;

        font-size: 14px;
        letter-spacing: 0.1px;
    }


    /* ========================================================
       SECTION LABEL
       ======================================================== */

    .section-label {
        text-align: center;

        color: #56565d;

        font-size: 10px;
        font-weight: 600;

        text-transform: uppercase;
        letter-spacing: 1.5px;

        margin: 12px 0 14px 0;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;
        min-height: 78px;

        border-radius: 17px;

        border: 1px solid rgba(255,255,255,0.075);

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.022)
            );

        color: #e9e9ed;

        font-size: 12px;
        font-weight: 500;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.035),
            0 15px 40px rgba(0,0,0,0.16);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color: rgba(255,255,255,0.16);

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.075),
                rgba(255,255,255,0.03)
            );

        color: white;

        box-shadow:
            0 18px 45px rgba(0,0,0,0.28);
    }


    /* ========================================================
       CHAT
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        color: #dedee3;
        font-size: 14px;
        line-height: 1.75;
    }


    /* USER MESSAGE */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) [data-testid="stChatMessageContent"] {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.085),
                rgba(255,255,255,0.045)
            );

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 20px 20px 6px 20px;

        padding: 12px 17px;

        color: #f3f3f5;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.18);
    }


    /* ASSISTANT MESSAGE */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] {

        color: #d7d7dc;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        position: fixed;

        bottom: 20px;
        left: 50%;

        transform: translateX(-50%);

        width: min(920px, calc(100% - 30px));

        z-index: 999;
    }

    [data-testid="stChatInput"] > div {
        background: rgba(20,21,25,0.88);

        border: 1px solid rgba(255,255,255,0.13);

        border-radius: 22px;

        box-shadow:
            0 30px 90px rgba(0,0,0,0.72),
            0 0 45px rgba(120,120,255,0.025),
            inset 0 1px 0 rgba(255,255,255,0.06);

        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
    }

    [data-testid="stChatInput"] textarea {
        color: #f5f5f7 !important;
        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #68686e !important;
    }


    /* ========================================================
       TOOL STATUS
       ======================================================== */

    .tool-card {
        display: flex;
        align-items: center;
        gap: 12px;

        padding: 12px 15px;
        margin: 7px 0 12px 0;

        border-radius: 15px;

        background: rgba(255,255,255,0.035);

        border: 1px solid rgba(255,255,255,0.07);

        color: #85858c;

        font-size: 11px;
    }

    .tool-icon {
        width: 30px;
        height: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: rgba(255,255,255,0.06);

        font-size: 14px;
    }

    .tool-name {
        color: #dedee3;

        font-size: 11px;
        font-weight: 600;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    .soft-divider {
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.07),
                transparent
            );

        margin: 25px 0;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        margin-top: 80px;

        color: #39393e;

        font-size: 9px;

        letter-spacing: 1.3px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding: 18px 15px 135px 15px !important;
        }

        .topbar {
            margin-bottom: 5px;
        }

        .hero {
            padding-top: 30px;
        }

        .hero-orb {
            width: 64px;
            height: 64px;

            border-radius: 21px;

            font-size: 27px;
        }

        .hero-title {
            font-size: 36px;
            letter-spacing: -1.7px;
        }

        .hero-subtitle {
            font-size: 12px;
        }

        [data-testid="stChatInput"] {
            width: calc(100% - 18px);
            bottom: 9px;
        }
    }

    </style>
    """
)


# ============================================================
# TOP BAR
# ============================================================

st.html(
    """
    <div class="topbar">

        <div class="brand-mini">

            <div class="brand-mark">
                ✦
            </div>

            <div class="brand-name">
                Swas Agent
                <span class="brand-version">
                    PERSONAL AI
                </span>
            </div>

        </div>

        <div class="connection">

            <span class="connection-dot"></span>

            Gemini online

        </div>

    </div>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False


# ============================================================
# HERO / EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.html(
        """
        <div class="hero">

            <div class="hero-orb">
                ✦
            </div>

            <div class="hero-title">
                What can I help you with?
            </div>

            <div class="hero-subtitle">
                Your personal AI assistant for ideas,
                calculations and your schedule.
            </div>

        </div>
        """
    )

    st.html(
        '<div class="section-label">Quick actions</div>'
    )

    quick_col1, quick_col2, quick_col3 = st.columns(
        3,
        gap="medium"
    )

    with quick_col1:

        if st.button(
            "✨  Ask anything",
            key="quick_ask"
        ):

            st.session_state.quick_prompt = (
                "Give me 5 interesting things I can ask you to help me with."
            )

            st.rerun()

    with quick_col2:

        if st.button(
            "📅  Schedule something",
            key="quick_calendar"
        ):

            st.session_state.quick_prompt = (
                "Help me schedule something in my Google Calendar."
            )

            st.rerun()

    with quick_col3:

        if st.button(
            "🧮  Calculate",
            key="quick_calc"
        ):

            st.session_state.quick_prompt = (
                "Calculate 125 × 48."
            )

            st.rerun()

    st.html(
        '<div class="soft-divider"></div>'
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
        "Convert relative dates such as tomorrow, today, "
        "next Monday, etc. into exact dates using the "
        "current date provided to you. "
        "The start time must be in YYYY-MM-DD HH:MM format. "
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

    "calculator": calculator,

    "create_calendar_event":
        create_calendar_event
}


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# QUICK PROMPT
# ============================================================

quick_prompt = st.session_state.pop(
    "quick_prompt",
    None
)


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Message Swas Agent..."
)

if quick_prompt:
    user_input = quick_prompt


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_input:

    st.session_state.started = True

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
        # AGENT PROMPT
        # ====================================================

        agent_input = f"""
You are Swas Agent, a helpful personal AI assistant.

Current date:
{current_date}

Current time:
{current_time}

Timezone:
Asia/Kolkata


IMPORTANT RULES:

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

11. Be concise but helpful.

12. Do not mention internal tools,
    function calls, APIs or implementation
    details unless specifically asked.


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

                    st.html(
                        """
                        <div class="tool-card">

                            <div class="tool-icon">
                                📅
                            </div>

                            <div>

                                <div class="tool-name">
                                    Calendar
                                </div>

                                Creating your event...

                            </div>

                        </div>
                        """
                    )

                elif function_name == "calculator":

                    st.html(
                        """
                        <div class="tool-card">

                            <div class="tool-icon">
                                🧮
                            </div>

                            <div>

                                <div class="tool-name">
                                    Calculator
                                </div>

                                Working it out...

                            </div>

                        </div>
                        """
                    )


                # ============================================
                # RUN FUNCTION
                # ============================================

                tool_result = function(
                    **arguments
                )


                # ============================================
                # SEND RESULT TO GEMINI
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

        st.markdown(response)


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

st.html(
    """
    <div class="footer">
        SWAS AGENT · PERSONAL AI SYSTEM · GEMINI
    </div>
    """
)