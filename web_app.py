from datetime import datetime

import streamlit as st

from app import run_agent
from tools.tasks import list_tasks, complete_task, delete_task


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Swas Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


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
        padding-top: 62px;
        padding-bottom: 34px;
    }

    .hero-orb {
        position: relative;

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

    .hero-orb::after {
        content: "";
        position: absolute;
        inset: -12px;

        border-radius: 31px;

        border: 1px solid rgba(255,255,255,0.035);

        box-shadow:
            0 0 55px rgba(125,125,255,0.045);
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
        min-height: 48px;

        border-radius: 14px;

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
        max-width: 900px;
        margin: 0 auto !important;
        background: transparent !important;
        border: none !important;
        padding: 9px 0 !important;
    }

    [data-testid="stChatMessageContent"] {
        color: #dedee3;
        font-size: 14px;
        line-height: 1.75;
        max-width: 100%;
        padding: 0 !important;
    }

    [data-testid="stChatMessage"]
    [data-testid="chatAvatarIcon-user"],
    [data-testid="stChatMessage"]
    [data-testid="chatAvatarIcon-assistant"] {
        width: 32px !important;
        height: 32px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.28);
    }

    [data-testid="stChatMessage"]
    [data-testid="stChatMessageAvatar"] {
        padding-top: 2px !important;
    }


    /* ========================================================
       USER BUBBLE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        justify-content: flex-end;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) [data-testid="stChatMessageContent"] {

        width: fit-content;
        max-width: min(720px, 78%);

        margin-left: auto;

        padding: 12px 16px !important;

        border-radius: 18px 18px 5px 18px !important;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.095),
                rgba(255,255,255,0.045)
            ) !important;

        border: 1px solid rgba(255,255,255,0.085) !important;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.20),
            inset 0 1px 0 rgba(255,255,255,0.035);
    }


    /* ========================================================
       ASSISTANT RESPONSE
       ======================================================== */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] {

        max-width: min(780px, 88%);

        color: #e1e1e6 !important;

        padding-top: 2px !important;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] p {

        margin: 0 0 8px 0;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) [data-testid="stChatMessageContent"] p:last-child {

        margin-bottom: 0;
    }

    [data-testid="stChatMessageContent"] strong {
        color: #ffffff;
        font-weight: 650;
    }

    [data-testid="stChatMessageContent"] code {
        background: rgba(255,255,255,0.065);

        border: 1px solid rgba(255,255,255,0.07);

        border-radius: 6px;

        padding: 2px 5px;
    }

    [data-testid="stChatMessageContent"] pre {
        border-radius: 14px !important;

        border: 1px solid rgba(255,255,255,0.08) !important;

        background: #0b0c10 !important;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        position: fixed;

        bottom: 18px;
        left: 50%;

        transform: translateX(-50%);

        width: min(920px, calc(100% - 30px));

        z-index: 999;
    }

    [data-testid="stChatInput"] > div {
        min-height: 56px;

        border-radius: 19px !important;

        background: rgba(15,16,20,0.92) !important;

        border: 1px solid rgba(255,255,255,0.12) !important;

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

        padding-top: 15px !important;
        padding-bottom: 13px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #68686e !important;
    }


    /* ========================================================
       TOOL ACTIVITY
       ======================================================== */

    .tool-card {
        width: min(700px, 100%);

        box-sizing: border-box;

        display: flex;
        align-items: center;

        gap: 12px;

        padding: 10px 13px;

        margin: 2px 0 10px 0;

        border-radius: 13px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );

        border: 1px solid rgba(255,255,255,0.065);

        color: #777982;

        font-size: 10px;
    }

    .tool-card .tool-icon {
        flex: 0 0 28px;

        width: 28px;
        height: 28px;

        border-radius: 8px;

        background: rgba(255,255,255,0.055);

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 13px;
    }

    .tool-card .tool-name {
        color: #dfe0e5;

        font-size: 10px;

        font-weight: 650;

        margin-bottom: 2px;

        letter-spacing: 0.1px;
    }

    .activity-dot {
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: #8b8dff;

        box-shadow:
            0 0 12px rgba(139,141,255,0.75);

        animation:
            swasPulse 1.2s ease-in-out infinite;
    }

    @keyframes swasPulse {

        0%, 100% {
            opacity: 0.45;
            transform: scale(0.85);
        }

        50% {
            opacity: 1;
            transform: scale(1);
        }
    }


    /* ========================================================
       TASK PANEL
       ======================================================== */

    .task-panel {
        max-width: 900px;

        margin: 20px auto 28px auto;

        padding: 18px;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );

        border: 1px solid rgba(255,255,255,0.065);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.20);
    }

    .task-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 14px;
    }

    .task-title {
        color: #eeeeF2;

        font-size: 13px;

        font-weight: 650;
    }

    .task-subtitle {
        color: #686970;

        font-size: 10px;

        margin-top: 3px;
    }

    .task-row {
        display: flex;

        align-items: center;

        gap: 12px;

        padding: 12px;

        margin-top: 8px;

        border-radius: 13px;

        background: rgba(255,255,255,0.025);

        border: 1px solid rgba(255,255,255,0.045);
    }

    .task-check {
        width: 9px;
        height: 9px;

        border-radius: 50%;

        background: #8b8dff;

        box-shadow:
            0 0 12px rgba(139,141,255,0.45);

        flex-shrink: 0;
    }

    .task-info {
        flex: 1;
        min-width: 0;
    }

    .task-name {
        color: #dedee3;

        font-size: 12px;

        font-weight: 550;
    }

    .task-meta {
        color: #666870;

        font-size: 9px;

        margin-top: 3px;
    }

    .priority-high {
        color: #ff8b8b;
    }

    .priority-medium {
        color: #d7c47a;
    }

    .priority-low {
        color: #86c995;
    }

    .completed-task {
        opacity: 0.55;
    }

    .completed-task .task-name {
        text-decoration: line-through;
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

        opacity: 0.7;
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

        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-user"]
        ) [data-testid="stChatMessageContent"] {

            max-width: 85%;
        }

        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-assistant"]
        ) [data-testid="stChatMessageContent"] {

            max-width: 94%;
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
# TASK PANEL
# ============================================================

pending_tasks = list_tasks()
all_tasks = list_tasks(include_completed=True)

completed_tasks = [
    task
    for task in all_tasks
    if task.get("completed", False)
]


if pending_tasks or completed_tasks:

    st.html(
        """
        <div class="task-panel">

            <div class="task-header">

                <div>
                    <div class="task-title">
                        ✦ My Tasks
                    </div>

                    <div class="task-subtitle">
                        Your personal task list
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # PENDING TASKS
    # --------------------------------------------------------

    if pending_tasks:

        for task in pending_tasks:

            priority = task.get(
                "priority",
                "medium"
            )

            due_date = task.get(
                "due_date"
            )

            if due_date:
                meta = (
                    f"Due: {due_date} · "
                    f"Priority: {priority}"
                )
            else:
                meta = f"Priority: {priority}"

            col1, col2 = st.columns(
                [5, 1],
                gap="small"
            )

            with col1:

                st.html(
                    f"""
                    <div class="task-row">

                        <div class="task-check"></div>

                        <div class="task-info">

                            <div class="task-name">
                                {task.get("title", "Untitled task")}
                            </div>

                            <div class="task-meta priority-{priority}">
                                {meta}
                            </div>

                        </div>

                    </div>
                    """
                )

            with col2:

                if st.button(
                    "✓ Done",
                    key=f"complete_task_{task['id']}"
                ):

                    complete_task(
                        task["id"]
                    )

                    st.rerun()

    # --------------------------------------------------------
    # COMPLETED TASKS
    # --------------------------------------------------------

    if completed_tasks:

        with st.expander(
            f"Completed · {len(completed_tasks)}"
        ):

            for task in completed_tasks:

                col1, col2 = st.columns(
                    [5, 1],
                    gap="small"
                )

                with col1:

                    st.html(
                        f"""
                        <div class="task-row completed-task">

                            <div class="task-check"></div>

                            <div class="task-info">

                                <div class="task-name">
                                    {task.get("title", "Untitled task")}
                                </div>

                                <div class="task-meta">
                                    Completed
                                </div>

                            </div>

                        </div>
                        """
                    )

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_task_{task['id']}"
                    ):

                        delete_task(
                            task["id"]
                        )

                        st.rerun()


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
                tasks, calculations and your schedule.
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
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    avatar = (
        "🤖"
        if role == "assistant"
        else "👤"
    )

    with st.chat_message(
        role,
        avatar=avatar
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

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            user_input
        )

    try:

        # ----------------------------------------------------
        # SWAS AGENT BRAIN
        # ----------------------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            result = run_agent(
                user_input
            )

            tool_used = result.get(
                "tool_used"
            )


            # ------------------------------------------------
            # TOOL ACTIVITY
            # ------------------------------------------------

            if tool_used == "create_calendar_event":

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

                            Working with your Google Calendar...

                        </div>

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            elif tool_used == "calculator":

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

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            elif tool_used == "add_task":

                st.html(
                    """
                    <div class="tool-card">

                        <div class="tool-icon">
                            ✅
                        </div>

                        <div>

                            <div class="tool-name">
                                Task Manager
                            </div>

                            Adding your task...

                        </div>

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            elif tool_used == "list_tasks":

                st.html(
                    """
                    <div class="tool-card">

                        <div class="tool-icon">
                            📋
                        </div>

                        <div>

                            <div class="tool-name">
                                Task Manager
                            </div>

                            Checking your tasks...

                        </div>

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            elif tool_used == "complete_task":

                st.html(
                    """
                    <div class="tool-card">

                        <div class="tool-icon">
                            ☑️
                        </div>

                        <div>

                            <div class="tool-name">
                                Task Manager
                            </div>

                            Marking task as complete...

                        </div>

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            elif tool_used == "delete_task":

                st.html(
                    """
                    <div class="tool-card">

                        <div class="tool-icon">
                            🗑️
                        </div>

                        <div>

                            <div class="tool-name">
                                Task Manager
                            </div>

                            Removing task...

                        </div>

                        <div class="activity-dot"></div>

                    </div>
                    """
                )


            # ------------------------------------------------
            # RESPONSE
            # ------------------------------------------------

            response = result.get(
                "response",
                "I couldn't generate a response."
            )

            st.markdown(
                response
            )


            # ------------------------------------------------
            # QUOTA ERROR
            # ------------------------------------------------

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "too_many_requests" in error_text.lower()
        ):

            response = (
                "⚠️ Gemini's current request limit has been reached. "
                "Your local tools are still safe and working. "
                "Please wait a little and try again."
            )

        else:

            response = (
                f"❌ Something went wrong: {error_text}"
            )

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.markdown(
                response
            )


    # --------------------------------------------------------
    # SAVE RESPONSE
    # --------------------------------------------------------

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