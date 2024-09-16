from collections import defaultdict
from utils.git import fetch_all_issues
from utils.discord import send_discord_message
from vars import DISCORD_WEBHOOK, GIT_API_URL

# GitHub 
params_closed = {'state': 'closed', 'per_page': 100, 'page': 1}

# Assign badges based on the number of issues solved
def assign_badge(count):
    if count >= 10:
        return "🥇 Gold Contributor"
    elif count >= 6:
        return "🥈 Silver Contributor"
    elif count >= 3:
        return "🥉 Bronze Contributor"
    elif count >= 1:
        return "⭐ Rising Star"
    else:
        return "🌱 New Contributor"

# Define milestones based on the current number of issues solved
def next_milestone(count):
    if count == 0:
        return 1  # Next milestone for new contributor
    elif count < 3:
        return 3  # Next milestone for Rising Star
    elif count < 6:
        return 6  # Next milestone for Bronze Contributor
    elif count < 10:
        return 10  # Next milestone for Silver Contributor
    else:
        return None  # No milestone after reaching Gold

# Progress bar function with badge milestones
def progress_bar(current, total):
    if total is None:  # No further milestones for Gold Contributors
        return "🎉 Max level achieved!"
    progress = int((current / total) * 10)  # A 10-step progress bar for visual clarity
    return f"{'▓' * progress}{'░' * (10 - progress)} ({current}/{total} to next badge)"

# Add milestones, badges, and progress bars to leaderboard with the badge-specific milestones
def format_leaderboard_with_progress(sorted_assignees):
    if sorted_assignees:
        message = ["**🏆 Leaderboard - Top Issue Solvers**:\n"]
        for i, (assignee, count) in enumerate(sorted_assignees, 1):
            milestone = next_milestone(count)
            progress = progress_bar(count, milestone)
            badge = assign_badge(count)  # Get badge based on issues solved
            trophy = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "⭐"
            message.append(f"{trophy} **{assignee}**: {count} issue(s) solved | {progress} | {badge}")
        return '\n'.join(message)
    else:
        return "No community-labeled issues have been solved by any assignees."

# Fetch closed issues and build the leaderboard
def generate_leaderboard():
    closed_issues = fetch_all_issues(GIT_API_URL, params_closed)
    solved_issues_by_assignee = defaultdict(int)

    for issue in closed_issues:
        labels = [label['name'].lower() for label in issue.get('labels', [])]
        has_community_tag = 'community' in labels

        if has_community_tag:
            assignees = [assignee['login'] for assignee in issue.get('assignees', [])]
            for assignee in assignees:
                solved_issues_by_assignee[assignee] += 1  # Count how many issues each assignee has solved

    # Sort the assignees by the number of solved issues (in descending order)
    sorted_assignees = sorted(solved_issues_by_assignee.items(), key=lambda x: x[1], reverse=True)

    leaderboard_message = format_leaderboard_with_progress(sorted_assignees)
    send_discord_message(DISCORD_WEBHOOK, leaderboard_message)
    
generate_leaderboard()
