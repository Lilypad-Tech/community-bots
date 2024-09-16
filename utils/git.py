import requests

# Function to fetch all issues (open or closed) based on the parameters
def fetch_all_issues(api_url, params):
    all_issues = []
    while True:
        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            print("Failed to retrieve the issues data.")
            exit()

        issues = response.json()
        if not issues:
            break  # No more issues

        all_issues.extend(issues)
        params['page'] += 1  # Move to next page

    return all_issues
