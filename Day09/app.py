from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "model.pkl"
ENCODER_PATH = BASE_DIR / "model" / "encoders.pkl"

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗"
)

st.title("🚗 Car Price Prediction")

# --------------------------------------------------
# Get the directory where app.py is located
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# --------------------------------------------------
# Load Model and Encoders
# --------------------------------------------------
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
ENCODER_PATH = BASE_DIR / "model" / "encoders.pkl"

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)