import datetime
import json
import os
from utils.tokenGen import Authenticator


token_file = "./data/token_data.json"
token_file = os.path.abspath(token_file)
user_authenticator = Authenticator(api_key=os.getenv("IBM_WATSONX_AUTH_TOKEN"))

def save_token(token):
    data = {
        "token": token,
        "generated_at": datetime.datetime.now().isoformat()
    }
    
    with open(token_file, "w") as f:
        json.dump(data, f, indent=4)
    

def load_token():
    try:
        with open(token_file, "r") as f:
            data = json.load(f)
            token = data.get("token")
            generated_at = datetime.datetime.fromisoformat(data.get("generated_at"))
            return token, generated_at
    except(FileNotFoundError, ValueError):
        
        return None, None 


def is_token_expired(generated_at):
    if generated_at == None:
        return True
    
    currentTime = datetime.datetime.now()
    time_difference = currentTime - generated_at
    return time_difference.total_seconds() > 3600

def generate_new_token():
    token = user_authenticator.get_access_token()
    return token


def get_access_token():
    
    token, generated_at = load_token()
    
    if is_token_expired(generated_at):
        print("Token has expired or does not exist. Generating a new token...")
        token = generate_new_token()
        save_token(token)
    else:
        print("Token is Valid")
        
    return token
            
                

