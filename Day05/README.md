# 🚗 Car Price Prediction using Machine Learning

## 📌 Overview

This project was completed as **Day 05** of the **Epochs Data Science Bootcamp 2026**.

The objective of this project is to build and compare multiple Machine Learning regression models to predict the selling price of used cars using the CarDekho Used Car Dataset.

---

## 📂 Dataset

- **Dataset:** CarDekho Used Car Dataset
- **Format:** CSV
- **Records:** Used car listings
- **Target Variable:** Selling_Price

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

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook

---

## 📊 Workflow

1. Load the dataset
2. Data cleaning and preprocessing
3. Exploratory Data Analysis (EDA)
4. Feature engineering
5. Feature encoding and scaling
6. Train-test split
7. Model training
8. Model evaluation
9. Performance comparison
10. Best model selection

---

## 🤖 Machine Learning Models Implemented

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

---

## 📈 Model Performance

| Model | MAE | MSE | RMSE | R² Score |
|--------|------------:|----------------:|------------:|---------:|
| Random Forest | 99,251.82 | 44,474,226,389.49 | 210,889.13 | 0.9409 |
| Decision Tree | 123,637.44 | 91,594,750,000.00 | 302,646.25 | 0.8783 |
| Linear Regression | 270,049.78 | 250,603,200,000.00 | 500,602.88 | 0.6671 |

---

## 🏆 Best Performing Model

**Random Forest Regressor** achieved the best overall performance.

### Justification

- Highest **R² Score (0.9409)**
- Lowest **Mean Absolute Error (MAE)**
- Lowest **Root Mean Squared Error (RMSE)**
- Better generalization by combining multiple decision trees, reducing overfitting and improving prediction accuracy.

Therefore, Random Forest Regressor was selected as the final model for predicting used car prices.

---

## 🔍 Key Observations

- Random Forest Regressor achieved the highest prediction accuracy among all evaluated models.
- Decision Tree Regressor performed significantly better than Linear Regression but was less accurate than Random Forest.
- Linear Regression served as a good baseline model but produced comparatively higher prediction errors.
- Tree-based models captured the nonlinear relationships in the dataset more effectively.
- Feature engineering and preprocessing contributed significantly to improving model performance.

---

## 🚀 Future Improvements

- Apply hyperparameter tuning using GridSearchCV or RandomizedSearchCV.
- Experiment with Gradient Boosting, XGBoost, LightGBM, and CatBoost regression models.
- Train the model on a larger and more diverse dataset.
- Perform k-fold cross-validation for more robust evaluation.
- Deploy the best-performing model as a web application using Flask or Streamlit.

---

## 📁 Project Structure

```text
Day05/
│
├── data/
│   ├── cardekho_dataset.csv
│   └── cardekho_dataset.zip
│
├── notebooks/
│   └── car_price_prediction.ipynb
│
├── images/
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