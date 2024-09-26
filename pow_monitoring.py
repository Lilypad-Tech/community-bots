import requests
from datetime import datetime, timezone
from utils.discord import send_discord_message
from vars import (
    POW_MONITORING_WEBHOOK, 
    LILYTEAM_DISCORD_ROLE, 
    LILYPAD_ADVOCATE_DISCORD_ROLE, 
    POW_CONTRACT_ADDRESS, 
    POW_CONTRACT_ADDRESS_URL, 
    ARBISCAN_API_KEY, 
    ARBISCAN_API_ENDPOINT
)

# Constants to set the warning and error thresholds for time since the last transaction
warning_threshold_minutes = 60  # Time in minutes to trigger a warning
error_threshold_minutes = 120  # Time in minutes to trigger an error

# Discord roles that will be tagged in the message
discord_roles = f"{LILYTEAM_DISCORD_ROLE}, {LILYPAD_ADVOCATE_DISCORD_ROLE}"

def get_latest_transaction_time():
    """
    Fetch the latest transaction timestamp from the Etherscan API for the given contract address.
    Returns the timestamp as a datetime object if successful, or None if an error occurs.
    """
    # Parameters for querying the Etherscan API to get the list of transactions for a specific address
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': POW_CONTRACT_ADDRESS,  # Contract address for the Lilypad POW
        'startblock': 0,  # Start from the first block
        'endblock': 99999999,  # End at the latest block
        'sort': 'desc',  # Sort transactions by newest first
        'apikey': ARBISCAN_API_KEY  # API key for authenticating the request
    }
    
    # Make the request to Etherscan API
    response = requests.get(ARBISCAN_API_ENDPOINT, params=params)
    
    if response.status_code == 200:  # Check if the API call was successful
        data = response.json()  # Parse the JSON response
        
        # If status is '1' (success) and transactions are available
        if data['status'] == '1' and len(data['result']) > 0:
            latest_tx = data['result'][0]  # Get the latest transaction (first one in the sorted list)
            timestamp = int(latest_tx['timeStamp'])  # Extract the timestamp from the transaction data
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)  # Convert timestamp to datetime object
        else:
            print("No transactions found for this address.")
            return None
    else:
        # Print an error message if the API request fails
        print("Error fetching data from Etherscan.")
        return None

def format_time_difference(seconds):
    """
    Format the time difference in seconds into a more human-readable form (minutes and seconds).
    """
    minutes = seconds // 60  # Convert total seconds to minutes
    remaining_seconds = seconds % 60  # Get the remaining seconds after the minutes
    return f"{int(minutes)} minutes and {int(remaining_seconds)} seconds"  # Return formatted string

def monitor_transactions():
    """
    Monitors the latest transaction time of the Lilypad POW contract. 
    Sends a Discord message if the time since the last transaction exceeds specified thresholds.
    """
    # Get the timestamp of the latest transaction
    latest_transaction_time = get_latest_transaction_time()
    
    if latest_transaction_time is None:  # Exit if there was an issue fetching the transaction
        return
    
    # Get the current time in UTC
    current_time = datetime.now(timezone.utc)
    
    # Calculate the difference between the current time and the time of the last transaction
    time_diff = current_time - latest_transaction_time
    total_seconds_since_last_tx = time_diff.total_seconds()  # Get the difference in total seconds

    # Info message to include with the alerts, contains the contract URL and Discord roles to tag
    info_message = f"Lilypad POW Contract Address: {POW_CONTRACT_ADDRESS_URL}"
    
    # Check if the time since the last transaction exceeds the error threshold
    if total_seconds_since_last_tx > error_threshold_minutes * 60:
        error_message = f"**ERROR**: Last transaction was {format_time_difference(total_seconds_since_last_tx)} ago"
        print(error_message)  # Print error message
        # Send an error alert to the specified Discord webhook
        send_discord_message(POW_MONITORING_WEBHOOK, f"🔴 {error_message} \n {info_message}")
        
    # Check if the time since the last transaction exceeds the warning threshold
    elif total_seconds_since_last_tx > warning_threshold_minutes * 60:
        warning_message = f"**WARNING**: Last transaction was {format_time_difference(total_seconds_since_last_tx)} ago"
        print(warning_message)  # Print warning message
        # Send a warning alert to the specified Discord webhook
        send_discord_message(POW_MONITORING_WEBHOOK, f"⚠️ {warning_message} \n {info_message}")
    
    else:
        # If the time since the last transaction is within acceptable limits
        ok_message = f"**OK**: Last transaction was {format_time_difference(total_seconds_since_last_tx)} ago."
        print(ok_message)  # Print OK message
        # Send an OK alert to the specified Discord webhook
        # send_discord_message(POW_MONITORING_WEBHOOK, f"🟢 {ok_message}")

# If this script is run directly, call the monitor_transactions function
if __name__ == "__main__":
    monitor_transactions()