"""
embeddings.py
-------------
Initializes and configures the HuggingFace SentenceTransformer embedding model.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from utils import EMBEDDING_MODEL_NAME, logger

def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Initializes and returns the SentenceTransformer embedding model instance.
    
    Returns:
        HuggingFaceEmbeddings: Configured embedding model object.
    """
    logger.info(f"Loading embedding model: '{EMBEDDING_MODEL_NAME}'...")
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={"device": "cpu"},  # Change to 'cuda' if GPU acceleration is preferred
            encode_kwargs={"normalize_embeddings": True}  # Normalizes vectors for accurate cosine similarity
        )
        logger.info("Embedding model loaded successfully.")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to load embedding model {EMBEDDING_MODEL_NAME}: {str(e)}", exc_info=True)
        raise RuntimeError(f"Embedding initialization failed: {str(e)}") from e