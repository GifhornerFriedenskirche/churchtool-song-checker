import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_URL = os.getenv("API_URL")

def get_json_data_from_api(api_url, headers):
    all_data = []
    page = 1
    while True:
        params = {'page': page}
        response = requests.get(api_url+'/api/songs?limit=200', headers=headers, params=params)
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
    sng_counts = {}
    for arrangement in arrangements:
        sng_count = sum(1 for file in arrangement['files'] if file['name'].endswith('.sng'))
        sng_counts[arrangement['name']] = sng_count
    return sng_counts

def write_songs_with_sng_counts_to_file(json_data, output_file):
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
    
    with open(output_file, 'w') as file:
        file.write("# Malicious Songs\n\n")
        for song in malicious_songs:
            file.write(song + '\n')
        
        file.write("\n# Clean Songs\n\n")
        for song in clean_songs:
            file.write(song + '\n')

def main():
    headers = {
        "Authorization": f"Login {AUTH_TOKEN}",  # Using "Login" instead of "Bearer"
        "Content-Type": "application/json"
    }
    output_file = "output.md"  # Output file with markdown extension
    json_data = get_json_data_from_api(API_URL, headers)
    if json_data:
        write_songs_with_sng_counts_to_file(json_data, output_file)
        print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()