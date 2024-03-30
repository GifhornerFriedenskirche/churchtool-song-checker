import requests

def get_tokens_and_cookie(user_name, user_password, api_url):
  """
  Retrieves authentication tokens and cookie for API access.

  Returns:
    tuple: A tuple containing the headers and cookie for API authentication.
  """
  # Login via API
  login_url = f"{api_url}/api/login"
  login_data = {
    "username": user_name,
    "password": user_password
  }
  headers = {
    "Content-Type": "application/json"
  }
  response = requests.post(login_url, json=login_data, headers=headers)
  response.raise_for_status()

  # Get cookie & UserID
  cookie = response.cookies.get_dict()
  person_id = response.json().get("data").get("personId")

  # Get csrf-token
  csrf_token_url = f"{api_url}/api/csrftoken"

  response = requests.get(csrf_token_url, cookies=cookie, headers=headers)
  response.raise_for_status()

  csrf_token = response.json().get("data")

  headers["X-CSRFToken"] = csrf_token

  # Get login-token
  login_token_url = f"{api_url}/api/persons/{person_id}/logintoken"
  response = requests.get(login_token_url, cookies=cookie, headers=headers)
  response.raise_for_status()
  login_token = response.json().get("data")

  headers["authorization"] = f"Login {login_token}"

  return headers, cookie