import requests
from datetime import datetime, timezone
from utils.discord import send_discord_message
from vars import (
    POW_MONITORING_WEBHOOK, 
    LILYTEAM_DISCORD_ROLE, 
    LILYPAD_ADVOCATE_DISCORD_ROLE, 
    POW_CONTRACT_ADDRESS, 
    POW_CONTRACT_ADDRESS_METHOD,
    POW_SIGNAL_CRON_ADDRESS,
    POW_SIGNAL_CRON_ADDRESS_METHOD,
    ARBISCAN_API_KEY, 
    ARBISCAN_API_ENDPOINT,
    ARBISCAN_ADDRESS_URL
)

# Constants to set the warning and error thresholds for time since the last transaction
warning_threshold_minutes = 60  # Time in minutes to trigger a warning
error_threshold_minutes = 120  # Time in minutes to trigger an error

# Discord roles that will be tagged in the message
discord_roles = f"{LILYTEAM_DISCORD_ROLE}, {LILYPAD_ADVOCATE_DISCORD_ROLE}"

def get_latest_transaction_time(contract_address: str, method_signature: str):
    """
    Fetch the latest transaction timestamp and method from the Etherscan API for the given contract address and method.
    Returns the timestamp as a datetime object and method name if successful, or None if an error occurs.
    """
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': contract_address,  # Dynamic contract address
        'startblock': 0,  # Start from the first block
        'endblock': 99999999,  # End at the latest block
        'sort': 'desc',  # Sort transactions by newest first
        'apikey': ARBISCAN_API_KEY
    }
    
    response = requests.get(ARBISCAN_API_ENDPOINT, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['status'] == '1' and len(data['result']) > 0:
            for tx in data['result']:
                method = tx['input'][:10]  # First 10 characters (0x + 4-byte selector)
                
                if method == method_signature:  # Match the method signature
                    timestamp = int(tx['timeStamp'])
                    return datetime.fromtimestamp(timestamp, tz=timezone.utc), method  # Return timestamp and method
            print(f"No matching transactions found for method {method_signature} on contract {contract_address}.")
            return None, None
        else:
            print(f"No transactions found for contract {contract_address}.")
            return None, None
    else:
        print("Error fetching data from Etherscan.")
        return None, None

def format_time_difference(seconds):
    """
    Format the time difference in seconds into a more human-readable form (minutes and seconds).
    """
    minutes = seconds // 60  # Convert total seconds to minutes
    remaining_seconds = seconds % 60  # Get the remaining seconds after the minutes
    return f"{int(minutes)} minutes and {int(remaining_seconds)} seconds"  # Return formatted string

def monitor_transactions(contract_methods):
    """
    Monitors the latest transactions for multiple contract addresses and methods.
    Sends a unified Discord message with the results of all checks.
    
    :param contract_methods: A list of dictionaries, each containing 'contract_address' and 'method_signature'.
    """
    # Initialize message parts
    info_messages = []
    
    for contract in contract_methods:
        contract_address = contract['contract_address']
        method_signature = contract['method_signature']
        method_name = contract.get('method_name', method_signature) 

        # Get the timestamp and method of the latest transaction
        latest_transaction_time, latest_method = get_latest_transaction_time(contract_address, method_signature)
        
        if latest_transaction_time is None or latest_method is None:  # Skip if no matching transaction
            continue
        
        # Get the current time in UTC
        current_time = datetime.now(timezone.utc)
        
        # Calculate the difference between the current time and the time of the last transaction
        time_diff = current_time - latest_transaction_time
        total_seconds_since_last_tx = time_diff.total_seconds()  # Get the difference in total seconds

        # Info message specific to this contract-method pair
        info_message = f"Contract: [{contract_address}]({ARBISCAN_ADDRESS_URL}{contract_address}) \n Method: {method_signature}"

        # Check thresholds and build appropriate messages
        if total_seconds_since_last_tx > error_threshold_minutes * 60:
            error_message = f"**ERROR**: Last transaction for __**{method_name}**__ was {format_time_difference(total_seconds_since_last_tx)} ago"
            print(error_message)
            info_messages.append(f"### 🔴 {error_message} \n {info_message} \n {discord_roles}")
        elif total_seconds_since_last_tx > warning_threshold_minutes * 60:
            warning_message = f"**WARNING**: Last transaction for __**{method_name}**__ was {format_time_difference(total_seconds_since_last_tx)} ago"
            print(warning_message)
            info_messages.append(f"### ⚠️ {warning_message} \n {info_message} \n {discord_roles}")
        else:
            ok_message = f"**OK**: Last transaction for __**{method_name}**__ was {format_time_difference(total_seconds_since_last_tx)} ago."
            print(ok_message)
            info_messages.append(f"### 🟢 {ok_message} \n {info_message}")
    
    # Combine all the messages into a single message to send to Discord
    final_message = "\n\n".join(info_messages)
    
    if final_message:
        send_discord_message(POW_MONITORING_WEBHOOK, final_message)

# If this script is run directly, call the monitor_transactions function
if __name__ == "__main__":
    # Define the contract addresses and method signatures to monitor
    contract_methods = [
        {'contract_address': POW_CONTRACT_ADDRESS, 'method_signature': POW_CONTRACT_ADDRESS_METHOD, 'method_name': 'POW Contract'},
        {'contract_address': POW_SIGNAL_CRON_ADDRESS, 'method_signature': POW_SIGNAL_CRON_ADDRESS_METHOD, 'method_name': 'POW Signal/Cron'}
    ]
    
    monitor_transactions(contract_methods)
