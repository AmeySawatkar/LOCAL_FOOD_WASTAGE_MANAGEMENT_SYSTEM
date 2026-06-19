CREATE DATABASE food_wastage_management;
USE food_wastage_management;
CREATE TABLE providers (
    Provider_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Address VARCHAR(255),
    City VARCHAR(100),
    Contact VARCHAR(50)
);
CREATE TABLE receivers (
    Receiver_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    City VARCHAR(100),
    Contact VARCHAR(50)
);
CREATE TABLE food_listings (
    Food_ID INT PRIMARY KEY,
    Food_Name VARCHAR(255),
    Quantity INT,
    Expiry_Date DATE,
    Provider_ID INT,
    Provider_Type VARCHAR(100),
    Location VARCHAR(100),
    Food_Type VARCHAR(100),
    Meal_Type VARCHAR(100),
    FOREIGN KEY (Provider_ID)
    REFERENCES providers(Provider_ID)
);
CREATE TABLE claims (
    Claim_ID INT PRIMARY KEY,
    Food_ID INT,
    Receiver_ID INT,
    Status VARCHAR(50),
    Timestamp DATETIME,
    FOREIGN KEY (Food_ID)
    REFERENCES food_listings(Food_ID),
    FOREIGN KEY (Receiver_ID)
    REFERENCES receivers(Receiver_ID)
);-- =====================================================
-- LOCAL FOOD WASTAGE MANAGEMENT SYSTEM
-- SQL ANALYSIS QUERIES
-- Internship Project
-- =====================================================

-- =====================================================
-- QUERY 1
-- Number of Food Providers in Each City
-- =====================================================

SELECT City,
       COUNT(*) AS Total_Providers
FROM providers
GROUP BY City
ORDER BY Total_Providers DESC;

-- =====================================================
-- QUERY 2
-- Number of Food Receivers in Each City
-- =====================================================

SELECT City,
       COUNT(*) AS Total_Receivers
FROM receivers
GROUP BY City
ORDER BY Total_Receivers DESC;

-- =====================================================
-- QUERY 3
-- Provider Type Contributing the Most Food
-- =====================================================

SELECT Provider_Type,
       SUM(Quantity) AS Total_Food_Quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Food_Quantity DESC;

-- =====================================================
-- QUERY 4
-- Contact Information of Food Providers in a Specific City
-- =====================================================

SELECT Name,
       Type,
       Contact,
       City
FROM providers
WHERE City = 'Mumbai';

-- =====================================================
-- QUERY 5
-- Receivers Who Claimed the Most Food
-- =====================================================

SELECT r.Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM claims c
JOIN receivers r
ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name
ORDER BY Total_Claims DESC;

-- =====================================================
-- QUERY 6
-- Total Quantity of Food Available from All Providers
-- =====================================================

SELECT SUM(Quantity) AS Total_Food_Available
FROM food_listings;

-- =====================================================
-- QUERY 7
-- City with the Highest Number of Food Listings
-- =====================================================

SELECT Location,
       COUNT(*) AS Total_Listings
FROM food_listings
GROUP BY Location
ORDER BY Total_Listings DESC;

-- =====================================================
-- QUERY 8
-- Most Commonly Available Food Types
-- =====================================================

SELECT Food_Type,
       COUNT(*) AS Total_Items
FROM food_listings
GROUP BY Food_Type
ORDER BY Total_Items DESC;

-- =====================================================
-- QUERY 9
-- Number of Claims Made for Each Food Item
-- =====================================================

SELECT f.Food_Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings f
LEFT JOIN claims c
ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY Total_Claims DESC;

-- =====================================================
-- QUERY 10
-- Provider with the Highest Number of Successful Claims
-- =====================================================

SELECT p.Name,
       COUNT(c.Claim_ID) AS Successful_Claims
FROM providers p
JOIN food_listings f
ON p.Provider_ID = f.Provider_ID
JOIN claims c
ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY Successful_Claims DESC;

-- =====================================================
-- QUERY 11
-- Percentage Distribution of Claim Status
-- =====================================================

SELECT Status,
       ROUND(
           COUNT(*) * 100.0 /
           (SELECT COUNT(*) FROM claims),
           2
       ) AS Percentage
FROM claims
GROUP BY Status;

-- =====================================================
-- QUERY 12
-- Average Quantity of Food Claimed per Receiver
-- =====================================================

SELECT r.Name,
       ROUND(AVG(f.Quantity),2) AS Avg_Quantity_Claimed
FROM claims c
JOIN receivers r
ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings f
ON c.Food_ID = f.Food_ID
GROUP BY r.Name
ORDER BY Avg_Quantity_Claimed DESC;

-- =====================================================
-- QUERY 13
-- Most Claimed Meal Type
-- =====================================================

SELECT f.Meal_Type,
       COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings f
JOIN claims c
ON f.Food_ID = c.Food_ID
GROUP BY f.Meal_Type
ORDER BY Total_Claims DESC;

-- =====================================================
-- QUERY 14
-- Total Quantity of Food Donated by Each Provider
-- =====================================================

SELECT p.Name,
       SUM(f.Quantity) AS Total_Donated
FROM providers p
JOIN food_listings f
ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;

-- =====================================================
-- QUERY 15
-- Food Items Expiring Within the Next 7 Days
-- =====================================================

SELECT Food_Name,
       Quantity,
       Expiry_Date,
       Location
FROM food_listings
WHERE Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY Expiry_Date;

-- =====================================================
-- END OF SQL ANALYSIS QUERIES
-- =====================================================
