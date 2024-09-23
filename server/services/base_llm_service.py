import os
from dotenv import load_dotenv
import requests
from utils.token_expiry_check import get_access_token
from langchain_core.prompts import PromptTemplate

load_dotenv()

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

template = (
    template
) = """
    You are an Assistant who help newly onboards in the organisation called {organisation} which is a type of {organisation_type} and this organisation {organisation_description}"
    
    Context: use context data to answer the question first if the data isn't sufficient then answer through your knowledge and even if its out of your knowledge then say "I cannot provide a response for this query or i have no data of the query in the knowledge base
    {context}
    
    By referring the Context answer my Question:
    {question}
    """

template = """
You are an Assistant helping new hires onboard into an organization called {organisation}, which is a {organisation_type}. This organization is known for {organisation_description}.

Context:
{context}

Your task is to answer the following question based on the given context. Use the context data first. If the data isn't sufficient, provide an answer based on your knowledge. If the answer is beyond your knowledge base or the context does not provide enough information, clearly state: "I cannot provide a response for this query as it is not available in the provided context or my knowledge base."

Question:
{question}

Answer:
"""


def call_llm(query, context, Organsation, Org_type, Org_description):
    prompt = PromptTemplate(
        template=template,
        input_variables=[
            "organisation",
            "organisation_type",
            "organisation_description",
            "role",
            "context",
            "question",
        ],
    )

    formatted_prompt = prompt.format(
        question=query,
        context=context,
        organisation=Organsation,
        organisation_type=Org_type,
        organisation_description=Org_description,
    )

    body = {
        "input": formatted_prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "repetition_penalty": 1.05,
        },
        "model_id": "ibm/granite-13b-chat-v2",
        "project_id": os.getenv("WATSONX_AI_PROJECT_ID"),
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + get_access_token(),
    }
    response = requests.post(url, headers=headers, json=body)

    print(formatted_prompt)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    print(data["results"][0])
