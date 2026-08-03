"""
vector_store.py
---------------
Manages vector database operations using ChromaDB, including initialization,
persistence, and similarity retrieval.
"""

from typing import List, Tuple
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from utils import CHROMA_DB_DIR, logger

def create_vector_store(documents: List[Document], embedding_model: HuggingFaceEmbeddings, collection_name: str = "pdf_qa_collection") -> Chroma:
    """
    Creates a persistent Chroma vector store from a list of chunked documents.
    
    Args:
        documents (List[Document]): The chunked documents to index.
        embedding_model (HuggingFaceEmbeddings): The embedding model instance.
        collection_name (str): Name of the Chroma collection.
        
    Returns:
        Chroma: Initialized vector store object.
    """
    if not documents:
        logger.warning("No documents provided to create vector store.")
        raise ValueError("Cannot create vector store with an empty document list.")
        
    logger.info(f"Creating persistent ChromaDB collection '{collection_name}' at '{CHROMA_DB_DIR}'...")
    
    try:
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            collection_name=collection_name,
            persist_directory=str(CHROMA_DB_DIR)
        )
        logger.info(f"Successfully indexed {len(documents)} chunks into ChromaDB.")
        return vectorstore
    except Exception as e:
        logger.error(f"Failed to create vector store: {str(e)}", exc_info=True)
        raise RuntimeError(f"Vector database creation failed: {str(e)}") from e

def load_vector_store(embedding_model: HuggingFaceEmbeddings, collection_name: str = "pdf_qa_collection") -> Chroma | None:
    """
    Loads an existing persistent Chroma vector store from disk.
    
    Args:
        embedding_model (HuggingFaceEmbeddings): The embedding model instance.
        collection_name (str): Name of the Chroma collection.
        
    Returns:
        Chroma | None: Loaded vector store object or None if persistence folder is empty/missing.
    """
    if not CHROMA_DB_DIR.exists() or not any(CHROMA_DB_DIR.iterdir()):
        logger.info("No existing persistent vector store found on disk.")
        return None
        
    logger.info(f"Loading existing Chroma vector store from '{CHROMA_DB_DIR}'...")
    try:
        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=str(CHROMA_DB_DIR)
        )
        logger.info("Existing vector store loaded successfully.")
        return vectorstore
    except Exception as e:
        logger.error(f"Failed to load existing vector store: {str(e)}", exc_info=True)
        return None