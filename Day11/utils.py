"""
utils.py
--------
Centralized configuration, logging setup, and directory path management 
for the Production RAG PDF Q&A application.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# ==========================================
# DIRECTORY PATHS CONFIGURATION
# ==========================================
BASE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = BASE_DIR / "data"
CHROMA_DB_DIR: Path = BASE_DIR / "chroma_db"

# Ensure runtime directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# RAG HYPERPARAMETERS & CONSTANTS
# ==========================================
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
TOP_K: int = 4
GEMINI_MODEL_NAME = "gemini-3.6-flash"

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a standardized logger with INFO level.
    
    Args:
        name (str): Name of the module requesting the logger.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

# Global application logger
logger = setup_logger("RAG_App")

# ==========================================
# ENVIRONMENT VALIDATION
# ==========================================
def validate_environment() -> None:
    """
    Validates that essential environment variables are configured.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.warning("GOOGLE_API_KEY environment variable is not set! Ensure it is provided before invoking Gemini.")
    else:
        logger.info("Environment validation passed: GOOGLE_API_KEY detected.")

# Run validation on import
validate_environment()