import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------------------------
# Load Environment Variables
# ---------------------------------

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# ---------------------------------
# Streamlit Page Config
# ---------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Assistant")
st.write("Welcome to the AI Study Assistant powered by Google Gemini!")

# ---------------------------------
# Verify API Key
# ---------------------------------

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file.")
    st.stop()

# ---------------------------------
# Create Gemini Client
# ---------------------------------

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Unable to initialize Gemini:\n{e}")
    st.stop()

# ---------------------------------
# Sidebar
# ---------------------------------

st.sidebar.title("📚 Features")

feature = st.sidebar.radio(
    "Choose a feature:",
    [
        "Explain Concepts",
        "Summarize Notes",
        "Generate Quiz",
        "Answer Questions",
        "Revision Notes"
    ]
)

st.subheader(f"Selected Feature: {feature}")

# ---------------------------------
# User Input
# ---------------------------------

user_input = st.text_area(
    "Enter your study notes or question:",
    height=220,
    placeholder="Type your question or paste your notes here..."
)

generate = st.button("🚀 Generate")

# ---------------------------------
# Prompt Builder
# ---------------------------------

def build_prompt(feature, text):

    prompts = {
        "Explain Concepts":
            f"Explain the following concept in simple language with examples:\n\n{text}",

        "Summarize Notes":
            f"Summarize the following notes into important bullet points:\n\n{text}",

        "Generate Quiz":
            f"Generate 10 quiz questions with answers from the following notes:\n\n{text}",

        "Answer Questions":
            f"Answer the following question clearly and accurately:\n\n{text}",

        "Revision Notes":
            f"Convert the following notes into concise revision notes:\n\n{text}"
    }

    return prompts.get(feature, text)

# ---------------------------------
# Generate Response
# ---------------------------------

if generate:

    if not user_input.strip():
        st.warning("Please enter some text.")
        st.stop()

    prompt = build_prompt(feature, user_input)

    try:

        with st.spinner("Generating response..."):

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

        st.success("✅ Response Generated Successfully")

        st.markdown("---")
        st.subheader("AI Response")

        st.write(response.text)

    except Exception as e:
        st.error(f"❌ Error:\n{e}")