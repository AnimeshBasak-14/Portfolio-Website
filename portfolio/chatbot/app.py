from flask import Flask, request, jsonify
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HF_TOKEN or not GROQ_API_KEY:
    raise EnvironmentError("Missing HF_TOKEN or GROQ_API_KEY in environment variables.")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Store session histories
session_store = {}

# Initialize LLM
def initialize_llm(api_key, provider="groq"):
    """
    Initialize an LLM with the given API key and provider.
    Default provider is 'groq'. You can switch to 'huggingface'.
    """
    print(f"Initializing LLM with provider: {provider}")

    if provider == "groq":
        # return ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")
        return ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192")

    elif provider == "huggingface":
        return HuggingFaceHub(
            repo_id="bigscience/bloom",  # Replace with the Hugging Face model of your choice
            huggingfacehub_api_token=api_key
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Create retriever
def create_retriever(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore.as_retriever()

# Chat history management
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()  # Ensure it's the correct type
    return session_store[session_id]

# Load and Process Resume at Startup
def process_resume():
    try:
        resume_path = 'resume.pdf'
        if not os.path.exists(resume_path):
            raise FileNotFoundError("resume.pdf not found in the project directory.")

        loader = PyPDFLoader(resume_path)
        documents = loader.load()

        retriever = create_retriever(documents)
        llm = initialize_llm(GROQ_API_KEY)

        contextualize_q_prompt = ChatPromptTemplate.from_messages([ 
            ("system", "Given a chat history and the latest user question, "
                       "formulate a standalone question without chat history."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        system_prompt = ("You are an assistant for question-answering tasks based on Animesh's resume for his porfolio website. "
                         "Use retrieved context to answer questions concisely.\n\n{context}")
        qa_prompt = ChatPromptTemplate.from_messages([ 
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        session_id = 'resume_session'
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,  # Pass the correct history function
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        session_store[f"{session_id}_chain"] = conversational_rag_chain
        print(f"conversational_rag_chain chain stored: {type(conversational_rag_chain)}")
        print(f"Session chain stored: {type(session_store[f'{session_id}_chain'])}")

        print("✅ Resume PDF successfully processed and ready for queries.")

    except Exception as e:
        print(f"❌ Error processing resume: {e}")


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('user_input')
        session_id = 'resume_session'
        chain_key = f"{session_id}_chain"
        if chain_key not in session_store:
            print("❌ Session not found. Resume was not processed correctly.")
            return jsonify({"error": "Session not found. Resume was not processed correctly."}), 400

        # if session_id not in session_store or "conversational_rag_chain" not in session_store[session_id]:
        #     return jsonify({"error": "Session not found. Resume was not processed correctly."}), 400

        chain = session_store[chain_key]

        # Invoke the chain and handle the response
        response = chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )

        # Debugging: Print the raw response structure
        print("Raw Response from Chain:", response)

        # Handle various response structures
        if isinstance(response, dict):
            # Look for the 'answer' or 'output' key
            answer = response.get('answer') or response.get('output')
            if answer:
                return jsonify({"answer": answer})
            else:
                return jsonify({"error": "Response does not contain an 'answer' or 'output' key."}), 500
        else:
            return jsonify({"error": "Unexpected response format from chain."}), 500

    except Exception as e:
        print(f"❌ Error during chat invocation: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "📝 Conversational RAG with Resume PDF - Flask Backend is running!"


if __name__ == '__main__':
    try:
        process_resume()
        CORS(app)
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start server: {e}")
