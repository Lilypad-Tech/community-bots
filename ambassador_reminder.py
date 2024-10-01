import os
from utils.discord import send_discord_message
from datetime import datetime, timezone
from vars import AMBASSADOR_REMINDER_WEBHOOK


def send_ambassador_reminder():
    """
    Sends a reminder for the ambassador program to the Lilypad general Discord channel.
    """
    announcement = """
🌟 Lilypad Ambassador Program Reminder 🌟

Hey Lilypad community! 👋

Just a friendly reminder about the Lilypad Ambassador Program! We're always on the lookout for passionate individuals to join our team of ambassadors.

🔑 Key Points to Remember:
The program is designed for our most engaged and enthusiastic community members.
Your level of activity and contributions in the community directly impacts your chances of being selected.

🏆 How to Increase Your Chances:
- Stay active in discussions
- Contribute feedback, issues and pull requests to Lilypad's open source repos
- Help other community members
- Share creative ideas and feedback
- Contribute to Lilypad's growth (e.g., documentation, tutorials, bug reports)
- Spread the word about Lilypad on social media and in tech communities

Remember, we're not just looking for quantity, but quality of engagement. Thoughtful, constructive, and consistent participation is what catches our eye! 👀

🚀 The more you contribute, the more you stand out!

Interested in becoming an ambassador? Keep up your amazing work in the community, and you might just be asked to join the program!

Let's continue building and growing together! 🌱💪
"""
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Sending announcement at {current_time} UTC")

    try:
        send_discord_message(AMBASSADOR_REMINDER_WEBHOOK, announcement)
        print("Announcement sent successfully!")
    except Exception as e:
        print(f"Failed to send announcement: {e}")


def main():
    send_ambassador_reminder()


if __name__ == "__main__":
    main()
