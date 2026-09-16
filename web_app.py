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
# PREMIUM CRIMSON × VIOLET UI
# ============================================================

st.html(
    """
    <style>

    /* ========================================================
       COLOR SYSTEM
       ======================================================== */

    :root {
        --black: #070609;
        --plum: #160B18;
        --crimson-violet: #7F1D5A;
        --red: #E11D48;
        --violet: #A855F7;
        --text: #F5F5F5;
        --muted: #817985;
        --soft: #B8AFBA;
    }


    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                rgba(168, 85, 247, 0.12),
                transparent 35%
            ),
            radial-gradient(
                circle at 5% 25%,
                rgba(127, 29, 90, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 75%,
                rgba(225, 29, 72, 0.05),
                transparent 25%
            ),
            #070609;

        color: #F5F5F5;
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
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
    }


    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 8px 3px 18px 3px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        width: 40px;
        height: 40px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background:
            linear-gradient(
                135deg,
                #A855F7 0%,
                #7F1D5A 58%,
                #E11D48 100%
            );

        color: #FFFFFF;

        font-size: 20px;
        font-weight: 800;

        box-shadow:
            0 8px 30px rgba(168, 85, 247, 0.22),
            0 0 0 1px rgba(168, 85, 247, 0.15);
    }

    .brand-title {
        color: #F5F5F5;

        font-size: 18px;
        font-weight: 750;

        letter-spacing: -0.4px;
        line-height: 1.1;
    }

    .brand-subtitle {
        margin-top: 4px;

        color: #756D78;

        font-size: 9px;
        font-weight: 700;

        letter-spacing: 1.8px;
    }

    .online-status {
        display: flex;
        align-items: center;
        gap: 8px;

        padding: 7px 12px;

        border-radius: 999px;

        background: rgba(22, 11, 24, 0.72);

        border: 1px solid rgba(168, 85, 247, 0.14);

        color: #A8A0AB;

        font-size: 10px;
        font-weight: 600;
    }

    .online-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #A855F7;

        box-shadow:
            0 0 8px rgba(168, 85, 247, 0.9),
            0 0 18px rgba(168, 85, 247, 0.35);
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        text-align: center;

        padding: 62px 20px 34px 20px;
    }

    .hero h1 {
        margin: 0;

        color: #F5F5F5;

        font-size: clamp(36px, 5.2vw, 58px);

        line-height: 1.02;

        font-weight: 780;

        letter-spacing: -3px;
    }

    .hero h1 span {
        background:
            linear-gradient(
                90deg,
                #A855F7 0%,
                #C084FC 45%,
                #E11D48 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        max-width: 650px;

        margin: 18px auto 0 auto;

        color: #817A86;

        font-size: 14px;

        line-height: 1.75;
    }


    /* ========================================================
       QUICK ACTIONS
       ======================================================== */

    .quick-title {
        margin: 8px 0 11px 2px;

        color: #756D78;

        font-size: 10px;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 1.6px;
    }

    div.stButton > button {
        min-height: 46px;

        border-radius: 14px;

        border: 1px solid rgba(168, 85, 247, 0.13);

        background:
            linear-gradient(
                145deg,
                rgba(22, 11, 24, 0.92),
                rgba(11, 7, 13, 0.92)
            );

        color: #C9C2CC;

        font-size: 12px;
        font-weight: 600;

        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.025);

        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            background 0.18s ease,
            box-shadow 0.18s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        border-color: rgba(168, 85, 247, 0.42);

        background:
            linear-gradient(
                145deg,
                rgba(42, 17, 45, 0.96),
                rgba(18, 9, 21, 0.96)
            );

        color: #FFFFFF;

        box-shadow:
            0 10px 30px rgba(168, 85, 247, 0.10);
    }


    /* ========================================================
       PANELS
       ======================================================== */

    .panel {
        margin-top: 30px;

        padding: 21px;

        border-radius: 20px;

        border: 1px solid rgba(168, 85, 247, 0.105);

        background:
            linear-gradient(
                145deg,
                rgba(22, 11, 24, 0.88),
                rgba(10, 7, 12, 0.84)
            );

        box-shadow:
            0 24px 70px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.018);

        backdrop-filter: blur(18px);
    }

    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 16px;
    }

    .panel-title {
        color: #F5F5F5;

        font-size: 16px;
        font-weight: 720;

        letter-spacing: -0.3px;
    }

    .panel-subtitle {
        margin-top: 4px;

        color: #756D78;

        font-size: 10px;

        line-height: 1.5;
    }

    .count-badge {
        min-width: 28px;

        padding: 5px 9px;

        text-align: center;

        border-radius: 999px;

        background: rgba(168, 85, 247, 0.10);

        border: 1px solid rgba(168, 85, 247, 0.14);

        color: #C084FC;

        font-size: 10px;
        font-weight: 750;
    }


    /* ========================================================
       TASK / REMINDER CARDS
       ======================================================== */

    .item-card {
        display: flex;
        align-items: center;

        gap: 13px;

        padding: 13px 14px;

        margin-bottom: 9px;

        border-radius: 14px;

        border: 1px solid rgba(168, 85, 247, 0.075);

        background: rgba(7, 6, 9, 0.60);

        transition:
            border-color 0.18s ease,
            background 0.18s ease;
    }

    .item-card:hover {
        border-color: rgba(168, 85, 247, 0.18);

        background: rgba(22, 11, 24, 0.72);
    }

    .item-icon {
        width: 31px;
        height: 31px;

        flex: 0 0 31px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 10px;

        background: rgba(168, 85, 247, 0.10);

        border: 1px solid rgba(168, 85, 247, 0.10);

        color: #C084FC;

        font-size: 13px;
    }

    .item-content {
        min-width: 0;
        flex: 1;
    }

    .item-name {
        color: #EDE9F0;

        font-size: 13px;
        font-weight: 620;

        word-break: break-word;
    }

    .item-meta {
        margin-top: 4px;

        color: #706875;

        font-size: 10px;
    }

    .priority-high {
        color: #FB7185;
    }

    .priority-medium {
        color: #C084FC;
    }

    .priority-low {
        color: #A78BFA;
    }

    .completed-item {
        opacity: 0.48;
    }

    .completed-item .item-name {
        text-decoration: line-through;
    }


    /* ========================================================
       CHAT
       ======================================================== */

    .chat-heading {
        margin-top: 42px;
        margin-bottom: 13px;

        color: #756D78;

        font-size: 10px;
        font-weight: 700;

        text-transform: uppercase;
        letter-spacing: 1.6px;
    }

    [data-testid="stChatMessage"] {
        margin-bottom: 10px;

        border-radius: 17px;

        border: 1px solid rgba(168, 85, 247, 0.07);

        background: rgba(22, 11, 24, 0.38);

        backdrop-filter: blur(12px);
    }

    [data-testid="stChatMessage"] p {
        color: #E8E3E9;
    }

    [data-testid="stChatInput"] {
        margin-top: 17px;
    }

    [data-testid="stChatInput"] > div {
        border-radius: 17px;

        border: 1px solid rgba(168, 85, 247, 0.18);

        background: rgba(22, 11, 24, 0.90);

        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.28),
            0 0 25px rgba(168, 85, 247, 0.035);

        backdrop-filter: blur(16px);
    }

    [data-testid="stChatInput"] textarea {
        color: #F5F5F5 !important;

        background: transparent !important;

        border: none !important;

        font-size: 13px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #6F6873 !important;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        border: 1px solid rgba(168, 85, 247, 0.08);

        border-radius: 13px;

        background: rgba(7, 6, 9, 0.42);
    }


    /* ========================================================
       ACTIVITY
       ======================================================== */

    .activity {
        margin-top: 16px;

        padding: 14px 15px;

        border-radius: 14px;

        border: 1px solid rgba(168, 85, 247, 0.12);

        background:
            linear-gradient(
                135deg,
                rgba(127, 29, 90, 0.12),
                rgba(22, 11, 24, 0.58)
            );
    }

    .activity-title {
        color: #C084FC;

        font-size: 10px;

        font-weight: 750;

        letter-spacing: 1px;

        text-transform: uppercase;
    }

    .activity-text {
        margin-top: 6px;

        color: #928A96;

        font-size: 11px;

        line-height: 1.7;
    }

    .activity-text strong {
        color: #E9D5FF;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .topbar {
            padding-left: 2px;
            padding-right: 2px;
        }

        .brand-title {
            font-size: 16px;
        }

        .online-status {
            padding: 6px 9px;
        }

        .hero {
            padding-top: 38px;
        }

        .hero h1 {
            font-size: 37px;
            letter-spacing: -2px;
        }

        .hero p {
            font-size: 13px;
        }

        .panel {
            padding: 15px;
            border-radius: 17px;
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

            <div class="brand-icon">
                ✦
            </div>

            <div>
                <div class="brand-title">
                    Swas Agent
                </div>

                <div class="brand-subtitle">
                    PERSONAL AI
                </div>
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
            Your personal AI assistant for questions,
            calculations, tasks, reminders and scheduling.
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

    if st.button(
        "💬  Ask anything",
        use_container_width=True,
    ):
        st.session_state.quick_prompt = (
            "What can you help me with?"
        )


with quick_col2:

    if st.button(
        "📅  Schedule something",
        use_container_width=True,
    ):
        st.session_state.quick_prompt = (
            "Help me schedule something on my Google Calendar."
        )


with quick_col3:

    if st.button(
        "🧮  Calculate",
        use_container_width=True,
    ):
        st.session_state.quick_prompt = (
            "Calculate 4589 * 27 + 156"
        )


# ============================================================
# TASKS
# ============================================================

pending_tasks = list_tasks()

completed_tasks = list_tasks(
    include_completed=True
)

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

                    <div class="panel-title">
                        My Tasks
                    </div>

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


    # --------------------------------------------------------
    # PENDING TASKS
    # --------------------------------------------------------

    for task in pending_tasks:

        title = html.escape(
            str(
                task.get(
                    "title",
                    "Untitled task"
                )
            )
        )

        task_id = task.get("id")

        due_date = html.escape(
            str(
                task.get("due_date")
                or "No due date"
            )
        )

        priority = str(
            task.get(
                "priority",
                "medium"
            )
        ).lower()


        st.html(
            f"""
            <div class="item-card">

                <div class="item-icon">
                    ✓
                </div>

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


        task_col1, task_col2 = st.columns(2)


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


    # --------------------------------------------------------
    # COMPLETED TASKS
    # --------------------------------------------------------

    if completed_tasks:

        with st.expander(
            f"Completed tasks ({len(completed_tasks)})"
        ):

            for task in completed_tasks:

                title = html.escape(
                    str(
                        task.get(
                            "title",
                            "Untitled task"
                        )
                    )
                )

                due_date = html.escape(
                    str(
                        task.get("due_date")
                        or "No due date"
                    )
                )

                task_id = task.get("id")


                st.html(
                    f"""
                    <div class="item-card completed-item">

                        <div class="item-icon">
                            ✓
                        </div>

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
# REMINDERS
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

                    <div class="panel-title">
                        My Reminders
                    </div>

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


    # --------------------------------------------------------
    # PENDING REMINDERS
    # --------------------------------------------------------

    for reminder in pending_reminders:

        reminder_id = reminder.get("id")

        title = html.escape(
            str(
                reminder.get(
                    "title",
                    "Untitled reminder"
                )
            )
        )

        remind_at = html.escape(
            str(
                reminder.get(
                    "remind_at",
                    "No time"
                )
            )
        )


        st.html(
            f"""
            <div class="item-card">

                <div class="item-icon">
                    ⏰
                </div>

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


        reminder_col1, reminder_col2 = st.columns(2)


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


    # --------------------------------------------------------
    # COMPLETED REMINDERS
    # --------------------------------------------------------

    if completed_reminders:

        with st.expander(
            f"Completed reminders ({len(completed_reminders)})"
        ):

            for reminder in completed_reminders:

                reminder_id = reminder.get("id")

                title = html.escape(
                    str(
                        reminder.get(
                            "title",
                            "Untitled reminder"
                        )
                    )
                )

                remind_at = html.escape(
                    str(
                        reminder.get(
                            "remind_at",
                            "No time"
                        )
                    )
                )


                st.html(
                    f"""
                    <div class="item-card completed-item">

                        <div class="item-icon">
                            ✓
                        </div>

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

    role = message.get(
        "role",
        "assistant"
    )

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
            message.get(
                "content",
                ""
            )
        )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Message Swas Agent..."
)


# ============================================================
# QUICK PROMPT SUPPORT
# ============================================================

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

    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

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

    tools_used = []
    tool_results = []


    # --------------------------------------------------------
    # RUN AGENT
    # --------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "Swas is thinking..."
        ):

            try:

                result = run_agent(prompt)


                # ------------------------------------------------
                # DICTIONARY RESULT
                # ------------------------------------------------

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

                    tools_used = result.get(
                        "tools_used",
                        []
                    ) or []

                    tool_results = result.get(
                        "tool_results",
                        []
                    ) or []


                # ------------------------------------------------
                # STRING RESULT
                # ------------------------------------------------

                elif isinstance(result, str):

                    response = result


                # ------------------------------------------------
                # OTHER RESULT
                # ------------------------------------------------

                else:

                    response = str(result)


            except Exception as error:

                error_text = str(error)


                # --------------------------------------------
                # GEMINI QUOTA
                # --------------------------------------------

                if (
                    "429" in error_text
                    or "quota" in error_text.lower()
                    or "too_many_requests"
                    in error_text.lower()
                ):

                    response = (
                        "⚠️ Gemini's current request limit "
                        "has been reached.\n\n"
                        "Your local tools are still safe "
                        "and working. Please wait a little "
                        "and try again."
                    )


                # --------------------------------------------
                # OTHER ERROR
                # --------------------------------------------

                else:

                    response = (
                        "❌ Something went wrong:\n\n"
                        f"{error_text}"
                    )


        # ====================================================
        # TOOL RESULT FALLBACK
        # ====================================================

        if not response:

            successful = []
            failed = []


            for item in tool_results:

                if not isinstance(item, dict):
                    continue


                tool_name = (
                    item.get("tool")
                    or item.get("name")
                    or "tool"
                )


                result_text = item.get(
                    "result"
                )


                if result_text is None:

                    result_text = item.get(
                        "output"
                    )


                if result_text is None:

                    result_text = ""


                result_text = str(
                    result_text
                )


                if (
                    "error" in result_text.lower()
                    or "failed" in result_text.lower()
                ):

                    failed.append(
                        f"{tool_name}: {result_text}"
                    )

                else:

                    successful.append(
                        f"{tool_name}: {result_text}"
                    )


            if successful and not failed:

                response = (
                    "Done — the requested action "
                    "was completed.\n\n"
                    + "\n".join(successful)
                )


            elif successful and failed:

                response = (
                    "The request was partially "
                    "completed.\n\n"
                    "**Completed:**\n"
                    + "\n".join(successful)
                    + "\n\n"
                    "**Issues:**\n"
                    + "\n".join(failed)
                )


            elif failed:

                response = (
                    "I couldn't complete the "
                    "requested action.\n\n"
                    + "\n".join(failed)
                )


        # ====================================================
        # FINAL FALLBACK
        # ====================================================

        if not response:

            response = (
                "I couldn't generate a response right now."
            )


        # ====================================================
        # SHOW RESPONSE
        # ====================================================

        st.markdown(response)


        # ====================================================
        # TOOL ACTIVITY
        # ====================================================

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
                "🗑 Task Manager",
                "Swas deleted a reminder."
            ),
        }


        activity_names = tools_used or (
            [tool_used]
            if tool_used
            else []
        )


        shown_tools = []


        for name in activity_names:

            if (
                name in activity_map
                and name not in shown_tools
            ):

                shown_tools.append(name)


        if shown_tools:

            activity_lines = []


            for name in shown_tools:

                activity_title, activity_text = (
                    activity_map[name]
                )


                activity_lines.append(
                    f"""
                    <div>
                        <strong>
                            {html.escape(activity_title)}
                        </strong>
                        <br>
                        {html.escape(activity_text)}
                    </div>
                    """
                )


            st.html(
                f"""
                <div class="activity">

                    <div class="activity-title">
                        Swas activity
                    </div>

                    <div class="activity-text">
                        {"<br><br>".join(activity_lines)}
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