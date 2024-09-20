from dotenv import load_dotenv
import os
from db.schemas.organsiations import getData
from flask import Flask
import requests
from utils.token_expiry_check import get_access_token
from services.llm import WatsonXLLM
import time
from db.schemas.organsiations import create

load_dotenv()
create()

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"


body = {
	"input": """<|system|>
You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior. You always respond to greetings (for example, hi, hello, g'\''day, morning, afternoon, evening, night, what'\''s up, nice to meet you, sup, etc) with \"Hello! I am Granite Chat, created by IBM. How can I help you today?\". Please do not say anything else and do not start a conversation.
<|assistant|>
Who is the father of the Nation India?
<|user|>
""",
	"parameters": {
		"decoding_method": "greedy",
		"max_new_tokens": 900,
		"repetition_penalty": 1.05
	},
	"model_id": "ibm/granite-13b-chat-v2",
	"project_id": "7df2cac2-9b44-4515-bbf5-86233a391a7c"
}

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": "Bearer " + get_access_token()
}

s_time = time.time()
response = requests.post(
	url,
	headers=headers,
	json=body
)
e_time = time.time()

if response.status_code != 200:
	raise Exception("Non-200 response: " + str(response.text))

data = response.json()


print(data["results"][0])
llm_instance = WatsonXLLM()
llm = llm_instance.get_llm()
print("-" * 50)
print(llm.invoke("Who is the father of the Nation India?"))
# getData()