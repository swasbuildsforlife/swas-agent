import os
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ Google OAuth credentials missing in .env")
    exit()

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

TOKEN_FILE = "calendar_token.pkl"


# -----------------------------
# LOAD EXISTING TOKEN
# -----------------------------
if os.path.exists(TOKEN_FILE):
    print("🔑 Existing Google Calendar login found.")
    print("✅ No new Google login required.")

else:
    print("🔐 Opening Google login...")

    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }

    flow = InstalledAppFlow.from_client_config(
        client_config,
        SCOPES
    )

    credentials = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "wb") as token:
        pickle.dump(credentials, token)

    print("\n✅ Google Calendar authorization successful!")
    print("💾 Login saved locally.")