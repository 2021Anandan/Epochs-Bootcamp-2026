"""
Main Gradio user interface application entry point for the Production RAG PDF Q&A system.
"""

import os
import shutil
from pathlib import Path
from typing import Tuple, List, Dict
import gradio as gr

from loader import load_pdf_documents
from splitter import split_documents
from embeddings import get_embedding_model
from vector_store import create_vector_store, load_vector_store
from rag_chain import get_rag_response
from memory import clear_session_history
from utils import DATA_DIR, CHROMA_DB_DIR, logger

# ==========================================
# API KEY CHECK (Fallback Safety)
# ==========================================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("⚠️ WARNING: GOOGLE_API_KEY is not set. App will run in limited mode.")

# ==========================================
# GLOBAL STATE
# ==========================================
current_vectorstore = None
embedding_model_instance = None

# ==========================================
# INITIALIZATION
# ==========================================
def initialize_system() -> None:
    """Initialize embedding model and load existing vector store."""
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


initialize_system()

# ==========================================
# PDF PROCESSING
# ==========================================
def process_uploaded_pdf(file_obj) -> str:
    global current_vectorstore, embedding_model_instance

    # API KEY FALLBACK
    if not GOOGLE_API_KEY:
        return "⚠️ API key missing. Cannot process PDF."

    if file_obj is None:
        return "⚠️ Please upload a valid PDF file."

    try:
        file_path = Path(file_obj.name)
        target_path = DATA_DIR / file_path.name
        shutil.copy(file_path, target_path)

        docs = load_pdf_documents(target_path)
        if not docs:
            return "❌ Failed to load PDF."

        chunks = split_documents(docs)
        if not chunks:
            return "❌ No chunks created."

        if not embedding_model_instance:
            embedding_model_instance = get_embedding_model()

        current_vectorstore = create_vector_store(chunks, embedding_model_instance)

        return f"✅ Indexed {len(chunks)} chunks successfully."

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return f"❌ Error: {str(e)}"

# ==========================================
# CHAT HANDLER
# ==========================================
def chat_interface_handler(user_message: str, history: List[Dict[str, str]]):

    # API KEY FALLBACK
    if not GOOGLE_API_KEY:
        history.append({"role": "user", "content": user_message})
        history.append({
            "role": "assistant",
            "content": "⚠️ API key not configured. Cannot generate AI response."
        })
        return "", history, "⚠️ API key missing."

    global current_vectorstore

    if not user_message.strip():
        return "", history, "No query provided."

    if current_vectorstore is None:
        msg = "⚠️ Upload and process a PDF first."
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": msg})
        return "", history, "No database."

    try:
        answer, sources = get_rag_response(
            current_vectorstore,
            user_message,
            session_id="default_user"
        )

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": answer})

        formatted_sources = "### 📚 Sources\n\n"

        if sources:
            for i, src in enumerate(sources, 1):
                formatted_sources += f"**[{i}] {src['source']} (Page {src['page']})**\n"
                formatted_sources += f"> {src['content']}\n\n"
        else:
            formatted_sources += "No sources found."

        return "", history, formatted_sources

    except Exception as e:
        logger.error(str(e), exc_info=True)
        return "", history, f"❌ Error: {str(e)}"

# ==========================================
# CLEAR FUNCTIONS
# ==========================================
def clear_conversation():
    clear_session_history("default_user")
    return [], "Conversation cleared."

def clear_database():
    global current_vectorstore
    current_vectorstore = None

    try:
        if CHROMA_DB_DIR.exists():
            shutil.rmtree(CHROMA_DB_DIR)
            CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

        return "🧹 Database cleared."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==========================================
# UI
# ==========================================
app_theme = gr.themes.Soft()

with gr.Blocks(theme=app_theme) as demo:

    # API WARNING UI
    if not GOOGLE_API_KEY:
        gr.Markdown(
            "⚠️ **API Key Missing**\n\n"
            "App will run in limited mode. AI responses disabled."
        )

    gr.Markdown("# 📄 Production PDF Q&A Assistant")
    gr.Markdown("Developed by ANANDAN M A")

    with gr.Row():

        # LEFT PANEL
        with gr.Column(scale=1):
            gr.Markdown("### Upload PDF")
            pdf_input = gr.File(file_types=[".pdf"])
            upload_btn = gr.Button("Process PDF")
            status_box = gr.Textbox(label="Status")

            gr.Markdown("### Controls")
            clear_chat_btn = gr.Button("Clear Chat")
            clear_db_btn = gr.Button("Wipe DB")
            db_status = gr.Textbox(label="DB Status")

        # RIGHT PANEL
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=400)
            msg = gr.Textbox(label="Ask question")
            sources_box = gr.Markdown()

    # EVENTS
    upload_btn.click(process_uploaded_pdf, pdf_input, status_box)

    msg.submit(
        chat_interface_handler,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, sources_box]
    )

    clear_chat_btn.click(clear_conversation, outputs=[chatbot, status_box])
    clear_db_btn.click(clear_database, outputs=db_status)

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)