import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Authenticator:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_access_token(self):
        token_url = "https://iam.cloud.ibm.com/identity/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": os.getenv("IBM_WATSONX_API_KEY"),
        }
        response = requests.post(url=token_url, headers=header,data=body)

        if response.status_code == 200:
            return response.json()["access_token"]
        else: 
            raise Exception(response.text)
