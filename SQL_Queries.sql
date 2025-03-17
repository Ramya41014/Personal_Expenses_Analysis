SELECT COUNT(*) FROM all_expenses;  -- Check total records
SELECT * FROM all_expenses LIMIT 10;  -- View sample records

-- 1. Total amount spent in each category
SELECT Category, SUM(Amount_Paid) AS Total_Spent_TO_Category
FROM all_expenses
GROUP BY Category;

-- 2. Total amount spent using each payment mode
SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent_to_payment_mode
FROM all_expenses
GROUP BY Payment_Mode;

-- 3. Total cashback received across all transactions
SELECT SUM(Cashback) AS Total_Cashback
FROM all_expenses;


-- 4. Top 5 most expensive categories
SELECT Category, SUM(Amount_Paid) AS Total_Spent_to_category
FROM all_expenses
GROUP BY Category
ORDER BY Total_Spent_to_category DESC
LIMIT 5;

-- 5. Amount Spending on transportation using different payment modes
SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent_to_payment_modes
FROM all_expenses
WHERE Category = 'Transportation'
GROUP BY Payment_Mode;

-- 6. Transactions that resulted in cashback
SELECT *
FROM all_expenses
WHERE Cashback > 0;

-- 7. Total spending in each month of the year
SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_each_month
FROM all_expenses
GROUP BY MONTH(Date);

-- 8. Months with highest spending in specific categories
SELECT MONTH(Date) AS Month, Category, SUM(Amount_Paid) AS Total_Spent_to_specific_category
FROM all_expenses
WHERE Category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY MONTH(Date), Category
ORDER BY Total_Spent_to_specific_category DESC;

-- 9. Recurring expenses during specific months
SELECT Description, MONTH(Date) AS Month, COUNT(*) AS Occurrences
FROM all_expenses
GROUP BY Description, MONTH(Date)
HAVING COUNT(*) > 1
ORDER BY Month, Occurrences DESC;
    
-- 10. Cashback earned in each month
SELECT MONTH(Date) AS Month, SUM(Cashback) AS Total_Cashback
FROM all_expenses
GROUP BY MONTH(Date);

-- 11. Overall spending change over time
SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_change_over_time
FROM all_expenses
GROUP BY YEAR(Date), MONTH(Date)
ORDER BY Year, Month;

-- 12. Typical costs associated with different types of travel
SELECT Description, AVG(Amount_Paid) AS Average_Cost
FROM all_expenses
WHERE Category = 'Travel'
GROUP BY Description;

-- 13. Patterns in grocery spending

SELECT DAYOFWEEK(Date) AS Day_of_Week, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
WHERE Category = 'Groceries'
GROUP BY Day_of_Week
ORDER BY Day_of_Week;
-- 14. Define High and Low Priority Categories
SELECT 
    CASE 
        WHEN Category IN ( 'Bills', 'Groceries', 'Insurance' ) THEN 'High Priority'
        WHEN Category IN ('Entertainment', 'Travel', 'Subscriptions','Investment','Food') THEN 'Low Priority'
        ELSE 'Other'
    END AS Priority,
    SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
GROUP BY Priority
ORDER BY Priority;

-- 15. Category contributing the highest percentage of total spending
SELECT Category, 
       SUM(Amount_Paid) AS Total_Spent,
       (SUM(Amount_Paid) / (SELECT SUM(Amount_Paid) FROM all_expenses) * 100) AS Percentage_Of_Total
FROM all_expenses
GROUP BY Category
ORDER BY Total_Spent DESC
LIMIT 1;

-- 16 What is the total spending on travel for each month?

SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Travel
FROM all_expenses
WHERE Category = 'Travel'
GROUP BY MONTH(Date);

-- 17 WWhat is the average cashback received per category?
SELECT Category, AVG(Cashback) AS Average_Cashback
FROM all_expenses
GROUP BY Category;

-- 19 What is the total spending on bills for each month?
SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Bills
FROM all_expenses
WHERE Category = 'Bills'
GROUP BY MONTH(Date);

-- 19 Which payment mode is used most frequently?
SELECT Payment_Mode, COUNT(*) AS Frequency
FROM all_expenses
GROUP BY Payment_Mode
ORDER BY Frequency DESC
LIMIT 3;

-- 20 What is the highest single transaction amount?
SELECT 
    Category, 
    MAX(Amount_Paid) AS Highest_Transaction_Amount
FROM 
    all_expenses
GROUP BY 
    Category;

-- 21 How many unique descriptions of expenses are there?
SELECT COUNT(DISTINCT Description) AS Unique_Expense_Descriptions
FROM all_expenses;

-- 22 How many transactions were made in each category?


SELECT Category, COUNT(*) AS Transaction_Count
FROM all_expenses
GROUP BY Category;

-- 23 which category is mostly not spended?
SELECT Category, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
GROUP BY Category
ORDER BY Total_Spent 
LIMIT 1;

-- 24 How much was spent on essential vs. non-essential items?

SELECT 
    CASE 
        WHEN Category IN ('Groceries', 'Bills', 'Transportation','Subscriptions') THEN 'Essential'
        ELSE 'Non-Essential'
    END AS Spending_Type,
    SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
GROUP BY Spending_Type;

-- 25  Which food category (e.g., groceries, dining out) has the highest spending?

SELECT Description, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
WHERE Category = 'Food'
GROUP BY Description
ORDER BY Total_Spent DESC;

-- 26 How does spending on investments vary by month?

SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Investments
FROM all_expenses
WHERE Category = 'Investment'
GROUP BY MONTH(Date)
ORDER BY Month;

-- 28 Which personal category description has the highest spending?

SELECT Description, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
WHERE Category = 'Personal'
GROUP BY Description
ORDER BY Total_Spent DESC;

-- 29 Which gifts category description has the highest spending?

SELECT Description, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
WHERE Category = 'Gifts'
GROUP BY Description
ORDER BY Total_Spent DESC;

