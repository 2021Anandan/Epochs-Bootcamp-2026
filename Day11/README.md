# PDF Question Answering Application (RAG) — Epochs '26 Day 11

## Participant Information
- **Participant Name:** Anandan M. A.
- **MUID:** [Insert your MUID]

## Project Overview
An intelligent PDF Question Answering system built using Retrieval-Augmented Generation (RAG). It ingests custom PDF documents, parses and chunks text structurally, embeds data using HuggingFace models, stores vectors efficiently via ChromaDB, and generates context-aware answers using a lightweight open-source LLM with conversational memory support.

## Technologies Used
- **LangChain & LangChain-HuggingFace:** Orchestration framework and model wrappers.
- **ChromaDB:** Local vector database for Approximate Nearest Neighbor (ANN) search.
- **HuggingFace Transformers / Sentence-Transformers:** Local embedding generation (ll-MiniLM-L6-v2) and text generation (Qwen2-0.5B-Instruct).
- **Gradio:** Interactive web UI for file uploads and chatting.

## Memory Implementation
Maintains multi-turn conversation state by passing past interaction logs directly into the prompt template architecture alongside retrieved document contexts.

## Challenges Faced
- Managing model context limitations during initial fixed-size chunking. Solved by shifting to a recursive character splitting strategy with optimal overlap.

## Future Improvements
- Incorporate hybrid keyword search (BM25) alongside dense vector retrieval for exact-match accuracy.
- Implement cross-encoder reranking for enhanced precision.
