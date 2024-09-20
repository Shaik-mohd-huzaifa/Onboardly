from langchain_ibm import WatsonxLLM
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["WATSONX_APIKEY"] = os.getenv("IBM_WATSONX_AUTH_TOKEN")

default_parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 1000,
    "min_new_tokens": 1,
    "temperature": 0.5,
    "top_k": 50,
    "top_p": 1,
}

class WatsonXLLM:
    def __init__(self, parameters = default_parameters):
        self.parameters = parameters

    def get_llm(self) -> None:
        watsonx_llm = WatsonxLLM(
            model_id="ibm/granite-13b-chat-v2",
            url="https://us-south.ml.cloud.ibm.com",
            project_id=os.getenv("WATSONX_AI_PROJECT_ID"),
            params=self.parameters,
        )
        return watsonx_llm

# print(watsonx_llm.invoke("Who is the father of american nation"))
