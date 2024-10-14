import os

# GitHub API URL for the repository
GIT_API_URL = "https://api.github.com/repos/Lilypad-Tech/lilypad/issues"

# Discord webhook URL (you can set your actual webhook URL here)
OSS_DISCORD_WEBHOOK = os.getenv('OSS_DISCORD_WEBHOOK')
POW_MONITORING_WEBHOOK = os.getenv('POW_DISCORD_WEBHOOK')
AMBASSADOR_REMINDER_WEBHOOK = os.getenv('AMBASSADOR_REMINDER_DISCORD_WEBHOOK')
LOGS_BOT_TOKEN = os.getenv('LOGS_BOT_TOKEN')

# Discord Roles
LILYTEAM_DISCORD_ROLE = "<@&1212902935969669140>"
LILYPAD_ADVOCATE_DISCORD_ROLE = "<@&1255696024161226783>"

# Arbiscan
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ARBISCAN_API_ENDPOINT = f'https://api-sepolia.arbiscan.io/api'
ARBISCAN_ADDRESS_URL = "https://sepolia.arbiscan.io/address/"

# Lilypad Addresses
POW_CONTRACT_ADDRESS = "0x8b852ba45293d6dd51b10c57625c6c5f25adfb40"
POW_CONTRACT_ADDRESS_METHOD = "0xda8accf9"
POW_SIGNAL_CRON_ADDRESS = "0xd10d15cc705f7d2558352b1212a9b3685155d93d"
POW_SIGNAL_CRON_ADDRESS_METHOD = "0xb681f2fd"
