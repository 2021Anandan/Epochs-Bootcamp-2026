import streamlit as st
import os
from langchain_core.output_parsers import StrOutputParser
from rag_pipeline import initialize_rag_system

st.set_page_config(page_title="PDF RAG Assistant — Epochs '26", page_icon="📄", layout="wide")

st.title("📄 PDF Question Answering Application (RAG)")
st.markdown("Upload your PDF document, index it into ChromaDB, and chat naturally with contextual memory.")

# Sidebar for PDF Upload and Indexing
with st.sidebar:
    st.header("📂 Document Management")
    uploaded_file = st.file_uploader("Upload a PDF file", type=[".pdf"])
    
    if st.button("🚀 Index PDF", type="primary"):
        if uploaded_file is not None:
            os.makedirs("data", exist_ok=True)
            pdf_path = os.path.join("data", uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Processing PDF, generating embeddings, and storing in ChromaDB..."):
                try:
                    st.session_state.retriever, st.session_state.prompt, st.session_state.llm, st.session_state.format_context = initialize_rag_system(pdf_path)
                    st.session_state.indexed = True
                    st.success("✅ PDF Indexed Successfully!")
                except Exception as e:
                    st.error(f"❌ Error indexing PDF: {str(e)}")
        else:
            st.warning("⚠️ Please upload a PDF file first.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your PDF..."):
    if not st.session_state.get("indexed", False):
        st.warning("⚠️ Please upload and index a PDF document using the sidebar first.")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate RAG response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    retrieved_docs = st.session_state.retriever.invoke(prompt)
                    context_text = st.session_state.format_context(retrieved_docs)
                    
                    formatted_history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages[:-1]]) if len(st.session_state.messages) > 1 else "No previous conversation."

                    chain = st.session_state.prompt | st.session_state.llm | StrOutputParser()
                    response = chain.invoke({
                        "context": context_text,
                        "history": formatted_history,
                        "question": prompt
                    })
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.error(error_msg)
