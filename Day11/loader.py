"""
loader.py
---------
Handles loading of PDF documents into LangChain Document objects 
with robust error handling and metadata enrichment.
"""

from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from utils import logger

def load_pdf_documents(file_path: str | Path) -> List[Document]:
    """
    Loads a PDF file page by page and attaches source metadata.
    
    Args:
        file_path (str | Path): The absolute or relative path to the target PDF file.
        
    Returns:
        List[Document]: A list of LangChain Document objects containing page content and metadata.
        
    Raises:
        FileNotFoundError: If the PDF file does not exist at the given path.
        ValueError: If the file path is invalid or parsing fails.
    """
    path_obj = Path(file_path)
    
    if not path_obj.exists():
        logger.error(f"PDF file not found at path: {path_obj.resolve()}")
        raise FileNotFoundError(f"The file {path_obj} does not exist.")
        
    if path_obj.suffix.lower() != ".pdf":
        logger.error(f"Invalid file format provided: {path_obj.suffix}. Expected '.pdf'.")
        raise ValueError("Only PDF documents are supported by this loader.")
        
    logger.info(f"Loading PDF document: {path_obj.name}...")
    
    try:
        loader = PyPDFLoader(str(path_obj))
        documents = loader.load()
        
        if not documents:
            logger.warning(f"The PDF file {path_obj.name} appears to be empty.")
            return []
            
        # Enrich metadata with clean source filenames and 1-based page numbers
        for idx, doc in enumerate(documents, start=1):
            doc.metadata["source"] = path_obj.name
            doc.metadata["page"] = doc.metadata.get("page", idx)
            
        logger.info(f"Successfully loaded {len(documents)} pages from {path_obj.name}.")
        return documents
        
    except Exception as e:
        logger.error(f"Failed to parse PDF document {path_obj.name}: {str(e)}", exc_info=True)
        raise RuntimeError(f"PDF parsing error: {str(e)}") from e