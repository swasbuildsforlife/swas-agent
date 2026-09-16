import html

import streamlit as st

from app import run_agent

from tools.tasks import (
    list_tasks,
    complete_task,
    delete_task,
)

from tools.reminders import (
    list_reminders,
    complete_reminder,
    delete_reminder,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Swas Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PREMIUM DARK UI
# ============================================================

st.html(
    """
    <style>

    /* =========================
       GLOBAL
    ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(79, 70, 229, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(34, 197, 94, 0.07),
                transparent 25%
            ),
            #020617;
        color: #f8fafc;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* =========================
       TOP BAR
    ========================= */

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 4px 22px 4px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 11px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(
            135deg,
            #6366f1,
            #4f46e5
        );
        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.35);
    }

    .brand-title {
        font-size: 18px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #f8fafc;
    }

    .brand-subtitle {
        font-size: 10px;
        color: #64748b;
        letter-spacing: 1.5px;
        margin-top: 1px;
    }

    .online-status {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 7px 11px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        background: rgba(15, 23, 42, 0.55);
        border-radius: 999px;
        font-size: 11px;
        color: #94a3b8;
    }

    .online-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.8);
    }


    /* =========================
       HERO
    ========================= */

    .hero {
        text-align: center;
        padding: 48px 20px 30px 20px;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(34px, 5vw, 56px);
        line-height: 1.05;
        font-weight: 750;
        letter-spacing: -2.5px;
        color: #f8fafc;
    }

    .hero h1 span {
        background: linear-gradient(
            90deg,
            #818cf8,
            #c4b5fd,
            #67e8f9
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        margin: 16px auto 0 auto;
        max-width: 620px;
        color: #64748b;
        font-size: 15px;
        line-height: 1.7;
    }


    /* =========================
       QUICK ACTIONS
    ========================= */

    .quick-title {
        color: #64748b;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin: 10px 0 10px 2px;
    }

    div.stButton > button {
        border-radius: 13px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        background: rgba(15, 23, 42, 0.65);
        color: #cbd5e1;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: rgba(129, 140, 248, 0.4);
        background: rgba(30, 41, 59, 0.85);
        color: white;
        transform: translateY(-1px);
    }


    /* =========================
       PANELS
    ========================= */

    .panel {
        margin-top: 28px;
        padding: 22px;
        border-radius: 20px;
        border: 1px solid rgba(148, 163, 184, 0.10);
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.88),
                rgba(2, 6, 23, 0.78)
            );
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.18);
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .panel-title {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
    }

    .panel-subtitle {
        font-size: 11px;
        color: #64748b;
        margin-top: 3px;
    }

    .count-badge {
        min-width: 28px;
        padding: 4px 9px;
        text-align: center;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.12);
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
    }


    /* =========================
       TASK / REMINDER CARDS
    ========================= */

    .item-card {
        display: flex;
        align-items: center;
        gap: 13px;
        padding: 13px 14px;
        margin-bottom: 9px;
        border-radius: 13px;
        border: 1px solid rgba(148, 163, 184, 0.08);
        background: rgba(15, 23, 42, 0.55);
    }

    .item-icon {
        width: 30px;
        height: 30px;
        flex: 0 0 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: rgba(99, 102, 241, 0.12);
        font-size: 14px;
    }

    .item-content {
        min-width: 0;
        flex: 1;
    }

    .item-name {
        color: #e2e8f0;
        font-size: 13px;
        font-weight: 600;
        word-break: break-word;
    }

    .item-meta {
        margin-top: 3px;
        color: #64748b;
        font-size: 10px;
    }

    .priority-high {
        color: #fca5a5;
    }

    .priority-medium {
        color: #fcd34d;
    }

    .priority-low {
        color: #86efac;
    }

    .completed-item {
        opacity: 0.55;
    }

    .completed-item .item-name {
        text-decoration: line-through;
    }


    /* =========================
       CHAT
    ========================= */

    .chat-heading {
        margin-top: 38px;
        margin-bottom: 12px;
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.3px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(148, 163, 184, 0.07);
        border-radius: 16px;
        margin-bottom: 9px;
    }

    [data-testid="stChatInput"] {
        margin-top: 15px;
    }

    [data-testid="stChatInput"] textarea {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 15px;
        color: #f8fafc;
    }


    /* =========================
       ACTIVITY
    ========================= */

    .activity {
        margin-top: 15px;
        padding: 13px 15px;
        border-radius: 13px;
        border: 1px solid rgba(99, 102, 241, 0.13);
        background: rgba(30, 41, 59, 0.45);
    }

    .activity-title {
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    .activity-text {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }


    /* =========================
       FOOTER
    ========================= */

    .footer {
        text-align: center;
        margin-top: 45px;
        color: #334155;
        font-size: 10px;
        letter-spacing: 0.8px;
    }


    /* =========================
       MOBILE
    ========================= */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .hero {
            padding-top: 30px;
        }

        .hero h1 {
            font-size: 36px;
        }

        .panel {
            padding: 15px;
            border-radius: 16px;
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

        <div class="brand">

            <div class="brand-icon">✦</div>

            <div>
                <div class="brand-title">Swas Agent</div>
                <div class="brand-subtitle">PERSONAL AI</div>
            </div>

        </div>

        <div class="online-status">
            <span class="online-dot"></span>
            Gemini online
        </div>

    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <h1>
            What can I help <span>you with?</span>
        </h1>

        <p>
            Your personal AI assistant for questions, calculations,
            tasks, reminders and scheduling.
        </p>

    </div>
    """
)


# ============================================================
# QUICK ACTIONS
# ============================================================

st.html(
    '<div class="quick-title">Quick actions</div>'
)

quick_col1, quick_col2, quick_col3 = st.columns(3)

with quick_col1:
    if st.button("💬  Ask anything", use_container_width=True):
        st.session_state.quick_prompt = "What can you help me with?"

with quick_col2:
    if st.button("📅  Schedule something", use_container_width=True):
        st.session_state.quick_prompt = (
            "Help me schedule something on my Google Calendar."
        )

with quick_col3:
    if st.button("🧮  Calculate", use_container_width=True):
        st.session_state.quick_prompt = (
            "Calculate 4589 * 27 + 156"
        )


# ============================================================
# TASKS PANEL
# ============================================================

pending_tasks = list_tasks()
completed_tasks = list_tasks(include_completed=True)

completed_tasks = [
    task
    for task in completed_tasks
    if task.get("completed")
]

if pending_tasks or completed_tasks:

    st.html(
        f"""
        <div class="panel">

            <div class="panel-header">

                <div>
                    <div class="panel-title">My Tasks</div>
                    <div class="panel-subtitle">
                        Things you want Swas Agent to keep track of
                    </div>
                </div>

                <div class="count-badge">
                    {len(pending_tasks)}
                </div>

            </div>

        """
    )

    # Pending tasks
    for task in pending_tasks:

        title = html.escape(str(task.get("title", "Untitled task")))
        task_id = task.get("id")
        due_date = html.escape(str(task.get("due_date") or "No due date"))
        priority = str(task.get("priority", "medium")).lower()

        st.html(
            f"""
            <div class="item-card">

                <div class="item-icon">✓</div>

                <div class="item-content">

                    <div class="item-name">
                        {title}
                    </div>

                    <div class="item-meta">
                        Due: {due_date}
                        &nbsp; • &nbsp;
                        Priority:
                        <span class="priority-{priority}">
                            {html.escape(priority)}
                        </span>
                    </div>

                </div>

            </div>
            """
        )

        task_col1, task_col2 = st.columns([1, 1])

        with task_col1:
            if st.button(
                "✓ Complete",
                key=f"complete_task_{task_id}",
                use_container_width=True,
            ):
                complete_task(task_id)
                st.rerun()

        with task_col2:
            if st.button(
                "Delete",
                key=f"delete_task_{task_id}",
                use_container_width=True,
            ):
                delete_task(task_id)
                st.rerun()

    # Completed tasks
    if completed_tasks:

        with st.expander(
            f"Completed tasks ({len(completed_tasks)})"
        ):

            for task in completed_tasks:

                title = html.escape(
                    str(task.get("title", "Untitled task"))
                )

                due_date = html.escape(
                    str(task.get("due_date") or "No due date")
                )

                task_id = task.get("id")

                st.html(
                    f"""
                    <div class="item-card completed-item">

                        <div class="item-icon">✓</div>

                        <div class="item-content">

                            <div class="item-name">
                                {title}
                            </div>

                            <div class="item-meta">
                                Completed • Due: {due_date}
                            </div>

                        </div>

                    </div>
                    """
                )

                if st.button(
                    "Delete",
                    key=f"delete_completed_task_{task_id}",
                    use_container_width=True,
                ):
                    delete_task(task_id)
                    st.rerun()

    st.html("</div>")


# ============================================================
# REMINDERS PANEL
# ============================================================

pending_reminders = list_reminders()

all_reminders = list_reminders(
    include_completed=True
)

completed_reminders = [
    reminder
    for reminder in all_reminders
    if reminder.get("completed")
]


if pending_reminders or completed_reminders:

    st.html(
        f"""
        <div class="panel">

            <div class="panel-header">

                <div>
                    <div class="panel-title">My Reminders</div>
                    <div class="panel-subtitle">
                        Swas Agent will keep your reminders organized
                    </div>
                </div>

                <div class="count-badge">
                    {len(pending_reminders)}
                </div>

            </div>

        """
    )

    # Pending reminders
    for reminder in pending_reminders:

        reminder_id = reminder.get("id")

        title = html.escape(
            str(reminder.get("title", "Untitled reminder"))
        )

        remind_at = html.escape(
            str(reminder.get("remind_at", "No time"))
        )

        st.html(
            f"""
            <div class="item-card">

                <div class="item-icon">⏰</div>

                <div class="item-content">

                    <div class="item-name">
                        {title}
                    </div>

                    <div class="item-meta">
                        Reminder: {remind_at}
                    </div>

                </div>

            </div>
            """
        )

        reminder_col1, reminder_col2 = st.columns([1, 1])

        with reminder_col1:
            if st.button(
                "✓ Dismiss",
                key=f"complete_reminder_{reminder_id}",
                use_container_width=True,
            ):
                complete_reminder(reminder_id)
                st.rerun()

        with reminder_col2:
            if st.button(
                "Delete",
                key=f"delete_reminder_{reminder_id}",
                use_container_width=True,
            ):
                delete_reminder(reminder_id)
                st.rerun()

    # Completed reminders
    if completed_reminders:

        with st.expander(
            f"Completed reminders ({len(completed_reminders)})"
        ):

            for reminder in completed_reminders:

                reminder_id = reminder.get("id")

                title = html.escape(
                    str(reminder.get("title", "Untitled reminder"))
                )

                remind_at = html.escape(
                    str(reminder.get("remind_at", "No time"))
                )

                st.html(
                    f"""
                    <div class="item-card completed-item">

                        <div class="item-icon">✓</div>

                        <div class="item-content">

                            <div class="item-name">
                                {title}
                            </div>

                            <div class="item-meta">
                                Completed • {remind_at}
                            </div>

                        </div>

                    </div>
                    """
                )

                if st.button(
                    "Delete",
                    key=f"delete_completed_reminder_{reminder_id}",
                    use_container_width=True,
                ):
                    delete_reminder(reminder_id)
                    st.rerun()

    st.html("</div>")


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


st.html(
    '<div class="chat-heading">Conversation</div>'
)


for message in st.session_state.messages:

    role = message.get("role", "assistant")

    avatar = (
        "🤖"
        if role == "assistant"
        else "👤"
    )

    with st.chat_message(
        role,
        avatar=avatar,
    ):
        st.markdown(
            message.get("content", "")
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message Swas Agent..."
)


# Quick prompt support
if (
    "quick_prompt" in st.session_state
    and st.session_state.quick_prompt
):

    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = None


# ============================================================
# PROCESS MESSAGE
# ============================================================

if prompt:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message(
        "user",
        avatar="👤",
    ):
        st.markdown(prompt)


    response = None
    tool_used = None
    tool_args = None


    # --------------------------------------------------------
    # RUN AGENT
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner("Swas is thinking..."):

            try:

                result = run_agent(prompt)

                # Support normal dictionary response
                if isinstance(result, dict):

                    response = result.get(
                        "response"
                    )

                    tool_used = result.get(
                        "tool"
                    )

                    tool_args = result.get(
                        "tool_args"
                    )

                # Support plain string response
                elif isinstance(result, str):

                    response = result

                else:

                    response = str(result)


            except Exception as error:

                error_text = str(error)

                if (
                    "429" in error_text
                    or "quota" in error_text.lower()
                    or "too_many_requests"
                    in error_text.lower()
                ):

                    response = (
                        "⚠️ Gemini's current request limit "
                        "has been reached. Your local tools "
                        "are still safe and working. Please "
                        "wait a little and try again."
                    )

                else:

                    response = (
                        f"❌ Something went wrong: "
                        f"{error_text}"
                    )


        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        if not response:

            response = (
                "I couldn't generate a response right now."
            )


        # ----------------------------------------------------
        # SHOW RESPONSE
        # ----------------------------------------------------

        st.markdown(response)


        # ----------------------------------------------------
        # TOOL ACTIVITY
        # ----------------------------------------------------

        activity_map = {

            "calculator": (
                "🧮 Calculator",
                "Swas used the calculator tool."
            ),

            "create_calendar_event": (
                "📅 Google Calendar",
                "Swas created a calendar event."
            ),

            "add_task": (
                "✓ Task Manager",
                "Swas added a new task."
            ),

            "list_tasks": (
                "📋 Task Manager",
                "Swas checked your tasks."
            ),

            "complete_task": (
                "✓ Task Manager",
                "Swas completed a task."
            ),

            "delete_task": (
                "🗑 Task Manager",
                "Swas deleted a task."
            ),

            "add_reminder": (
                "⏰ Reminder Manager",
                "Swas created a reminder."
            ),

            "list_reminders": (
                "⏰ Reminder Manager",
                "Swas checked your reminders."
            ),

            "complete_reminder": (
                "✓ Reminder Manager",
                "Swas dismissed a reminder."
            ),

            "delete_reminder": (
                "🗑 Reminder Manager",
                "Swas deleted a reminder."
            ),

        }


        if tool_used in activity_map:

            activity_title, activity_text = (
                activity_map[tool_used]
            )

            st.html(
                f"""
                <div class="activity">

                    <div class="activity-title">
                        {html.escape(activity_title)}
                    </div>

                    <div class="activity-text">
                        {html.escape(activity_text)}
                    </div>

                </div>
                """
            )


    # ========================================================
    # SAVE ASSISTANT MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        SWAS AGENT • PERSONAL AI • BUILT BY SWASTIK
    </div>
    """
) 