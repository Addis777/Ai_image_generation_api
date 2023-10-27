import requests
import json
from urllib.parse import urlencode

class OAuth2Provider:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authentication_url(self):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid profile email'
        }
        auth_url = 'https://accounts.google.com/o/oauth2/auth?' + urlencode(params)
        return auth_url

    def exchange_code_for_tokens(self, code):
        data = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        tokens = json.loads(response.text)
        access_token = tokens['access_token']
        id_token = tokens['id_token']
        return access_token, id_token

    def get_user_info(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        user_info = json.loads(response.text)
        return user_info
