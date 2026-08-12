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
st.markdown("""
<style>

/* Background */
.stApp{
    background:#f5f7fb;
}

/* Main Title */
h1{
    text-align:center;
    color:#1f2937;
    font-weight:800;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#eef2ff;
    padding:20px;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{
    color:#374151;
}

/* Text Area */
.stTextArea textarea{
    border-radius:15px;
    border:2px solid #dbeafe;
    font-size:16px;
    padding:15px;
}

/* Text Input */
.stTextInput input{
    border-radius:12px;
    border:2px solid #dbeafe;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
    border-radius:12px;
}

/* Radio */
.stRadio{
    padding-bottom:10px;
}

/* Buttons */
.stButton>button{
    width:100%;
    border:none;
    border-radius:15px;
    background:linear-gradient(90deg,#ff4b6e,#ff6b6b);
    color:white;
    font-size:18px;
    font-weight:bold;
    padding:14px;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.02);
    background:linear-gradient(90deg,#ff416c,#ff4b2b);
}

/* Success Message */
.stSuccess{
    border-radius:15px;
}

/* Error */
.stError{
    border-radius:15px;
}

/* Warning */
.stWarning{
    border-radius:15px;
}

/* Info Card */
.info-card{
    background:#dbeafe;
    padding:18px;
    border-radius:15px;
    color:#1e3a8a;
    margin-top:20px;
}

/* Output Box */
.output-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
}

/* Footer */
.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)
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