import os
import requests
from dotenv import load_dotenv

# Loads API key and secret and reddit password.
load_dotenv()
senha = os.getenv('SENHA_REDDIT')
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')


def request_handler(api_params=None):

  token, headers = auth()
  responses = []

  for request in api_params:

    subreddit, num_posts, wanted_flairs = request
    flairs = ''

    if not(isinstance(wanted_flairs, list)):
      params = {'limit':str(num_posts)}
      res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot', headers = headers, params = params)
    else:
      for flair in wanted_flairs:
        if len(flairs) < 2:
          flairs = f'flair:{flair}'
        else:
          flairs += f' OR flair:{flair}'
          params = {'limit':str(num_posts), 'q':flairs}
          res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/search', headers = headers, params = params)

    responses.append(res)

  return responses


# ------------

# Gets API's access token and authorization.
def auth():

  auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
  data = {'grant_type':'password','username':'RevolutionaryLab7729','password':senha}
  headers = {'User-Agent':'windows:script for automation:v0.1 (by u/RevolutionaryLab7729'}

  res_test = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

  if res_test.status_code == 200:
    token = res_test.json()['access_token']
    headers['Authorization'] = f"bearer {token}"
  else:
    raise ValueError("Request error.")
    # TO DO: logger_request(res.status_code)

  return (token, headers)


# ---------------------

if __name__ == "__main__":
  request_handler()
