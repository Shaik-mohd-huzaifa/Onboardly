import os
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from services.llm import WatsonXLLM

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    # dimensions: Optional[int] = None, # Can specify dimensions with new text-embedding-3 models
    azure_endpoint="https://wasp-ai-openai.openai.azure.com/",
    api_key="2704e1c05ed94dfea045cb86d1d8c86c",
    openai_api_version="2023-03-15-preview",
)


def perform_similarity_search(path, query):
    # Check if the FAISS index files exist
    faiss_file = os.path.join(path, "index.faiss")
    pkl_file = os.path.join(path, "index.pkl")

    if not (os.path.exists(faiss_file) and os.path.exists(pkl_file)):
        return {"error": "Vector store files not found"}, 404

    # Load the vector store using FAISS
    vectorStore = FAISS.load_local(
        path, embeddings, allow_dangerous_deserialization=True
    )

    # Define the prompt template
    template = """You are an assistant helping new hires onboard.

    Context:
    {context}

    Question:
    {question}

    Answer:"""

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)

    # Initialize the LLM
    llm_instance = WatsonXLLM()
    client = llm_instance.get_llm()

    # Create the RetrievalQA chain
    retrieval_chain = RetrievalQA.from_chain_type(
        llm=client,
        chain_type="stuff",
        retriever=vectorStore.as_retriever(),
        chain_type_kwargs={"prompt": prompt},
    )

    # Run the retrieval chain with a query
    result = retrieval_chain.invoke({"query": query})

    return result
