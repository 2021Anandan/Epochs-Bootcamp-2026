import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from rag_pipeline import initialize_rag_system

qa_chain = None
retriever_global = None
prompt_global = None
llm_global = None
format_context_global = None

def index_pdf(file_obj):
    global qa_chain, retriever_global, prompt_global, llm_global, format_context_global
    if file_obj is None:
        return "⚠️ Please upload a PDF file first."
    
    try:
        pdf_path = file_obj.name if hasattr(file_obj, "name") else file_obj
        retriever_global, prompt_global, llm_global, format_context_global = initialize_rag_system(pdf_path)
        return "✅ PDF Indexed Successfully! You can now ask questions below."
    except Exception as e:
        return f"❌ Error indexing PDF: {str(e)}"

def chat_with_pdf(message, history):
    global retriever_global, prompt_global, llm_global, format_context_global
    if retriever_global is None:
        return "⚠️ Please upload and index a PDF document first."

    try:
        retrieved_docs = retriever_global.invoke(message)
        context_text = format_context_global(retrieved_docs)
        formatted_history = "\n".join([f"User: {h[0]}\nAssistant: {h[1]}" for h in history]) if history else "No previous conversation."

        chain = prompt_global | llm_global | StrOutputParser()
        response = chain.invoke({
            "context": context_text,
            "history": formatted_history,
            "question": message
        })
        return response
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📄 PDF RAG Assistant — Epochs '26 Day 11")
    gr.Markdown("Upload your PDF document, index it into ChromaDB, and chat naturally with contextual memory!")

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            index_btn = gr.Button("🚀 Index PDF", variant="primary")
            status_output = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(
                fn=chat_with_pdf,
                textbox=gr.Textbox(placeholder="Ask a question about your PDF...", container=False, scale=7),
                title="Document Q&A Chatbot",
            )

    index_btn.click(fn=index_pdf, inputs=[file_input], outputs=[status_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
