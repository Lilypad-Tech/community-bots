from utils.discord import send_discord_message
from datetime import datetime, timezone
from vars import SUPPORT_REMINDER_DISCORD_WEBHOOK


def send_support_reminder():
    """
    Sends a reminder for the Lilypad support channels on GitHub.
    """
    announcement = """
🌟 Lilypad GitHub Support Reminder 🌟

Hey Lilypad community! 👋

Just a quick reminder about how to effectively troubleshoot and push inquiries forward:

🔗 **Use GitHub Discussions**:  
    For any technical issues, troubleshooting, or general questions, 
    our GitHub Discussions channels are the go-to place to connect with the team and other community members. 
    
    Any support issues brought up in the General Discord channel will be deleted.

📋 **Where to Post:**
    - **Complex Issues**: Start a new discussion using the [`rp-issue`](https://github.com/orgs/Lilypad-Tech/discussions/categories/rp-issue) template if you're a resource provider or need technical assistance.

    - **General Questions**: Share your thoughts in a general discussion or the [#i-need-help channel](https://discord.com/channels/1212897693450641498/1230231823674642513) on Discord.

🛠️ **Why GitHub Discussions?**
  - It keeps conversations organized and accessible for everyone.

  - It helps the team track, prioritize, and resolve issues effectively.

  - Your feedback contributes directly to improving Lilypad!

🚀 **Pro Tip**: Always provide as much detail as possible (e.g., steps to reproduce, error messages, setup configurations). The more context, the quicker we can help!

Thank you for keeping Lilypad running smoothly by sharing your insights and helping us troubleshoot together. Let’s continue building a stronger community! 💪✨
"""

    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Sending announcement at {current_time} UTC")

    try:
        send_discord_message(SUPPORT_REMINDER_DISCORD_WEBHOOK, announcement)
        print("Announcement sent successfully!")
    except Exception as e:
        print(f"Failed to send announcement: {e}")


def main():
    send_support_reminder()


if __name__ == "__main__":
    main()
