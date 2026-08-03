"""
app.py
------
Main Gradio user interface application entry point for the Production RAG PDF Q&A system.
"""

import os
import shutil
from pathlib import Path
from typing import Tuple, List, Dict, Union
import gradio as gr

from loader import load_pdf_documents
from splitter import split_documents
from embeddings import get_embedding_model
from vector_store import create_vector_store, load_vector_store
from rag_chain import get_rag_response
from memory import clear_session_history
from utils import DATA_DIR, CHROMA_DB_DIR, logger

# Global state to track active vector store in memory
current_vectorstore = None
embedding_model_instance = None

def initialize_system() -> None:
    """Initializes the embedding model and attempts to load an existing vector store on startup."""
    global current_vectorstore, embedding_model_instance
    try:
        embedding_model_instance = get_embedding_model()
        current_vectorstore = load_vector_store(embedding_model_instance)
        if current_vectorstore:
            logger.info("System initialized: Loaded existing vector store from disk.")
        else:
            logger.info("System initialized: No existing vector store found. Ready for PDF uploads.")
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}", exc_info=True)

# Initialize on module load
initialize_system()

def process_uploaded_pdf(file_obj) -> str:
    """
    Handles PDF file upload, parsing, splitting, embedding, and vector DB indexing.
    """
    global current_vectorstore, embedding_model_instance
    
    if file_obj is None:
        return "⚠️ Please upload a valid PDF file first."
        
    try:
        file_path = Path(file_obj.name)
        target_path = DATA_DIR / file_path.name
        shutil.copy(file_path, target_path)
        
        logger.info(f"Processing uploaded file: {target_path.name}")
        
        docs = load_pdf_documents(target_path)
        if not docs:
            return "❌ Failed to load documents from the PDF. The file may be empty or unreadable."
            
        chunks = split_documents(docs)
        if not chunks:
            return "❌ Document splitting resulted in zero chunks."
            
        if not embedding_model_instance:
            embedding_model_instance = get_embedding_model()
            
        current_vectorstore = create_vector_store(chunks, embedding_model_instance)
        
        return f"✅ Success! Indexed {len(chunks)} text chunks from '{target_path.name}' into ChromaDB."
        
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}", exc_info=True)
        return f"❌ Error processing PDF: {str(e)}"

def chat_interface_handler(user_message: str, history: List[Dict[str, str]]) -> Tuple[str, List[Dict[str, str]], str]:
    """
    Handles chat interaction, invokes the RAG chain, and formats source citations using dictionary messages.
    """
    global current_vectorstore
    
    if not user_message.strip():
        return "", history, "No query provided."
        
    if current_vectorstore is None:
        bot_response = "⚠️ Please upload and process a PDF document before asking questions."
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": bot_response})
        return "", history, "No active vector database found."
        
    # Execute RAG response generation
    answer, sources = get_rag_response(current_vectorstore, user_message, session_id="default_user")
    
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": answer})
    
    # Format source citations for UI display
    formatted_sources = "### 📚 Retrieved Source Citations\n\n"
    if sources:
        for idx, src in enumerate(sources, start=1):
            formatted_sources += f"**[{idx}] File:** `{src['source']}` | **Page:** `{src['page']}`\n"
            formatted_sources += f"> *{src['content']}*\n\n"
    else:
        formatted_sources += "No specific sources cited for this response."
        
    return "", history, formatted_sources

def clear_conversation() -> Tuple[List, str]:
    """Clears conversation memory and chat UI window."""
    clear_session_history("default_user")
    logger.info("Chat history cleared by user.")
    return [], "Conversation history cleared."

def clear_database() -> str:
    """Wipes the persistent vector database from disk and memory."""
    global current_vectorstore
    current_vectorstore = None
    
    try:
        if CHROMA_DB_DIR.exists():
            shutil.rmtree(CHROMA_DB_DIR)
            CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Vector database wiped successfully.")
        return "🧹 Vector database and persistent storage wiped successfully."
    except Exception as e:
        logger.error(f"Failed to clear database: {str(e)}", exc_info=True)
        return f"❌ Error clearing database: {str(e)}"

# ==========================================
# GRADIO UI LAYOUT
# ==========================================
app_theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="indigo",
)

with gr.Blocks(theme=app_theme, title="Epochs Day 11 — Production RAG PDF Q&A") as demo:
    gr.Markdown("# 📚 Production-Quality PDF Q&A Assistant")
    gr.Markdown(
        "**Developed by:** ANANDAN M A | **MuLearn ID:** `anandanma@mulearn`\n\n"
        "Build a professional Retrieval-Augmented Generation (RAG) system powered by **LangChain**, "
        "**ChromaDB**, **SentenceTransformers**, and the **Google Gemini API**."
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1️⃣ Document Ingestion")
            pdf_file_input = gr.File(
                label="Upload PDF Document",
                file_types=[".pdf"],
                type="filepath"
            )
            upload_btn = gr.Button("Process & Index PDF", variant="primary")
            status_output = gr.Textbox(label="Ingestion Status", interactive=False)
            
            gr.Markdown("### ⚙️ System Controls")
            with gr.Row():
                clear_chat_btn = gr.Button("Clear Chat")
                clear_db_btn = gr.Button("Wipe Database", variant="stop")
            db_status_output = gr.Textbox(label="Database Status", interactive=False)
            
        with gr.Column(scale=2):
            gr.Markdown("### 2️⃣ Interactive Chat & Citations")
            chatbot = gr.Chatbot(label="PDF Assistant Chat Window", height=400)
            msg_input = gr.Textbox(
                label="Ask a question about your PDF...",
                placeholder="Type your question here and press Enter...",
                lines=2
            )
            sources_box = gr.Markdown(label="Source Citations", value="*Sources will appear here after querying.*")
            
    # Event Wiring
    upload_btn.click(fn=process_uploaded_pdf, inputs=pdf_file_input, outputs=status_output)
    
    msg_input.submit(
        fn=chat_interface_handler,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot, sources_box]
    )
    
    clear_chat_btn.click(fn=clear_conversation, outputs=[chatbot, status_output])
    clear_db_btn.click(fn=clear_database, outputs=[db_status_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)