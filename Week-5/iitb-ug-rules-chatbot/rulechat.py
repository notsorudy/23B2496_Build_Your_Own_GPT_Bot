import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import tempfile

# Load environment variables
load_dotenv()

# Function to create a vector store from PDF
def create_vector_store(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# Load existing vector store
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Build the chatbot chain with custom prompt
def build_conversational_chain(vector_store):
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Custom prompt template
    prompt_template = """
You are a helful assistant.
Answer USING MARKDOWN SYNTAX about the UG academic rules of IITB ONLY from the provided transcript context. If the context is insufficient, just say you don't know. Don't start the sentences with "according to the transcript" or "according to the context provided". NEVER make it appear that you've been provided a contexy. When you want to quote the context, say "According to the UG Rulebook".
-----------------
Context:
{context}
-----------------
Question:
{question}
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

# Streamlit UI
st.set_page_config(page_title="PDF Chatbot", layout="wide")
st.title("💬 PDF Chatbot")

# Upload PDF
pdf_file = st.file_uploader("Upload a PDF", type="pdf")

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    with st.spinner("Processing PDF..."):
        vector_store = create_vector_store(tmp_path)
        st.session_state.vector_store = vector_store
        st.session_state.chat_chain = build_conversational_chain(vector_store)
        st.success("PDF processed and chatbot is ready!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
if "chat_chain" in st.session_state:
    user_input = st.text_input("Ask a question about the PDF:")

    if user_input:
        result = st.session_state.chat_chain(
            {
                "question": user_input,
                "chat_history": st.session_state.chat_history
            }
        )
        st.session_state.chat_history.append((user_input, result["answer"]))

        for q, a in st.session_state.chat_history:
            st.write(f"**You:** {q}")
            st.write(f"**Bot:** {a}")
