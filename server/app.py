from flask import Flask, request, jsonify
from flask_cors import CORS
from db.schemas.employees import Employees
from db.schemas.organsiations import Orgs
from db.schemas.documents import Documents, create
from utils.data_Normalization import NormalizeData
from utils.document_to_text import extract_text_from_pdf
from langchain_text_splitters import CharacterTextSplitter
import json
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
from peewee import DoesNotExist
from langchain.schema import Document
from services.base_llm_service import call_llm
from utils.similarity_search import perform_similarity_search
from services.llm import WatsonXLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from db.schemas.AddNotes import Notes, create

create()

# from services.embeddingModel import generate_embedding
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    # dimensions: Optional[int] = None, # Can specify dimensions with new text-embedding-3 models
    azure_endpoint="https://wasp-ai-openai.openai.azure.com/",
    api_key="2704e1c05ed94dfea045cb86d1d8c86c",
    openai_api_version="2023-03-15-preview",
)
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "docx"}

vectorStore = None

@app.route("/emplogin", methods=["POST"])
def login():
    data = request.get_data()
    data = data.decode("utf-8")
    login_data = json.loads(data)

    try:
        employee = Employees.get((Employees.employee_name == login_data["email"]) & (Employees.password == login_data["password"]))
        return {"Validity": True, "User": employee}
    except Exception as e:
        return {"Validity": False} 


@app.route("/CreateEmployee", methods=["POST"])
def CreateEmployee():
    data = request.get_data()
    data = data.decode("utf-8")
    New_Employee_Data = json.loads(data)

    try:
        employee = Employees.get(Employees.employee_name == New_Employee_Data["employee_email"])
        return jsonify({"message": "patient/@exists"})
    except DoesNotExist:
        Employees.insert_many([New_Employee_Data]).execute()
        return jsonify({"message": "patient/@created"})
    except Exception as e:
        print(f"The Error is {e}")
        return jsonify({"message": "error/unexpected"})


@app.route("/CreateOrg", methods=["POST"])
def Create_Organisation():
    data = NormalizeData(request.get_data())

    try:
        # Try to find an organization with the given email
        Orgs.get(Orgs.organisation_email == data["organisation_email"])
        # If we reach this point, the organization exists
        return jsonify({"message": "organisation/@exists"})
    except DoesNotExist:
        # If we get here, the organization doesn't exist, so we can create it
        Orgs.create(**data)
        org = Orgs.get(Orgs.organisation_email == data["organisation_email"])
        org = {
            "organisation_id": org.organisation_id,
            "organisation_name": org.organisation_name,
            "organisation_type": org.organisation_type,
            "organisation_description": org.organisation_description,
            "organisation_email": org.organisation_email,
        }
        return jsonify({"message": "organisation/@created", "data": org})
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred: {e}")
        return jsonify({"message": "error/@unexpected"}), 500

@app.route("/getOrgsEmps", methods=["POST"])
def get_Organisation_employees():
    data = NormalizeData(request.get_data())

    org = Orgs.get(Orgs.organisation_id == data["org_id"])

    org_emp = org.onboarding_employees.dicts()

    print(org_emp)
    return jsonify(list(org_emp)), 200


# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/uploadDocuments", methods=["POST"])
def UploadDocuments():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    org_id = request.form.get("org_id")

    # org = Orgs.get(Orgs.organisation_id == org_id)

    try:
        org = Orgs.get(Orgs.organisation_id == org_id)
    except Orgs.DoesNotExist:
        return jsonify({"error": "Organization not found"}), 404

    if file and allowed_file(file.filename):
        filename = file.filename
        # Convert organisation_id to a string and sanitize organisation_name
        org_id = org.organisation_id
        org_name = org.organisation_name.replace(" ", "_").strip()

        global UPLOAD_FOLDER

        UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, f"{org_id}_{org_name}")

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Converting Docs, Pdf in Text
        text = extract_text_from_pdf(file_path)

        documents = [Document(page_content=text, meta_data={})]
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
        docs = text_splitter.split_documents(documents)

        global vectorStore

        if vectorStore is None:
            vectorStore = FAISS.from_documents(docs, embeddings)
        else:
            vectorStore.add_documents(docs)

        vectorStore.save_local(UPLOAD_FOLDER)

        documentData = {
            "document_name": request.form.get("name"),
            "document_description": request.form.get("description"),
            "organisation": request.form.get("org_id"),
            "document_address": file_path,
        }

        Documents.insert_many([documentData]).execute()

        return jsonify({"message": "Suceesfull Uploaded"})


@app.route("/getDocs", methods=["POST"])
def getDocs():
    data = NormalizeData(request.get_data())

    org = Orgs.get(Orgs.organisation_id == data["org_id"])

    org_emp = org.org_docs.dicts()

    return jsonify(list(org_emp)), 200


@app.route("/getSimilarity", methods=["POST"])
def similarity():
    # Normalize and parse the request data
    data = NormalizeData(request.get_data())

    # Get the organization details from the database
    try:
        org = Orgs.get(Orgs.organisation_id == data["org_id"])
    except Orgs.DoesNotExist:
        return jsonify({"error": "Organization not found"}), 404

    # Prepare the file path for the vector store
    org_id = org.organisation_id
    org_name = org.organisation_name.replace(" ", "_").strip()
    vectorStorePath = os.path.join("uploads", f"{org_id}_{org_name}")

    # Check if the FAISS index files exist
    faiss_file = os.path.join(vectorStorePath, "index.faiss")
    pkl_file = os.path.join(vectorStorePath, "index.pkl")

    if not (os.path.exists(faiss_file) and os.path.exists(pkl_file)):
        return jsonify({"error": "Vector store files not found"}), 404

    # Load the vector store using FAISS
    global vectorStore
    if vectorStore is None:
        vectorStore = FAISS.load_local(
            vectorStorePath, embeddings, allow_dangerous_deserialization=True
        )

    # Extract the query text from the request
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Perform the similarity search
    search_results = vectorStore.similarity_search_with_score(query)

    # Format the search results to return relevant information
    result_data = [
        {
            "similarity_score": float(score),  # Convert numpy.float32 to Python float
            "document_content": doc.page_content,
            "document_metadata": doc.metadata,
        }
        for doc, score in search_results
    ]

    response = call_llm(
        query=query,
        # context=[context["document_content"] for context in result_data],
        context=result_data[0]["document_content"],
        Organsation=org_name,
        Org_type=org.organisation_type,
        Org_description=org.organisation_description,
    )

    llm_instance = WatsonXLLM()
    llm = llm_instance.get_llm()

    template2 = """
    You are an Assistant helping new hires onboard into an organization called {organisation}, which is a {organisation_type}. This organization is known for {organisation_description}.

    Context:
    {context}

    Your task is to answer the following question based on the given context. Use the context data first, and if the data isn't sufficient, answer using your knowledge. If the answer is beyond your knowledge base or the context does not provide enough information, clearly state: "I cannot provide a response for this query as it is not available in the provided context or my knowledge base."

    Question:
    {question}
    """

    prompt = PromptTemplate(
        template=template2,
        input_variables=[
            "organisation",
            "organisation_type",
            "organisation_description",
            "role",
            "context",
            "question",
        ],
    )

    llmChain = prompt | llm
    # response = llmChain.invoke(
    #     {
    #         "question": query,
    #         "context": result_data[0]["document_content"],
    #         "organisation": org_name,
    #         "organisation_type": org.organisation_type,
    #         "organisation_description": org.organisation_description,
    #     }
    # )
    print(response)
    return jsonify({"results": result_data}), 200


@app.route("/AddNotes", methods=["POST"])
def AddNotes():
    data = NormalizeData(request.get_data())

    org = Orgs.get(Orgs.organisation_id == data["Org_id"])

    org_id = org.organisation_id
    org_name = org.organisation_name.replace(" ", "_").strip()
    vectorStorePath = os.path.join("uploads", f"{org_id}_{org_name}")
    text = "Note Name: " + data["name"] + "Description: " + data["description"]
    documents = [Document(page_content=text, meta_data={})]
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    docs = text_splitter.split_documents(documents)

    global vectorStore

    if vectorStore is None:
        vectorStore = FAISS.from_documents(docs, embeddings)
    else:
        vectorStore.add_documents(docs)

    vectorStore.save_local(vectorStorePath)

    Notes.insert_many([data]).execute()

    return jsonify({"message": "Upload Sucessful"})


@app.route("/getNotes", methods=["POST"])
def getNotes():
    data = NormalizeData(request.get_data())
    org = Orgs.get(Orgs.organisation_id == data["org_id"])

    notes = org.org_rules.dicts()

    return jsonify(list(notes))


if __name__ == "__main__":
    app.run(debug=True)
