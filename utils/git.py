# utils/git.py
import requests

# Function to fetch all issues (open or closed) based on the parameters
def fetch_all_issues(api_url, params):
    all_issues = []
    params_copy = params.copy()  # Copy params to avoid modifying the original
    params_copy['page'] = 1  # Start from the first page

    while True:
        response = requests.get(api_url, params=params_copy)
        if response.status_code != 200:
            print(f"Failed to retrieve the issues data from {api_url}. Status code: {response.status_code}")
            break  # Optionally handle retries or exit

        issues = response.json()
        if not issues:
            break  # No more issues

        all_issues.extend(issues)
        params_copy['page'] += 1  # Move to next page

    return all_issues
