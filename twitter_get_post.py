import math
import requests
from pprint import pprint

def get_token(tweet_id):
    token = (int(tweet_id) / 1e15) * math.pi
    hex_token = hex(int(token * (10 ** 16)))[2:]  # Convert to integer before formatting to hex
    return hex_token.replace('0', '').replace('.', '')

def fetch_tweet_data(tweet_id):
    token = get_token(tweet_id)
    url = f'https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&token={token}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # With beautiful print
        pprint(data)

        # Accessing data.user.name
        user_name = data['user']['name']
        print(f"User Name: {user_name}")

    except requests.exceptions.RequestException as error:
        print(f'Error fetching tweet data: {error}')

# Example usage
tweet_id = '1826464289357529413'  # Replace with actual tweet ID
fetch_tweet_data(tweet_id)
