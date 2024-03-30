import os
import requests
from dotenv import load_dotenv
from wikiupdate import updateWiki
from getCredentials import *

# Load environment variables from .env file
load_dotenv()

# Get environment variables
API_URL = os.getenv("API_URL")
CATEGORIE = os.getenv("CATEGORIE")
PAGE_TITLE = os.getenv("PAGE_TITLE")
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")


def get_song_data(api_url, headers, cookies):
    """
    Fetches song data from the API. Configured User needs view rights to songs.

    Args:
        api_url (str): The URL of the API.
        headers (dict): The headers for the API request.
        cookies (dict): The cookies for the API request.

    Returns:
        dict: The song data in JSON format.
    """
    all_data = []
    page = 1
    while True:
        params = {'page': page}
        response = requests.get(api_url+'/api/songs?limit=200', headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            all_data.extend(data['data'])
            if len(data['data']) < 10:  # Assuming '10' is the default limit
                break
            page += 1
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    return {'data': all_data}

def count_sng_files(arrangements):
    """
    Counts the number of .sng files in each arrangement.

    Args:
        arrangements (list): The list of song arrangements.

    Returns:
        dict: A dictionary with arrangement names as keys and the count of .sng files as values.
    """
    sng_counts = {}
    for arrangement in arrangements:
        sng_count = sum(1 for file in arrangement['files'] if file['name'].endswith('.sng'))
        sng_counts[arrangement['name']] = sng_count
    return sng_counts

def check_for_missing_sng_file(json_data):
    """
    Checks for songs with missing .sng files.

    Args:
        json_data (dict): The song data in JSON format.

    Returns:
        str: The report content with information about malicious and clean songs.
    """
    malicious_songs = []
    clean_songs = []
    
    for song in json_data['data']:
        arrangement_counts = count_sng_files(song['arrangements'])
        has_missing_sng = any(count == 0 for count in arrangement_counts.values())
        
        song_info = f"Song: {song['name']}\n"
        arrangement_info = ""
        for arrangement, count in arrangement_counts.items():
            arrangement_info += f"- {arrangement}: {count} .sng file(s)\n"
        
        if has_missing_sng:
            malicious_songs.append(song_info + arrangement_info)
        else:
            clean_songs.append(song_info + arrangement_info)
    
    content = "# General Info\n\nThis is an automated report based on [songchecker](https://github.com/GifhornerFriedenskirche/churchtoolScripts)\n\nCurrently implemented features\n\n* Check for missing SNG files\n\n"
    content += "# Malicious Songs\n\n"
    for song in malicious_songs:
        content += song + '\n'
        
    content += "\n# Clean Songs\n\n"
    for song in clean_songs:
        content += song + '\n'
    
    return content

def main():
    """
    The main function that executes the script.
    """
    headers, cookies = get_tokens_and_cookie(USER_NAME, USER_PASSWORD, API_URL)

    json_data = get_song_data(API_URL, headers, cookies)
    if json_data:
        content = check_for_missing_sng_file(json_data)
        print(updateWiki(CATEGORIE, PAGE_TITLE, content))

if __name__ == "__main__":
    main()