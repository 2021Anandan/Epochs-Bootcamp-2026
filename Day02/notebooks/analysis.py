#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import sqlite3

# Connect to the Northwind database
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "northwind.db"

conn = sqlite3.connect(DB_PATH)
print("✅ Connected successfully!")


# In[ ]:


import pandas as pd
import sqlite3

# Connect to the Northwind database
conn = sqlite3.connect("../database/northwind.db")
print("✅ Connected successfully!")

# Load Products table into a DataFrame
products = pd.read_sql_query(
    "SELECT * FROM Products",
    conn
)

# Display first 5 rows
products.head()


# # Northwind Sales Analysis
# 
# ## Business Analysis using SQL and Pandas
# 
# **Dataset:** Northwind Database
# 
# **Author:** Anandan M A
# 
# ---
# 
# ### Objectives
# 
# - Analyze Top Selling Products
# - Find Top Customers by Revenue
# - Analyze Monthly Sales Trends
# - Find Best Performing Product Categories
# - Analyze Customer Purchase Frequency

# In[ ]:


# Explore the Products table

print("Shape:", products.shape)

print("\nColumns:")
print(products.columns.tolist())

print("\nData Types:")
print(products.dtypes)

print("\nMissing Values:")
print(products.isnull().sum())


# In[ ]:


# Product statistics

print("Total Products:", len(products))

print("\nAverage Product Price:")
print(products["UnitPrice"].mean())

print("\nMost Expensive Product:")
print(products.loc[products["UnitPrice"].idxmax()])

print("\nLeast Expensive Product:")
print(products.loc[products["UnitPrice"].idxmin()])


# In[ ]:


import matplotlib.pyplot as plt

# Top 10 most expensive products
top10 = products.nlargest(10, "UnitPrice")

plt.figure(figsize=(10,5))
plt.bar(top10["ProductName"], top10["UnitPrice"])
plt.title("Top 10 Most Expensive Products")
plt.xlabel("Product Name")
plt.ylabel("Unit Price")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.tight_layout()
plt.savefig("../images/top10_most_expensive_products.png",
            dpi=300,
            bbox_inches="tight")
plt.show()



# In[ ]:


import sys
print(sys.executable)


# In[ ]:


# Top 10 Best Selling Products

top_selling = (
    products.sort_values("UnitsInStock", ascending=False)
            [["ProductName", "UnitsInStock"]]
            .head(10)
)

print(top_selling)


# In[ ]:


import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.bar(top_selling["ProductName"], top_selling["UnitsInStock"])

plt.title("Top 10 Products by Units in Stock")
plt.xlabel("Product Name")
plt.ylabel("Units In Stock")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.tight_layout()

plt.savefig(
    "images/<image_name>.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show(block=False)
plt.pause(2)
plt.close()


# In[ ]:


query = """
SELECT
    strftime('%Y-%m', o.OrderDate) AS Month,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS TotalSales
FROM Orders o
JOIN "Order Details" od
ON o.OrderID = od.OrderID
GROUP BY Month
ORDER BY Month;
"""

monthly_sales = pd.read_sql_query(query, conn)

monthly_sales.head()


# In[ ]:


plt.figure(figsize=(14,6))

plt.plot(
    monthly_sales["Month"],
    monthly_sales["TotalSales"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=90)

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()


# In[ ]:


query = """
SELECT
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY c.CompanyName
ORDER BY Revenue DESC
LIMIT 10;
"""

top_customers = pd.read_sql_query(query, conn)

top_customers


# In[ ]:


import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.bar(top_customers["CompanyName"], top_customers["Revenue"])

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Customer")
plt.ylabel("Revenue")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.show()


# In[ ]:


# Sales by Category

query = """
SELECT
    c.CategoryName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Categories c
JOIN Products p
    ON c.CategoryID = p.CategoryID
JOIN "Order Details" od
    ON p.ProductID = od.ProductID
GROUP BY c.CategoryName
ORDER BY Revenue DESC;
"""

category_sales = pd.read_sql_query(query, conn)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,8))

plt.pie(
    category_sales["Revenue"],
    labels=category_sales["CategoryName"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sales by Category")

plt.show()


# In[ ]:


# Revenue by Country

query = """
SELECT
    c.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Revenue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY c.Country
ORDER BY Revenue DESC;
"""

# Load SQL result into a DataFrame
country_sales = pd.read_sql_query(query, conn)

# Replace missing country names
country_sales["Country"] = country_sales["Country"].fillna("Unknown")

# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.bar(country_sales["Country"], country_sales["Revenue"])

plt.title("Revenue by Country")
plt.xlabel("Country")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()


# In[ ]:


# Revenue by Country

query = """
SELECT
    c.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Revenue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY c.Country
ORDER BY Revenue DESC;
"""

# Load SQL result into a DataFrame
country_sales = pd.read_sql_query(query, conn)

# Replace missing country names
country_sales["Country"] = country_sales["Country"].fillna("Unknown")

# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.bar(country_sales["Country"], country_sales["Revenue"])

plt.title("Revenue by Country")
plt.xlabel("Country")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()


# In[ ]:


import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 2, figsize=(18,12))

# -------------------------------
# Top Customers
# -------------------------------
ax[0,0].bar(
    top_customers["CompanyName"],
    top_customers["Revenue"]
)
ax[0,0].set_title("Top Customers")
ax[0,0].tick_params(axis="x", rotation=45)

# -------------------------------
# Sales by Category
# -------------------------------
ax[0,1].pie(
    category_sales["Revenue"],
    labels=category_sales["CategoryName"],
    autopct="%1.1f%%",
    startangle=90
)
ax[0,1].set_title("Sales by Category")

# -------------------------------
# Revenue by Country
# -------------------------------
ax[1,0].bar(
    country_sales["Country"],
    country_sales["Revenue"]
)
ax[1,0].set_title("Revenue by Country")
ax[1,0].tick_params(axis="x", rotation=45)

# -------------------------------
# Revenue by Product Category
# -------------------------------
ax[1,1].barh(
    category_revenue["CategoryName"],
    category_revenue["Revenue"]
)
ax[1,1].set_title("Revenue by Product Category")

plt.tight_layout()

plt.show()


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# Top Customers
# ---------------------------------
query = """
SELECT
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY c.CompanyName
ORDER BY Revenue DESC
LIMIT 10;
"""
top_customers = pd.read_sql_query(query, conn)

# ---------------------------------
# Sales by Category
# ---------------------------------
query = """
SELECT
    c.CategoryName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Categories c
JOIN Products p
    ON c.CategoryID = p.CategoryID
JOIN "Order Details" od
    ON p.ProductID = od.ProductID
GROUP BY c.CategoryName
ORDER BY Revenue DESC;
"""
category_sales = pd.read_sql_query(query, conn)

# ---------------------------------
# Revenue by Country
# ---------------------------------
query = """
SELECT
    cu.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Customers cu
JOIN Orders o
    ON cu.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY cu.Country
ORDER BY Revenue DESC;
"""
country_sales = pd.read_sql_query(query, conn)

country_sales["Country"] = country_sales["Country"].fillna("Unknown")

# ---------------------------------
# Revenue by Product Category
# ---------------------------------
query = """
SELECT
    c.CategoryName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)),2) AS Revenue
FROM Categories c
JOIN Products p
    ON c.CategoryID = p.CategoryID
JOIN "Order Details" od
    ON p.ProductID = od.ProductID
GROUP BY c.CategoryName
ORDER BY Revenue DESC;
"""
category_revenue = pd.read_sql_query(query, conn)

# =================================
# VISUALIZATIONS
# =================================

fig, ax = plt.subplots(2, 2, figsize=(18,12))

# Top Customers
ax[0,0].bar(
    top_customers["CompanyName"],
    top_customers["Revenue"],
    color="steelblue"
)
ax[0,0].set_title("Top Customers")
ax[0,0].tick_params(axis="x", rotation=45)

# Sales by Category
ax[0,1].pie(
    category_sales["Revenue"],
    labels=category_sales["CategoryName"],
    autopct="%1.1f%%",
    startangle=90
)
ax[0,1].set_title("Sales by Category")

# Revenue by Country
ax[1,0].bar(
    country_sales["Country"],
    country_sales["Revenue"],
    color="green"
)
ax[1,0].set_title("Revenue by Country")
ax[1,0].tick_params(axis="x", rotation=45)

# Revenue by Product Category
ax[1,1].barh(
    category_revenue["CategoryName"],
    category_revenue["Revenue"],
    color="orange"
)
ax[1,1].set_title("Revenue by Product Category")
plt.tight_layout()

plt.savefig(
    "../images/top10_most_expensive_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.plt.tight_layout()

plt.tight_layout()

plt.savefig(
    "../images/top10_most_expensive_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.shplt.tight_layout()

plt.savefig("../images/top10_most_expensive_products.png",
            dpi=300,
            bbox_inches="tight")

plt.show()oplt.tight_layout()

plt.savefig("../images/top10_most_expensive_products.png",
            dpi=300,
            bbox_inches="tight")

plt.tight_layout()

plt.savefig("../images/top10_best_selling_products.png",
            dpi=300,
            bbox_inches="tight")

plt.show()