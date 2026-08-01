from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Load Model & Encoders
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "model.pkl"
ENCODER_PATH = BASE_DIR / "model" / "encoders.pkl"

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🚗 Used Car Price Predictor")

st.write(
    "Estimate the resale value of a used car. "
    "Fill in the car's details in the sidebar and get an instant prediction."
)


st.info("Set the car details in the sidebar, then click **Predict Price**.")
# --------------------------------------------------
# Sidebar Inputs
# --------------------------------------------------
st.sidebar.header("🚘 Car Details")

car_name = st.sidebar.selectbox(
    "Car Name",
    sorted(encoders["car_name"].classes_)
)

brand = st.sidebar.selectbox(
    "Brand",
    sorted(encoders["brand"].classes_)
)

car_model = st.sidebar.selectbox(
    "Model",
    sorted(encoders["model"].classes_)
)

vehicle_age = st.sidebar.slider(
    "Vehicle Age (Years)",
    0, 30, 5
)

km_driven = st.sidebar.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000,
    step=1000
)

seller_type = st.sidebar.selectbox(
    "Seller Type",
    encoders["seller_type"].classes_
)

fuel_type = st.sidebar.selectbox(
    "Fuel Type",
    encoders["fuel_type"].classes_
)

transmission = st.sidebar.selectbox(
    "Transmission",
    encoders["transmission_type"].classes_
)
mileage = st.sidebar.number_input(
    "Mileage (km/l)",
    min_value=0.0,
    value=18.0,
    step=0.1
)

engine = st.sidebar.number_input(
    "Engine (CC)",
    min_value=500,
    value=1200,
    step=100
)

max_power = st.sidebar.number_input(
    "Max Power (bhp)",
    min_value=20.0,
    value=80.0,
    step=1.0
)

seats = st.sidebar.number_input(
    "Seats",
    min_value=2,
    max_value=10,
    value=5,
    step=1
)


predict = st.sidebar.button("🚀 Predict Price")

if predict:
    try:
        # Encode categorical inputs
        car_name_enc = encoders["car_name"].transform([car_name])[0]
        brand_enc = encoders["brand"].transform([brand])[0]
        model_enc = encoders["model"].transform([car_model])[0]
        seller_type_enc = encoders["seller_type"].transform([seller_type])[0]
        fuel_type_enc = encoders["fuel_type"].transform([fuel_type])[0]
        transmission_enc = encoders["transmission_type"].transform([transmission])[0]

        # Create input DataFrame
        input_data = pd.DataFrame([{
            "car_name": car_name_enc,
            "brand": brand_enc,
            "model": model_enc,
            "vehicle_age": vehicle_age,
            "km_driven": km_driven,
            "seller_type": seller_type_enc,
            "fuel_type": fuel_type_enc,
            "transmission_type": transmission_enc,
            "mileage": mileage,
            "engine": engine,
            "max_power": max_power,
            "seats": seats
        }])

        # Predict
        prediction = model.predict(input_data)[0]

        # Show Result
        st.success("### 💰 Estimated Car Price")

        st.markdown(
            f"""
            <div style="
                background-color:#d4edda;
                padding:35px;
                border-radius:10px;
                text-align:center;
                font-size:42px;
                font-weight:bold;
                color:#155724;
            ">
                ₹ {prediction:,.0f}
            </div>
            """,
            unsafe_allow_html=True
        )

        # About Model
        with st.expander("ℹ About this Model"):
            st.markdown("""
- **Algorithm:** Random Forest Regressor
- **Dataset:** CarDekho Used Car Dataset
- **Framework:** Streamlit
- **Developer:** Anandan M A
- **µLearn ID:** anandanma@mulearn
- **GitHub:** https://github.com/2021Anandan
- **Live Demo:** https://epochs-bootcamp-2026-....
""")

    except Exception as e:
        st.error(f"Prediction Error: {e}")