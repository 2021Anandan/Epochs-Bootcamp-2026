# Day 07 – Customer Segmentation using K-Means Clustering

## Participant Details

**Name:** Anandan M A  
**MUID:** anandanma@mulearn

---

## Business Objective

The objective of this project is to segment mall customers into meaningful groups using the K-Means Clustering algorithm. These customer segments help businesses understand customer behavior and develop targeted marketing strategies.

## Dataset

**Dataset:** Mall Customer Segmentation Dataset

**Features**
- CustomerID
- Gender
- Age
- Annual Income (k$)
- Spending Score (1–100)

## Preprocessing

- Checked for missing values
- Encoded the Gender column
- Selected Annual Income and Spending Score for clustering
- Applied StandardScaler before K-Means

## Model Implementation

- Elbow Method
- K-Means Clustering (K = 5)
- Principal Component Analysis (PCA)

## Results

- Optimal number of clusters: **5**
- Successfully segmented customers into five groups.
- PCA visualization clearly separated the customer segments.

## Business Insights

- Premium customers should receive loyalty rewards.
- High-income, low-spending customers can be targeted with personalized promotions.
- Budget-conscious customers can be engaged through discounts.
- Customer segmentation improves personalized marketing and customer retention.

## Conclusion

K-Means clustering successfully identified meaningful customer groups. The segmentation can support better marketing decisions and improve business performance.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn