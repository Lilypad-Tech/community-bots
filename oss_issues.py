import random
from utils.git import fetch_all_issues
from utils.discord import send_discord_message
from vars import OSS_DISCORD_WEBHOOK, GIT_API_URL

# GitHub 
params_open = {'state': 'open', 'per_page': 100, 'page': 1}

# Load encouragement messages from file
def load_encouragement_messages(filename):
    with open(filename, 'r') as file:
        messages = file.readlines()
    return [message.strip() for message in messages if message.strip()]

# Format the message to send to Discord (for open issues)
def format_issues(issues, status):
    if issues:
        message = [f"{status} community issues:"]
        for i, issue in enumerate(issues, 1):
            assignees = ', '.join(issue['assignees'])
            message.append(f"{i}. [{issue['title']}](<{issue['url']}>) ({assignees})")
        return '\n'.join(message)
    else:
        return f"No {status.lower()} community issues:"

def process_open_issues():
    open_issues = fetch_all_issues(GIT_API_URL, params_open)
    
    community_assigned_issues = []
    community_unassigned_issues = []

    for issue in open_issues:
        labels = [label['name'].lower() for label in issue.get('labels', [])]
        has_community_tag = 'community' in labels

        issue_title = issue.get('title', '').strip()
        issue_url = issue.get('html_url', '')

        assignees = [assignee['login'] for assignee in issue.get('assignees', [])]
        assignee_names = assignees if assignees else ["Unassigned"]

        if has_community_tag:
            if assignee_names == ["Unassigned"]:
                community_unassigned_issues.append({
                    'title': issue_title,
                    'url': issue_url,
                    'assignees': assignee_names
                })
            else:
                community_assigned_issues.append({
                    'title': issue_title,
                    'url': issue_url,
                    'assignees': assignee_names
                })

    # Choose a random encouragement message
    encouragement_messages = load_encouragement_messages('oss_encouragement_messages.txt')
    encouragement_message = random.choice(encouragement_messages)

    # Prepare the content for Discord message (for open issues)
    open_issues_message = (encouragement_message + "\n\n" +
                           format_issues(community_unassigned_issues, "**Unassigned**") +
                           "\n\n" +
                           format_issues(community_assigned_issues, "**Assigned**"))

    send_discord_message(OSS_DISCORD_WEBHOOK, open_issues_message)
    
# Process open issues
process_open_issues()