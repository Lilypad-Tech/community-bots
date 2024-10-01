import os

# GitHub API URL for the repository
GIT_API_URL = "https://api.github.com/repos/Lilypad-Tech/lilypad/issues"

# Discord webhook URL (you can set your actual webhook URL here)
OSS_DISCORD_WEBHOOK = os.getenv('OSS_DISCORD_WEBHOOK')
POW_MONITORING_WEBHOOK = os.getenv('POW_DISCORD_WEBHOOK')
AMBASSADOR_REMINDER_WEBHOOK = os.getenv('AMBASSADOR_REMINDER_DISCORD_WEBHOOK')
# Discord Roles
LILYTEAM_DISCORD_ROLE = "<@&1212902935969669140>"
LILYPAD_ADVOCATE_DISCORD_ROLE = "<@&1255696024161226783>"

# Arbiscan
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ARBISCAN_API_ENDPOINT = f'https://api-sepolia.arbiscan.io/api'
POW_CONTRACT_ADDRESS = "0x8b852ba45293d6dd51b10c57625c6c5f25adfb40"
POW_CONTRACT_ADDRESS_URL = f"https://sepolia.arbiscan.io/address/{
    POW_CONTRACT_ADDRESS}"
