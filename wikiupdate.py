import requests
from getCredentials import *

def updateWiki(categorie, page_title, content):
  """
  Update a wiki page with the specified category, page title, and content.

  Args:
    categorie (str): The category of the wiki page.
    page_title (str): The title of the wiki page.
    content (str): The content in markdown to update the wiki page with.

  Returns:
    str: A message indicating whether the update was successful or failed.
  """
  # Get authentication data
  headers, cookie = get_tokens_and_cookie()

  # Get identifier
  identifier_url = f"{API_URL}/api/wiki/categories/{categorie}/pages/{page_title}/versions"

  response = requests.get(identifier_url, headers=headers, cookies=cookie)
  response.raise_for_status()

  identifier = response.json().get("data")[0].get("identifier")

  # Write data to /?q=churchwiki/ajax
  update_url = f"{API_URL}/?q=churchwiki/ajax"
  update_data = {
    "doc_id": page_title,
    "wikicategory_id": categorie,
    "val": content,
    "auf_startseite_yn": False,
    "identifier": identifier,
    "is_markdown": True,
    "func": "save"
  }

  params = {
    "func": "save"
  }
  response = requests.post(update_url, json=update_data, headers=headers, params=params, cookies=cookie)
  response.raise_for_status()

  # Check if the update was successful
  if response.json().get("status") == 'success':
    return "Update successful"
  else:
    return "Update failed"
