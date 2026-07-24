SELECT
    p.ProductName,
    SUM(od.Quantity) AS Total_Quantity_Sold
FROM Products p
JOIN "Order Details" od
    ON p.ProductID = od.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;

------------------------------------------------------------
-- Question 2: Top 10 Customers by Revenue
------------------------------------------------------------
SELECT
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Total_Revenue
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.CompanyName
ORDER BY Total_Revenue DESC
LIMIT 10;

------------------------------------------------------------
-- Question 3: Monthly Sales Trends
------------------------------------------------------------

SELECT
    strftime('%Y-%m', o.OrderDate) AS Month,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Total_Sales
FROM Orders o
JOIN "Order Details" od
    ON o.OrderID = od.OrderID
GROUP BY Month
ORDER BY Month;

------------------------------------------------------------
-- Question 4: Best-Performing Product Categories
------------------------------------------------------------

SELECT
    c.CategoryName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS Total_Revenue
FROM Categories c
JOIN Products p
    ON c.CategoryID = p.CategoryID
JOIN "Order Details" od
    ON p.ProductID = od.ProductID
GROUP BY c.CategoryID, c.CategoryName
ORDER BY Total_Revenue DESC;

------------------------------------------------------------
-- Question 5: Customer Purchase Frequency
------------------------------------------------------------

SELECT
    c.CompanyName,
    COUNT(DISTINCT o.OrderID) AS Total_Orders
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CompanyName
ORDER BY Total_Orders DESC;