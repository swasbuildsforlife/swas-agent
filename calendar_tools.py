import os
import pickle
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from google.auth.transport.requests import Request


TOKEN_FILE = "calendar_token.pkl"


def get_calendar_service():
    """Load saved Google credentials and create Calendar service."""

    if not os.path.exists(TOKEN_FILE):
        raise Exception(
            "Google Calendar is not connected. Run calendar_auth.py first."
        )

    with open(TOKEN_FILE, "rb") as token:
        credentials = pickle.load(token)

    # Refresh expired credentials automatically
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build(
        "calendar",
        "v3",
        credentials=credentials
    )


def create_calendar_event(
    title: str,
    start_time: str,
    duration_minutes: int = 60,
    description: str = ""
):
    """
    Create a Google Calendar event.

    start_time format:
    YYYY-MM-DD HH:MM

    Example:
    2026-09-15 17:00
    """

    try:
        service = get_calendar_service()

        start = datetime.strptime(
            start_time,
            "%Y-%m-%d %H:%M"
        )

        end = start + timedelta(
            minutes=duration_minutes
        )

        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end.isoformat(),
                "timeZone": "Asia/Kolkata"
            }
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return {
            "success": True,
            "title": created_event.get("summary"),
            "start": start.strftime("%d %b %Y, %I:%M %p"),
            "end": end.strftime("%I:%M %p"),
            "event_id": created_event.get("id"),
            "link": created_event.get("htmlLink")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------
# DIRECT TEST
# -----------------------------

if __name__ == "__main__":

    print("📅 Testing Google Calendar connection...")

    result = create_calendar_event(
        title="Swas Agent Test Event",
        start_time="2026-09-15 17:00",
        duration_minutes=30,
        description="Test event created by Swas Agent."
    )

    print("\nResult:")

    if result["success"]:
        print("✅ Event created successfully!")
        print("📌 Title:", result["title"])
        print("🕐 Start:", result["start"])
        print("🕐 End:", result["end"])
        print("🔗 Calendar:", result["link"])
    else:
        print("❌ Error:", result["error"])