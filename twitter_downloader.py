import sys
import os
import re

import requests
import bs4

from tqdm import tqdm
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def download_video(url, file_name) -> None:
    """Download a video from a URL into a filename.

    Args:
        url (str): The video URL to download
        file_name (str): The file name or path to save the video to.
    """
    
    # Define the save directory
    result_directory = os.path.join(os.getcwd(), 'result_video')
    os.makedirs(result_directory, exist_ok=True)
    
    download_path = os.path.join(result_directory, file_name)

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

    with open(download_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    print(f"Video downloaded successfully as {download_path}!")


def extract_video_id(url):
    """Extract video ID from the Twitter URL.

    Args:
        url (str): The Twitter post URL

    Returns:
        str: The video ID
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    # Assuming the ID is the last part of the URL path
    video_id = path_parts[-1] if path_parts[-1].isdigit() else 'video_id'
    return video_id


def download_twitter_video(url):
    """Extract the highest quality video url to download into a file

    Args:
        url (str): The twitter post URL to download from
    """

    api_url = f"https://twitsave.com/info?url={url}"

    response = requests.get(api_url)
    data = bs4.BeautifulSoup(response.text, "html.parser")
    download_button = data.find_all("div", class_="origin-top-right")[0]
    quality_buttons = download_button.find_all("a")
    highest_quality_url = quality_buttons[0].get("href")  # Highest quality video url
    
    video_id = extract_video_id(url)
    file_name = f"{video_id}.mp4"  # Use video ID as filename
    
    download_video(highest_quality_url, file_name)


if __name__ == "__main__":
    url = input("Please enter the Twitter video URL: ")
    if url:
        download_twitter_video(url)
    else:
        print("Invalid Twitter video URL provided.")
