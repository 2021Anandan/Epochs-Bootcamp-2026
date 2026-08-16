# Day 08 – Model Optimization using Decision Tree and GridSearchCV
**Participant Name:** Anandan M A  
**MUID:** anandanma@mulearn

---

# Project Summary

This project demonstrates the optimization of a **Decision Tree Classifier** for predicting customer churn using **GridSearchCV**. A baseline model is first trained and evaluated, followed by hyperparameter tuning to improve model performance. The optimized model is compared with the baseline using multiple evaluation metrics, and feature importance is analyzed to understand the key factors influencing customer churn.

---

# Objectives

- Load and explore the Customer Churn dataset.
- Perform data preprocessing and feature encoding.
- Split the dataset into training and testing sets.
- Build a baseline Decision Tree Classifier.
- Evaluate the baseline model.
- Optimize the model using GridSearchCV.
- Compare baseline and optimized models.
- Analyze feature importance.

---

# Dataset

- **Dataset:** Customer Churn Dataset
- **Problem Type:** Binary Classification
- **Target Variable:** Churn

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

# Project Workflow

1. Import Required Libraries
2. Load the Dataset
3. Explore the Dataset
4. Data Preprocessing
5. Train-Test Split
6. Train Baseline Decision Tree Model
7. Evaluate Baseline Model
8. Generate Confusion Matrix
9. Optimize Model using GridSearchCV
10. Evaluate Optimized Model
11. Compare Model Performance
12. Analyze Feature Importance
13. Visualize Feature Importance
14. Draw Conclusions

---

# Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Classification Report
- Confusion Matrix

---

# Hyperparameter Optimization

GridSearchCV with **5-Fold Cross Validation** was used to identify the best combination of Decision Tree hyperparameters.

Parameters tuned include:

- Criterion
- Maximum Depth
- Minimum Samples Split
- Minimum Samples Leaf

---

# Results

- Successfully trained a baseline Decision Tree model.
- Improved model selection using GridSearchCV.
- Compared baseline and optimized models.
- Evaluated performance using multiple classification metrics.
- Identified the most influential features affecting customer churn.

---

# Conclusion

This project demonstrates the importance of model optimization in machine learning. Hyperparameter tuning using GridSearchCV improved the model selection process and provided a systematic approach to finding the best-performing Decision Tree model. Feature importance analysis also helped identify the key variables contributing to customer churn prediction.

---

# Repository Structure

```
Day08/
│
├── data/
│   └── customer_churn_dataset-testing-master.csv
│
├── images/
├── models/
│
├── model_optimization.ipynb
├── README.md
└── requirements.txt
```

---

**Epochs Bootcamp 2026 | Day 08 – Model Optimization**