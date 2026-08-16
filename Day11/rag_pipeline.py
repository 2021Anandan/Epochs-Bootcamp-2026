import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_rag_system(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunked_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        collection_name="pdf_rag_collection"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.2,
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template(
        "You are an expert research assistant.\n"
        "Answer the user's question accurately using ONLY the provided context below.\n"
        "If the answer cannot be found in the context, say 'I cannot find the answer in the provided document.'\n\n"
        "Context:\n{context}\n\n"
        "Conversation History:\n{history}\n\n"
        "Question: {question}\n"
        "Answer:"
    )

    def format_context(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    return retriever, prompt, llm, format_context
