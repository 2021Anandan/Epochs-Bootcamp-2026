"""
rag_chain.py
------------
Builds and executes the core RAG retrieval and response generation chain
using Google Gemini and LangChain LCEL.
"""

from typing import Dict, Any, List, Tuple
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from memory import get_session_history
from utils import GEMINI_MODEL_NAME, TOP_K, logger

def format_docs_with_sources(docs: List[Any]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Formats retrieved documents into a single text block and extracts source metadata.
    
    Args:
        docs (List[Any]): Retrieved document chunks.
        
    Returns:
        Tuple[str, List[Dict[str, Any]]]: Formatted context string and a list of source references.
    """
    formatted_texts = []
    sources = []
    
    for doc in docs:
        source_name = doc.metadata.get("source", "Unknown Source")
        page_num = doc.metadata.get("page", "Unknown")
        formatted_texts.append(doc.page_content)
        sources.append({"source": source_name, "page": page_num, "content": doc.page_content[:150] + "..."})
        
    return "\n\n".join(formatted_texts), sources

def get_rag_response(
    vectorstore: Chroma, 
    user_query: str, 
    session_id: str = "default_user"
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Executes the end-to-end RAG pipeline for a given user query and session.
    
    Args:
        vectorstore (Chroma): The initialized vector database instance.
        user_query (str): The user's input question.
        session_id (str): Unique session identifier for memory tracking.
        
    Returns:
        Tuple[str, List[Dict[str, Any]]]: The generated answer string and a list of citation sources.
    """
    if not vectorstore:
        logger.warning("Attempted RAG query without an initialized vector store.")
        return "Please upload and process a PDF document first.", []
        
    logger.info(f"Executing RAG query for session '{session_id}': '{user_query}'")
    
    try:
        # Initialize Gemini model via LangChain
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_NAME,
            temperature=0.2,  # Low temperature for factual grounded answers
            convert_system_message_to_human=True
        )
        
        # Set up retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
        retrieved_docs = retriever.invoke(user_query)
        
        context_text, source_references = format_docs_with_sources(retrieved_docs)
        
        # Define rigorous prompt template with grounding constraint
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are an expert AI assistant designed for document-based question answering.\n"
                "Answer ONLY using the retrieved context provided below.\n"
                "If the answer is not available in the context, clearly say you don't know. "
                "Do not make up or fabricate facts.\n\n"
                "Retrieved Context:\n{context}"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Retrieve historical messages for this session
        chat_history_obj = get_session_history(session_id)
        
        # Build LCEL chain
        chain = prompt | llm | StrOutputParser()
        
        # Invoke chain
        answer = chain.invoke({
            "context": context_text,
            "chat_history": chat_history_obj.messages,
            "input": user_query
        })
        
        # Append interaction to chat history storage
        chat_history_obj.add_user_message(user_query)
        chat_history_obj.add_ai_message(answer)
        
        logger.info("RAG response generated successfully.")
        return answer, source_references
        
    except Exception as e:
        logger.error(f"Error during RAG response generation: {str(e)}", exc_info=True)
        return f"An error occurred while generating the response: {str(e)}", []