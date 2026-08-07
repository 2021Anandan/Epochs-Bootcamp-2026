"""
Main Streamlit application for Production RAG PDF Q&A system
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict

import streamlit as st

from loader import load_pdf_documents
from splitter import split_documents
from embeddings import get_embedding_model
from vector_store import create_vector_store, load_vector_store
from rag_chain import get_rag_response
from memory import clear_session_history
from utils import DATA_DIR, CHROMA_DB_DIR, logger

# ==========================================
# API KEY CHECK
# ==========================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ==========================================
# GLOBAL STATE
# ==========================================

current_vectorstore = None
embedding_model_instance = None

# ==========================================
# INITIALIZATION
# ==========================================

def initialize_system():
    global current_vectorstore, embedding_model_instance

    try:
        embedding_model_instance = get_embedding_model()
        current_vectorstore = load_vector_store(embedding_model_instance)

        if current_vectorstore:
            logger.info("Loaded existing vector store.")
        else:
            logger.info("No vector store found. Ready for upload.")

    except Exception as e:
        logger.error(f"Initialization error: {str(e)}", exc_info=True)

# ==========================================
# PDF PROCESSING
# ==========================================

def process_uploaded_pdf(file_obj):
    global current_vectorstore, embedding_model_instance

    if not GOOGLE_API_KEY:
        return "⚠️ API key missing."

    if file_obj is None:
        return "⚠️ Upload a PDF."

    try:
        file_path = DATA_DIR / file_obj.name

        with open(file_path, "wb") as f:
            f.write(file_obj.getbuffer())

        docs = load_pdf_documents(file_path)
        chunks = split_documents(docs)

        if not embedding_model_instance:
            embedding_model_instance = get_embedding_model()

        current_vectorstore = create_vector_store(chunks, embedding_model_instance)

        return f"✅ Indexed {len(chunks)} chunks"

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return f"❌ Error: {str(e)}"

# ==========================================
# CHAT
# ==========================================

def chat_interface(user_input, history):
    global current_vectorstore

    if not GOOGLE_API_KEY:
        return history, "⚠️ API key missing."

    if current_vectorstore is None:
        return history, "⚠️ Upload PDF first."

    try:
        answer, sources = get_rag_response(
            current_vectorstore,
            user_input,
            session_id="default_user"
        )

        history.append({"user": user_input, "bot": answer})

        source_text = "### 📚 Sources\n\n"
        for i, src in enumerate(sources, 1):
            source_text += f"[{i}] {src['source']} (Page {src['page']})\n"

        return history, source_text

    except Exception as e:
        return history, f"❌ Error: {str(e)}"

# ==========================================
# CLEAR FUNCTIONS
# ==========================================

def clear_chat():
    clear_session_history("default_user")
    return []

def clear_database():
    global current_vectorstore
    current_vectorstore = None

    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)
        CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

    return "Database cleared"

# ==========================================
# MAIN STREAMLIT UI
# ==========================================

def main():
    st.set_page_config(page_title="RAG PDF Chat", layout="wide")

    st.title("📄 Production PDF Q&A Assistant")
    st.write("Developed by ANANDAN M A")

    initialize_system()

    # Upload Section
    st.subheader("Upload PDF")
    uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])

    if st.button("Process PDF"):
        result = process_uploaded_pdf(uploaded_file)
        st.info(result)

    # Chat Section
    st.subheader("Chat")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("Ask a question")

    if st.button("Send"):
        st.session_state.history, sources = chat_interface(
            user_input,
            st.session_state.history
        )

        if st.session_state.history:
            st.write(st.session_state.history[-1]["bot"])
            st.markdown(sources)

    # Controls
    st.subheader("Controls")

    if st.button("Clear Chat"):
        st.session_state.history = clear_chat()

    if st.button("Clear Database"):
        msg = clear_database()
        st.warning(msg)