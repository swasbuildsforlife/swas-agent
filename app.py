import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)

print("=" * 50)
print("🤖 SWAS AGENT")
print("Your personal AI Agent")
print("=" * 50)
print("Type 'exit' to stop the agent.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("🤖 Agent: Goodbye bhai! 👋")
        break

    if not user_input.strip():
        continue

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=user_input
        )

        print("🤖 Agent:", interaction.output_text)
        print()

    except Exception as e:
        print("❌ Error:", e)
        print()