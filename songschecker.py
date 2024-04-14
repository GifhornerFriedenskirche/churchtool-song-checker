import os
import requests
import datetime
from dotenv import load_dotenv
from wikiUpdate import updateWiki
from modifyTags import *
from getCredentials import *

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
            song['has_sng_file'] = False
        else:
            clean_songs.append(song_info + arrangement_info)
            song['has_sng_file'] = True
    
    now = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
    wiki_content = f"# General Info\n\nThis is an automated report based on [songchecker](https://github.com/GifhornerFriedenskirche/churchtoolScripts)\nStatus of last run (date: {now}): [![check songs 🎶 and update status page 📖](https://github.com/GifhornerFriedenskirche/churchtoolScripts/actions/workflows/checkSongs.yml/badge.svg)](https://github.com/GifhornerFriedenskirche/churchtoolScripts/actions/workflows/checkSongs.yml)\n\nCurrently implemented features\n\n* Check for missing SNG files\n\n"
    wiki_content += "# Malicious Songs\n\n"
    for song in malicious_songs:
        wiki_content += song + '\n'
        
    wiki_content += "\n# Clean Songs\n\n"
    for song in clean_songs:
        wiki_content += song + '\n'
    
    return wiki_content, json_data

def main():
    """
    The main function that executes the script.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    API_URL = os.getenv("API_URL")
    CATEGORY = os.getenv("CATEGORY")
    PAGE_TITLE = os.getenv("PAGE_TITLE")
    USER_NAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    TAG_MISSING_SNG = os.getenv("TAG_MISSING_SNG")
    TAG_LICENCE_CHECK = os.getenv("TAG_LICENCE_CHECK")
    UPDATE_WIKI = os.getenv("UPDATE_WIKI")
    MODIFY_TAGS = os.getenv("MODIFY_TAGS")

    # Get tokens and cookie
    headers, cookies = get_tokens_and_cookie(USER_NAME, USER_PASSWORD, API_URL)

    # Get song data
    json_data = get_song_data(API_URL, headers, cookies)
    if json_data:
        print(f"Successfully fetched {len(json_data['data'])} songs from the API")

        # Check for missing .sng files
        content = check_for_missing_sng_file(json_data)
        print("Checked for missing .sng files")
    
        # Update wiki page if activated
        if UPDATE_WIKI == 'True':
            print("Wiki update is enabled")
            # Todo: check if a page with the title exists
            # Todo: create page if not exists

            print(f"Update wiki page {PAGE_TITLE} at category {CATEGORY} with result: {updateWiki(CATEGORY, PAGE_TITLE, content, USER_NAME, USER_PASSWORD, API_URL)}")
        else :
            print("Wiki update is disabled")

        # Modify tags if activated
        if MODIFY_TAGS == 'True':
            print("Tag modification is enabled")
            # Handle tags for missing SNG files
            TAG_ID_MISSING_SNG = get_tag_id(API_URL, cookies, headers, TAG_MISSING_SNG)
            if TAG_ID_MISSING_SNG == None:
                TAG_ID_MISSING_SNG = create_tag(API_URL, cookies, headers, TAG_MISSING_SNG, type='songs')
                print(f"Tag `{TAG_MISSING_SNG}` was added with ID:{TAG_ID_MISSING_SNG}")
            for songs in json_data['data']:
                if songs['has_sng_file'] == False:
                    add_tag_to_song(API_URL, cookies, headers, songs['id'], TAG_ID_MISSING_SNG, 'songs')
                else:
                    # ToDo: Add check for tag and only remove it if it exists - [blocked by API](https://forum.church.tools/topic/7726/song-schema-attribut-f%C3%BCr-tags-fehlen)
                    remove_tag(API_URL, cookies, headers, songs['id'], TAG_ID_MISSING_SNG, 'songs')
            print(f"Tags modified at {len(json_data['data'])} songs. ")
        else:
            print("Tag modification is disabled")
    

if __name__ == "__main__":
    """
    This condition checks if this script is being run directly or being imported. 
    If it is run directly, it calls the main function.
    """
    main()
