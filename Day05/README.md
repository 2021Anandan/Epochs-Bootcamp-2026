# 🚗 Car Price Prediction using Machine Learning

## 📌 Overview

This project was completed as **Day 05** of the **Epochs Data Science Bootcamp 2026**.

The objective is to build and compare multiple Machine Learning regression models to predict the selling price of used cars using the CarDekho dataset.

---

## 📂 Dataset

- Dataset: CarDekho Used Car Dataset
- Format: CSV
- Records: Used car listings
- Target Variable: Selling Price

---
## 📋 Features

### Numerical Features
- Year
- Present_Price
- Kms_Driven
- Owner

### Categorical Features
- Fuel_Type
- Seller_Type
- Transmission

### Target Variable
- Selling_Price

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

---

## 📊 Workflow

1. Load Dataset
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Train-Test Split
6. Model Training
7. Model Evaluation
8. Performance Comparison

---

## 🤖 Machine Learning Models

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

---

## 📈 Model Performance

## 📈 Model Performance

| Model | MAE | MSE | RMSE | R² Score |
|--------|------------:|----------------:|------------:|---------:|
| Random Forest | 99,251.82 | 44,474,226,389.49 | 210,889.13 | 0.9409 |
| Decision Tree | 123,637.44 | 91,594,750,000.00 | 302,646.25 | 0.8783 |
| Linear Regression | 270,049.78 | 250,603,200,000.00 | 500,602.88 | 0.6671 |

**Best Model:** Random Forest Regressor

The Random Forest Regressor achieved the highest R² Score (0.9409) while also producing the lowest MAE and RMSE among the evaluated models. This indicates that it provides the most accurate predictions for the CarDekho used car price dataset.

**Best Model:** Random Forest Regressor

---

## 📁 Project Structure

```
Day05/
│
├── data/
│   ├── cardekho_dataset.csv
│   └── cardekho_dataset.zip
│
├── notebooks/
│   └── car_price_prediction.ipynb
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 👨‍💻 Author

**Anandan M A**

B.Tech Computer Science & Engineering

Epochs Data Science Bootcamp 2026