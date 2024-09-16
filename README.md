# GitHub Issues and Discord Integration Framework

This Python project provides a modular framework for interacting with GitHub issues and sending notifications to a Discord channel. It is designed to be easily extensible for future bots or similar integrations.

## Project Structure

- `utils/`
  - `discord.py`: Utility functions for sending messages to Discord.
  - `git.py`: Utility functions for fetching issues from GitHub.

- `oss_issues.py`: Processes open GitHub issues, formats them, and sends them to Discord with encouragement messages.

- `oss_leaderboard.py`: Generates a leaderboard of contributors based on closed GitHub issues and sends it to Discord.

- `vars.py`: Contains configuration variables such as GitHub API URL and Discord webhook URL.


## Usage

### Sending Discord Messages

The `utils/discord.py` module contains two functions for sending messages to a Discord channel:

- `send_discord_message(webhook_url, message)`: Sends a simple text message.
- `send_discord_message_with_local_image(webhook_url, message, image_path=None)`: Sends a text message with an optional image attachment.

### Fetching GitHub Issues

The `utils/git.py` module provides the `fetch_all_issues(api_url, params)` function to fetch all issues from GitHub. It handles pagination automatically.

### Processing Open Issues

The `oss_issues.py` script:

1. Fetches all open GitHub issues.
2. Categorizes issues by whether they are assigned or unassigned and if they have a "community" label.
3. Formats the issues and sends them to Discord with a randomly selected encouragement message.

### Generating Leaderboard

The `oss_leaderboard.py` script:

1. Fetches all closed GitHub issues.
2. Counts the number of issues solved by each assignee.
3. Creates a leaderboard with badges and progress bars based on the number of solved issues.
4. Sends the leaderboard to Discord.

#### Features

- **Badges:** Awards badges to contributors based on their issue-solving count.
- **Progress Bar:** Shows visual progress towards the next badge milestone.
- **Leaderboard Formatting:** Ranks contributors and displays their achievements.


### Usage
To set up and run the project locally using Docker Compose, follow these steps:

1. **Build and run the Docker container:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image and start the container. The `entrypoint` is set to `tail -f /dev/null` to keep the container running, allowing you to execute commands interactively.

2. **Access the container:**

    To run scripts or interact with the container, use the following command:

    ```bash
    docker exec -it lilypad_assistant /bin/bash
    ```

    You can now run your Python scripts inside the container. For example, to run `oss_issues.py`:

    ```bash
    python3 oss_issues.py
    ```

    Or to run `oss_leaderboard.py`:

    ```bash
    python3 oss_leaderboard.py
    ```

3. **Stop the container:**

    To stop and remove the container, use:

    ```bash
    docker-compose down
    ```
