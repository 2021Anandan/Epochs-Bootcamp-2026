"""
splitter.py
-----------
Provides logic to split large PDF documents into smaller, overlapping chunks 
using a recursive character strategy while preserving metadata.
"""

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import CHUNK_SIZE, CHUNK_OVERLAP, logger

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Takes a list of loaded PDF documents and splits them into smaller text chunks.
    
    Args:
        documents (List[Document]): The raw page documents loaded from the PDF.
        
    Returns:
        List[Document]: A list of chunked Document objects with preserved metadata.
        
    Raises:
        ValueError: If the input document list is empty.
    """
    if not documents:
        logger.warning("Empty document list passed to chunking pipeline.")
        return []
        
    logger.info(
        f"Initializing text splitter with chunk_size={CHUNK_SIZE} "
        f"and chunk_overlap={CHUNK_OVERLAP}..."
    )
    
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            add_start_index=True
        )
        
        chunks = splitter.split_documents(documents)
        
        logger.info(f"Successfully split {len(documents)} pages into {len(chunks)} chunks.")
        return chunks
        
    except Exception as e:
        logger.error(f"Error occurred during text chunking: {str(e)}", exc_info=True)
        raise RuntimeError(f"Text splitting failed: {str(e)}") from e