import requests
import os
from getCredentials import *

def get_tag_id(api_url, cookies, headers, tag_name, type='songs'):
  """
  Retrieves the ID of a tag with the given name from the specified API endpoint.

  Parameters:
    api_url (str): The URL of the API endpoint.
    cookies (dict): The cookies to be included in the request.
    headers (dict): The headers to be included in the request.
    tag_name (str): The name of the tag to retrieve the ID for.
    type (str, optional): The type of tag to retrieve. Can be 'songs' or 'persons'. Defaults to 'songs'.

  Returns:
    int or None: The ID of the tag if found, None otherwise.
  """
  if type == 'songs' or type == 'persons':
    params = {
      'type': type
    }
    response = requests.get(api_url + '/api/tags', cookies=cookies, headers=headers, params=params)
  else:
    return None
  tags = response.json()['data']
  if any(tag['name'] == tag_name for tag in tags):
    tag_id = next(tag['id'] for tag in tags if tag['name'] == tag_name)
  else:
    tag_id = None
  return tag_id

def create_tag(api_url, cookies, headers, tag_name, type='songs'):
  """
  Creates a new tag with the specified name and type.

  Parameters:
  - api_url (str): The URL of the API.
  - cookies (dict): The cookies to be sent with the request.
  - headers (dict): The headers to be sent with the request.
  - tag_name (str): The name of the tag to be created.
  - type (str, optional): The type of the tag. Can be 'songs' or 'persons'. Defaults to 'songs'.

  Returns:
  - tag_id (str or None): The ID of the created tag, or None if the tag creation failed.
  """
  if type == 'songs' or type == 'persons':
    create_data = {
      'name': tag_name,
      'type': type
    }
    response = requests.post(api_url + '/api/tags', cookies=cookies, headers=headers, json=create_data)
  else:
    return None
  if response.status_code == 201:
    tag_id = response.json()['data']['id']
  else:
    tag_id = None
  return tag_id

def add_tag_to_song(api_url, cookies, headers, song_id, tag_id, type='songs'):
  """
  Adds a tag to a song.

  Parameters:
  - api_url (str): The URL of the API.
  - cookies (dict): The cookies to be sent with the request.
  - headers (dict): The headers to be sent with the request.
  - song_id (str): The ID of the song to add the tag to.
  - tag_id (str): The ID of the tag to add to the song.
  - type (str, optional): The type of the tag. Can be 'songs' or 'persons'. Defaults to 'songs'.

  Returns:
  - response (dict): The response of the request.
  """
  if type == 'songs':
    func = 'addSongTag'
  elif type == 'persons':
    func = 'addPersonTag'
  else:
    return None
  add_url = f"{api_url}/?q=churchservice/ajax"
  
  add_data = {
    'func': func,
    'id': song_id,
    'tag_id': tag_id
  }
  response = requests.post(add_url,cookies=cookies,headers=headers,json=add_data)
  
  if 'Duplicate entry' in str(response.content):
    return 200
  elif response.status_code == 200:
    return 200
  else:
    return response.status_code


def remove_tag(api_url, cookies, headers, id, tag_id, type='songs'):
  """
  Removes a tag from a song or a person.

  Parameters:
  - api_url (str): The URL of the API.
  - cookies (dict): The cookies to be sent with the request.
  - headers (dict): The headers to be sent with the request.
  - id (str): The ID of the song or the person to remove the tag from.
  - tag_id (str): The ID of the tag to remove from the song.
  - type (str, optional): The type of the tag. Can be 'songs' or 'persons'. Defaults to 'songs'.

  Returns:
  - response (dict): The response of the request.
  """
  if type == 'songs':
    func = 'delSongTag'
  elif type == 'persons':
    func = 'delPersonTag'
  else:
    return None
  remove_url = f"{api_url}/?q=churchservice/ajax"
  
  remove_data = {
    'func': func,
    'id': id,
    'tag_id': tag_id
  }
  response = requests.post(remove_url,cookies=cookies,headers=headers,json=remove_data)
  return response

def delete_tag(api_url, cookies, headers, tag_id, type='songs'):
  """
  WIP: Deletes a tag from the database.
  """
  remove_url = f"{api_url}/?q=churchservice/ajax"
  
  remove_data = {
    'func': 'removeTag',
    'id': tag_id,
    'type': type
  }
  #response = requests.post(remove_url,cookies=cookies,headers=headers,json=remove_data)
  #return response
  return 'WIP: Delete tag function is not yet implemented.'