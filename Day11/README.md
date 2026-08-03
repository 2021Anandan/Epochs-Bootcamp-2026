# Production-Quality PDF Q&A Application

**Developed by:** ANANDAN M A | **MuLearn ID:** anandanma@mulearn  
**Event:** Epochs '26 Data Science Bootcamp (Day 11 Assignment)

An enterprise-grade, modular Retrieval-Augmented Generation (RAG) system built for intelligent document Q&A. This application enables users to upload PDF documents, index them into a persistent vector database, and converse with an AI assistant powered by **Google Gemini**, ensuring precise source citations and short-term session memory.

---

## 🏗️ Architecture & Modular Design

The codebase adheres strictly to separation of concerns and production coding standards (PEP8, type hinting, structured logging, and pathlib path handling):

```text
Day11/
│
├── data/               # Managed local storage for uploaded PDFs
├── chroma_db/          # Persistent vector database storage directory
├── utils.py            # Global configurations, constants, and logging setup
├── loader.py           # PDF document loading and metadata enrichment
├── splitter.py         # Recursive character text chunking
├── embeddings.py       # HuggingFace SentenceTransformer embedding factory
├── vector_store.py     # ChromaDB creation, persistence, and loading operations
├── memory.py           # Session-based chat history management
├── rag_chain.py        # Core LCEL RAG execution chain with Google Gemini
├── app.py              # Gradio web user interface entry point
└── requirements.txt    # Application dependencies
