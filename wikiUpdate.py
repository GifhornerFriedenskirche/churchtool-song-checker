import requests
from getCredentials import *

def updateWiki(category, page_title, content, api_url, headers, cookies):
  """
  Updates a wiki page with the specified category, page title, and content.

  Args:
    category (str): The category of the wiki page.
    page_title (str): The title of the wiki page.
    content (str): The content to update the wiki page with.
    api_url (str): The URL of the API.
    headers (dict): The headers to include in the API request.
    cookies (dict): The cookies to include in the API request.

  Returns:
    str: A message indicating whether the update was successful or failed.
  """
  # Get identifier
  identifier_url = f"{api_url}/api/wiki/categories/{category}/pages/{page_title}/versions"

  response = requests.get(identifier_url, headers=headers, cookies=cookies)
  response.raise_for_status()

  identifier = response.json().get("data")[0].get("identifier")

  # Write data to /?q=churchwiki/ajax
  update_url = f"{api_url}/?q=churchwiki/ajax"
  update_data = {
    "doc_id": page_title,
    "wikicategory_id": category,
    "val": content,
    "auf_startseite_yn": False,
    "identifier": identifier,
    "is_markdown": True,
    "func": "save"
  }

  params = {
    "func": "save"
  }
  response = requests.post(update_url, json=update_data, headers=headers, params=params, cookies=cookies)
  response.raise_for_status()

  # Check if the update was successful
  if response.json().get("status") == 'success':
    return "Update successful"
  else:
    return "Update failed"
