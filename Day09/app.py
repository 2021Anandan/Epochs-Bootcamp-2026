import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")

st.title("🚗 Car Price Prediction")

model = joblib.load("model/model.pkl")
encoders = joblib.load("model/encoders.pkl")

car_name = st.selectbox(
    "Car Name",
    encoders["car_name"].classes_
)

brand = st.selectbox(
    "Brand",
    encoders["brand"].classes_
)

model_name = st.selectbox(
    "Model",
    encoders["model"].classes_
)

vehicle_age = st.number_input("Vehicle Age",1,30,5)

km_driven = st.number_input("Kilometers Driven",0,500000,50000)

seller_type = st.selectbox(
    "Seller Type",
    encoders["seller_type"].classes_
)

fuel_type = st.selectbox(
    "Fuel Type",
    encoders["fuel_type"].classes_
)

transmission = st.selectbox(
    "Transmission",
    encoders["transmission_type"].classes_
)

mileage = st.number_input("Mileage",5.0,40.0,18.0)

engine = st.number_input("Engine CC",500,5000,1200)

max_power = st.number_input("Max Power",20.0,500.0,80.0)

seats = st.number_input("Seats",2,10,5)

if st.button("Predict Price"):

    data = pd.DataFrame({
        "car_name":[encoders["car_name"].transform([car_name])[0]],
        "brand":[encoders["brand"].transform([brand])[0]],
        "model":[encoders["model"].transform([model_name])[0]],
        "vehicle_age":[vehicle_age],
        "km_driven":[km_driven],
        "seller_type":[encoders["seller_type"].transform([seller_type])[0]],
        "fuel_type":[encoders["fuel_type"].transform([fuel_type])[0]],
        "transmission_type":[encoders["transmission_type"].transform([transmission])[0]],
        "mileage":[mileage],
        "engine":[engine],
        "max_power":[max_power],
        "seats":[seats]
    })

    prediction = model.predict(data)

    st.success(f"Estimated Price: ₹ {prediction[0]:,.0f}")