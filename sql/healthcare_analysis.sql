-- ─────────────────────────────────────────────────────────────
-- Healthcare Patient & Revenue Analysis
-- Database: MySQL  |  Author: [Your Name]  |  Year: 2023
-- ─────────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    Patient_ID          VARCHAR(10)   NOT NULL,
    Age                 INT           NOT NULL,
    Gender              VARCHAR(10)   NOT NULL,
    Blood_Type          VARCHAR(5)    NOT NULL,
    Medical_Condition   VARCHAR(50)   NOT NULL,
    Hospital            VARCHAR(100)  NOT NULL,
    Insurance_Provider  VARCHAR(50)   NOT NULL,
    Admission_Type      VARCHAR(20)   NOT NULL,
    Admission_Date      DATE          NOT NULL,
    Discharge_Date      DATE          NOT NULL,
    Stay_Days           INT           NOT NULL,
    Billing_Amount      DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (Patient_ID)
);

-- After creating the table, import data using:
-- Right-click patients table → Table Data Import Wizard → select healthcare_data.csv


-- ─────────────────────────────────────────────────────────────
-- 1. BASIC EXPLORATION
-- ─────────────────────────────────────────────────────────────

SELECT * FROM patients LIMIT 10;

SELECT COUNT(*) AS Total_Patients FROM patients;

SELECT COUNT(DISTINCT Hospital)          AS Total_Hospitals,
       COUNT(DISTINCT Medical_Condition) AS Total_Conditions
FROM patients;


-- ─────────────────────────────────────────────────────────────
-- 2. REVENUE OVERVIEW
-- ─────────────────────────────────────────────────────────────

-- Overall KPIs
SELECT
    COUNT(*)                          AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2)     AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2)     AS Avg_Billing,
    ROUND(AVG(Stay_Days), 2)          AS Avg_Stay_Days,
    MIN(Billing_Amount)               AS Min_Bill,
    MAX(Billing_Amount)               AS Max_Bill
FROM patients;


-- ─────────────────────────────────────────────────────────────
-- 3. REVENUE BY CATEGORY
-- ─────────────────────────────────────────────────────────────

-- By Medical Condition
SELECT
    Medical_Condition,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Medical_Condition
ORDER BY Total_Revenue DESC;


-- By Hospital
SELECT
    Hospital,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Hospital
ORDER BY Total_Revenue DESC;


-- By Gender
SELECT
    Gender,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Gender
ORDER BY Total_Revenue DESC;


-- By Insurance Provider
SELECT
    Insurance_Provider,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Insurance_Provider
ORDER BY Total_Revenue DESC;


-- By Admission Type
SELECT
    Admission_Type,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Admission_Type
ORDER BY Total_Revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 4. STAY DURATION ANALYSIS
-- ─────────────────────────────────────────────────────────────

-- Average stay by condition
SELECT
    Medical_Condition,
    ROUND(AVG(Stay_Days), 2) AS Avg_Stay_Days,
    MIN(Stay_Days)           AS Min_Stay,
    MAX(Stay_Days)           AS Max_Stay
FROM patients
GROUP BY Medical_Condition
ORDER BY Avg_Stay_Days DESC;


-- Average stay by hospital
SELECT
    Hospital,
    ROUND(AVG(Stay_Days), 2) AS Avg_Stay_Days
FROM patients
GROUP BY Hospital
ORDER BY Avg_Stay_Days DESC;


-- ─────────────────────────────────────────────────────────────
-- 5. AGE GROUP ANALYSIS
-- ─────────────────────────────────────────────────────────────

SELECT
    CASE
        WHEN Age BETWEEN 18 AND 30 THEN '18-30'
        WHEN Age BETWEEN 31 AND 45 THEN '31-45'
        WHEN Age BETWEEN 46 AND 60 THEN '46-60'
        WHEN Age BETWEEN 61 AND 75 THEN '61-75'
        ELSE '75+'
    END                           AS Age_Group,
    COUNT(*)                      AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Total_Revenue,
    ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Age_Group
ORDER BY Total_Revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 6. TIME-BASED ANALYSIS
-- ─────────────────────────────────────────────────────────────

-- Monthly revenue trend
SELECT
    MONTH(Admission_Date)             AS Month_Num,
    MONTHNAME(Admission_Date)         AS Month_Name,
    COUNT(*)                          AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2)     AS Monthly_Revenue
FROM patients
GROUP BY Month_Num, Month_Name
ORDER BY Month_Num;


-- Quarterly revenue
SELECT
    QUARTER(Admission_Date)           AS Quarter,
    COUNT(*)                          AS Total_Patients,
    ROUND(SUM(Billing_Amount), 2)     AS Quarterly_Revenue
FROM patients
GROUP BY Quarter
ORDER BY Quarter;


-- ─────────────────────────────────────────────────────────────
-- 7. FILTERS — WHERE AND HAVING
-- ─────────────────────────────────────────────────────────────

-- Patients with above-average billing
SELECT Patient_ID, Age, Gender, Medical_Condition, Hospital, Billing_Amount
FROM patients
WHERE Billing_Amount > (SELECT AVG(Billing_Amount) FROM patients)
ORDER BY Billing_Amount DESC
LIMIT 20;


-- Hospitals with more than 90 patients
SELECT Hospital, COUNT(*) AS Total_Patients
FROM patients
GROUP BY Hospital
HAVING COUNT(*) > 90
ORDER BY Total_Patients DESC;


-- Heart Disease patients above age 50
SELECT Patient_ID, Age, Gender, Hospital, Stay_Days, Billing_Amount
FROM patients
WHERE Medical_Condition = 'Heart Disease'
  AND Age > 50
ORDER BY Billing_Amount DESC;


-- Conditions where average billing exceeds $8,000
SELECT Medical_Condition, ROUND(AVG(Billing_Amount), 2) AS Avg_Billing
FROM patients
GROUP BY Medical_Condition
HAVING AVG(Billing_Amount) > 8000
ORDER BY Avg_Billing DESC;


-- Emergency admissions by condition
SELECT
    Medical_Condition,
    COUNT(*)                      AS Emergency_Patients,
    ROUND(SUM(Billing_Amount), 2) AS Emergency_Revenue
FROM patients
WHERE Admission_Type = 'Emergency'
GROUP BY Medical_Condition
ORDER BY Emergency_Revenue DESC;


-- ─────────────────────────────────────────────────────────────
-- 8. TOP & BOTTOM PATIENTS
-- ─────────────────────────────────────────────────────────────

-- Top 5 highest billing patients
SELECT Patient_ID, Age, Gender, Medical_Condition, Hospital, Billing_Amount
FROM patients
ORDER BY Billing_Amount DESC
LIMIT 5;


-- Bottom 5 lowest billing patients
SELECT Patient_ID, Age, Gender, Medical_Condition, Hospital, Billing_Amount
FROM patients
ORDER BY Billing_Amount ASC
LIMIT 5;
