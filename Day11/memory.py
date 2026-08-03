"""
memory.py
---------
Manages session-based conversation message histories for multi-turn chats.
"""

from typing import Dict
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from utils import logger

# In-memory store for session histories
# Key: session_id (str), Value: ChatMessageHistory instance
store: Dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieves or creates a chat message history object for a given session ID.
    
    Args:
        session_id (str): Unique identifier for the user session.
        
    Returns:
        BaseChatMessageHistory: The message history storage instance.
    """
    if session_id not in store:
        logger.info(f"Initializing new chat history storage for session_id: '{session_id}'")
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def clear_session_history(session_id: str) -> None:
    """
    Clears the conversation history for a specific session.
    
    Args:
        session_id (str): Unique identifier for the user session.
    """
    if session_id in store:
        store[session_id].clear()
        logger.info(f"Cleared chat history for session_id: '{session_id}'")