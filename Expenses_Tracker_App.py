import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to the MySQL database
mydb = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        password='Ramya@123',
        database='tracking_expenses',
        auth_plugin='mysql_native_password'
 )
    

# Function to execute SQL queries
def execute_query(query):
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [i[0] for i in cursor.description]  # Get column names
    cursor.close()
    return pd.DataFrame(result, columns=columns)

# Main function to run the Streamlit app
def main():
    st.title(" Personal Expenses Tracker App")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Select an option", ["Home", "Insights", "Add Expense"])

    if options == "Home":
        st.write("Welcome to the Expense Tracker App!")
        st.write("This app helps you track your expenses, analyze spending patterns, and manage your finances effectively.")
        st.write("Use the sidebar to navigate through the app.")
     
    elif options == "Insights":
        st.subheader("Insights from Expense Data")

              # 1. Total Amount Spent in Each Category
        st.header("Total Amount Spent in Each Category")
        query = """
            SELECT Category, SUM(Amount_Paid) AS Total_Spent
            FROM all_expenses
            GROUP BY Category
            ORDER BY Total_Spent DESC;
            """
        total_spent_by_category = execute_query(query)
        st.write(total_spent_by_category)

        # Bar chart for total spending by category
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Total_Spent', y='Category', data=total_spent_by_category)
        plt.title('Total Amount Spent in Each Category')
        plt.xlabel('Total Spending')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 2. Total Amount Spent Using Each Payment Mode
        st.header("Total Amount Spent Using Each Payment Mode")
        query = """
            SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent
            FROM all_expenses
            GROUP BY Payment_Mode
            ORDER BY Total_Spent DESC;
        """
        total_spent_by_payment_mode = execute_query(query)
        st.write(total_spent_by_payment_mode)

        # Bar chart for total spending by payment mode
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Total_Spent', y='Payment_Mode', data=total_spent_by_payment_mode)
        plt.title('Total Amount Spent Using Each Payment Mode')
        plt.xlabel('Total Spending')
        plt.ylabel('Payment Mode')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 3. Total Cashback Received Across All Transactions
        st.header("Total Cashback Received Across All Transactions")
        query = """
            SELECT SUM(Cashback) AS Total_Cashback
            FROM all_expenses;
        """
        total_cashback = execute_query(query)
        st.write(total_cashback)

        # Bar chart for total cashback
        plt.figure(figsize=(6, 4))
        sns.barplot(x=['Total Cashback'], y=total_cashback['Total_Cashback'])
        plt.title('Total Cashback Received Across All Transactions')
        plt.xlabel('Cashback')
        plt.ylabel('Amount')
        plt.grid(axis='y')
        st.pyplot(plt)

        # 4. Top 5 Most Expensive Categories
        st.header("Top 5 Most Expensive Categories")
        query = """
            SELECT Category, SUM(Amount_Paid) AS Total_Spent
            FROM all_expenses
            GROUP BY Category
            ORDER BY Total_Spent DESC
            LIMIT 5;
        """
        top_5_expensive_categories = execute_query(query)
        st.write(top_5_expensive_categories)

        # Bar chart for top 5 most expensive categories
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Total_Spent', y='Category', data=top_5_expensive_categories)
        plt.title('Top 5 Most Expensive Categories in Terms of Spending')
        plt.xlabel('Total Spending')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 5. Transportation Spending by Payment Mode
        st.header("Transportation Spending by Payment Mode")
        query = """
        SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        WHERE Category = 'Transportation'
        GROUP BY Payment_Mode
        ORDER BY Total_Spent DESC;
        """
        transportation_spending = execute_query(query)
        st.write(transportation_spending)

        #   Bar chart for transportation spending by payment mode
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Total_Spent', y='Payment_Mode', data=transportation_spending)
        plt.title('Transportation Spending by Payment Mode')
        plt.xlabel('Total Spending')
        plt.ylabel('Payment Mode')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 6. Transactions that Resulted in Cashback
        st.header("Transactions that Resulted in Cashback")
        query = """
        SELECT *
        FROM all_expenses
        WHERE Cashback > 0;
        """
        cashback_transactions = execute_query(query)
        st.write(cashback_transactions)

        # Bar chart to visualize total cashback from these transactions
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Description', y='Cashback', data=cashback_transactions)
        plt.title('Cashback Received from Transactions')
        plt.xlabel('Transaction Description')
        plt.ylabel('Cashback Amount')
        plt.xticks(rotation=45, ha='right')  # Rotate x labels for better readability
        plt.grid(axis='y')
        st.pyplot(plt)

        # 7. Total Spending in Each Month of the Year
        st.header("Total Spending in Each Month of the Year")
        query = """
SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent
FROM all_expenses
GROUP BY MONTH(Date)
ORDER BY Month;
"""
        monthly_spending = execute_query(query)
        st.write(monthly_spending)

        # Line chart to visualize total spending by month
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Month', y='Total_Spent', data=monthly_spending, marker='o', color='blue')
        plt.title('Total Spending in Each Month of the Year')
        plt.xlabel('Month')
        plt.ylabel('Total Spending')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid()
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        st.pyplot(plt)

        # 8. Months with Highest Spending in Specific Categories
        st.header("Highest Spending Category for Each Month")
        query = """
        SELECT MONTH(Date) AS Month, Category, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        GROUP BY MONTH(Date), Category
        ORDER BY Month, Total_Spent DESC;
        """
        highest_spending = execute_query(query).loc[lambda df: df.groupby('Month')['Total_Spent'].idxmax()]
        st.write(highest_spending)

        # Bar chart to visualize the highest spending category for each month
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Month', y='Total_Spent', hue='Category', data=highest_spending)
        plt.title('Highest Spending Category for Each Month')
        plt.xlabel('Month')
        plt.ylabel('Total Spent')
        plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.legend(title='Category')
        plt.grid(axis='y')
        st.pyplot(plt)

        # 9. Recurring Expenses by Month
        st.header("Recurring Expenses by Month and Category")
        query = """
            SELECT MONTH(Date) AS Month, Category AS Expense_Type, SUM(Amount_Paid) AS Total_Expense
            FROM all_expenses
            WHERE Category IN ('Groceries', 'Bills', 'Subscriptions')
            GROUP BY MONTH(Date), Category
            ORDER BY Month, Category;
        """
        recurring_expenses = execute_query(query)
        st.write(recurring_expenses)

        # Create a pivot table for better visualization
        pivot_table = recurring_expenses.pivot(index='Month', columns='Expense_Type', values='Total_Expense').fillna(0)

        plt.figure(figsize=(12, 8))
        sns.barplot(x='Month', y='Total_Expense', hue='Expense_Type', data=recurring_expenses)
        plt.title('Recurring Expenses by Month and Category')
        plt.xlabel('Month')
        plt.ylabel('Total Expense')
        plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.legend(title='Expense Category')
        plt.grid(axis='y')
        st.pyplot(plt)

        # 10. Total Cashback Earned by Month
        st.header("Total Cashback Earned by Month")
        query = """
        SELECT MONTH(Date) AS Month, SUM(Cashback) AS Total_Cashback
        FROM all_expenses
        GROUP BY MONTH(Date);
        """
        cashback_data = execute_query(query)
        st.write(cashback_data)

        # Bar chart to visualize total cashback earned by month
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Month', y='Total_Cashback', data=cashback_data)
        plt.title('Total Cashback Earned by Month')
        plt.xlabel('Month')
        plt.ylabel('Total Cashback')
        plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid(axis='y')
        st.pyplot(plt)

        # 11. Total Spending by Month
        st.header("Total Spending by Month")
        query = """
        SELECT DATE_FORMAT(Date, '%Y-%m') AS Month, SUM(Amount_Paid) AS Total_Spending
        FROM all_expenses
        GROUP BY Month
        ORDER BY Month;
        """
        spending_data = execute_query(query)
        st.write(spending_data)

        # Line chart to visualize overall spending over time
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Month', y='Total_Spending', data=spending_data, marker='o')
        plt.title('Overall Spending Over Time')
        plt.xlabel('Month')
        plt.ylabel('Total Spending')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        st.pyplot(plt)

        # 12. Average Costs Associated with Different Travel Descriptions
        st.header("Average Costs Associated with Different Travel Descriptions")
        query = """
        SELECT Description, AVG(Amount_Paid) AS Average_Cost
        FROM all_expenses
        WHERE Category = 'Travel'
        GROUP BY Description;
        """
        average_travel_costs = execute_query(query)
        st.write(average_travel_costs)

        # Bar chart to visualize average costs associated with different travel descriptions
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Average_Cost', y='Description', data=average_travel_costs)
        plt.title('Average Costs Associated with Different Travel Descriptions')
        plt.xlabel('Average Cost')
        plt.ylabel('Travel Description')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 13. Grocery Spending by Day of the Week
        st.header("Grocery Spending by Day of the Week")
        query = """
        SELECT DAYOFWEEK(Date) AS Day_of_Week, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        WHERE Category = 'Groceries'
        GROUP BY Day_of_Week
        ORDER BY Day_of_Week;
        """
        grocery_spending_analysis = execute_query(query)
        st.write(grocery_spending_analysis)

        # Bar chart to visualize grocery spending by day of the week
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Day_of_Week', y='Total_Spent', data=grocery_spending_analysis)
        plt.title('Grocery Spending by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Total Spent')
        plt.xticks(ticks=range(7), labels=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
        plt.grid(axis='y')
        st.pyplot(plt)

        # 14. Total Spending by Priority Category
        st.header("Total Spending by Priority Category")
        query = """
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
        """
        priority_expenses = execute_query(query)
        st.write(priority_expenses)

        # Bar chart to visualize spending by priority category
        plt.figure(figsize=(8, 6))
        sns.barplot(x='Priority', y='Total_Spent', data=priority_expenses)
        plt.title('Total Spending by Priority Category')
        plt.xlabel('Priority Category')
        plt.ylabel('Total Spent')
        plt.grid(axis='y')
        st.pyplot(plt)

        # 15. Total Spending by Category
        st.header("Total Spending by Category")
        query = """
        SELECT Category, 
            SUM(Amount_Paid) AS Total_Spent,
            (SUM(Amount_Paid) / (SELECT SUM(Amount_Paid) FROM all_expenses) * 100) AS Percentage_Of_Total
        FROM all_expenses
        GROUP BY Category
        ORDER BY Total_Spent DESC
        """
        category_spending = execute_query(query)

        # Calculate the total spending
        total_spending = category_spending['Total_Spent'].sum()

        # Calculate the percentage contribution of each category
        category_spending['Percentage'] = (category_spending['Total_Spent'] / total_spending) * 100

        # Find the category with the highest percentage contribution
        highest_contribution = category_spending.loc[category_spending['Percentage'].idxmax()]

        st.write(category_spending)
        st.write(f"Category with the highest contribution: {highest_contribution['Category']} - {highest_contribution['Percentage']:.2f}%")

        # Bar chart to visualize spending by category
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Total_Spent', y='Category', data=category_spending)
        plt.title('Total Spending by Category')
        plt.xlabel('Total Spent')
        plt.ylabel('Category')
        plt.axvline(x=highest_contribution['Total_Spent'], color='red', linestyle='--', label='Highest Contribution')
        plt.legend()
        plt.grid(axis='y')
        st.pyplot(plt)

        # 16. Total Spending on Travel for Each Month
        st.header("Total Spending on Travel per Month")
        query = """
        SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Travel
        FROM all_expenses
        WHERE Category = 'Travel'
        GROUP BY MONTH(Date)
        ORDER BY Month;
        """
        total_spent_on_travel = execute_query(query)
        st.write(total_spent_on_travel)

        # Bar chart to visualize the total spending on travel per month
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Month', y='Total_Spent_On_Travel', data=total_spent_on_travel)
        plt.title('Total Spending on Travel per Month')
        plt.xlabel('Month')
        plt.ylabel('Total Spending on Travel')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid(axis='y')
        st.pyplot(plt)

        # 17. Average Cashback Received per Category
        st.header("Average Cashback Received per Category")
        query = """
        SELECT Category, AVG(Cashback) AS Average_Cashback
        FROM all_expenses
        GROUP BY Category;
        """
        average_cashback_per_category = execute_query(query)
        st.write(average_cashback_per_category)

        # Horizontal bar chart to visualize the average cashback per category
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Average_Cashback', y='Category', data=average_cashback_per_category)
        plt.title('Average Cashback Received per Category')
        plt.xlabel('Average Cashback')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 18. Total Spending on Bills for Each Month
        st.header("Total Spending on Bills per Month")
        query = """
        SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Bills
        FROM all_expenses
        WHERE Category = 'Bills'
        GROUP BY MONTH(Date)
        ORDER BY Month;
        """
        total_spent_on_bills = execute_query(query)
        st.write(total_spent_on_bills)

        # Line chart to visualize the total spending on bills per month
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Month', y='Total_Spent_On_Bills', data=total_spent_on_bills, marker='o', color='orange')
        plt.title('Total Spending on Bills per Month')
        plt.xlabel('Month')
        plt.ylabel('Total Spending on Bills')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid()
        st.pyplot(plt)

        # 19. Most Frequently Used Payment Modes
        st.header("Most Frequently Used Payment Modes")
        query = """
        SELECT Payment_Mode, COUNT(*) AS Frequency
        FROM all_expenses
        GROUP BY Payment_Mode
        ORDER BY Frequency DESC
        LIMIT 3;
        """
        most_frequent_payment_modes = execute_query(query)
        st.write(most_frequent_payment_modes)

        # Horizontal bar chart to visualize the most frequently used payment modes
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Frequency', y='Payment_Mode', data=most_frequent_payment_modes)
        plt.title('Most Frequently Used Payment Modes')
        plt.xlabel('Frequency')
        plt.ylabel('Payment Mode')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 20. Highest Single Transaction Amount by Category
        st.header("Highest Single Transaction Amount by Category")
        query = """
        SELECT Category, MAX(Amount_Paid) AS Highest_Transaction_Amount
        FROM all_expenses
        GROUP BY Category;
        """
        highest_transaction_per_category = execute_query(query)
        st.write(highest_transaction_per_category)

        # Bar chart visualization for highest single transaction amount by category
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Highest_Transaction_Amount', y='Category', data=highest_transaction_per_category)
        plt.title('Highest Single Transaction Amount by Category')
        plt.xlabel('Highest Transaction Amount')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)


        # 21. Count Unique Descriptions of Expenses
        st.header("Unique Descriptions of Expenses")
        query = """
        SELECT COUNT(DISTINCT Description) AS Unique_Descriptions
        FROM all_expenses;
        """
        unique_descriptions = execute_query(query)
        num_unique_descriptions = unique_descriptions['Unique_Descriptions'][0]

        # Create a card-style visualization
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, f'Unique Descriptions of Expenses:\n{num_unique_descriptions}', 
                fontsize=20, ha='center', va='center', bbox=dict(facecolor='lightblue', alpha=0.5, boxstyle='round,pad=1'))
        plt.axis('off')  # Turn off the axis
        plt.title('Unique Expense Descriptions', fontsize=16)
        st.pyplot(plt)

        # 22. Count the Number of Transactions in Each Category
        st.header("Number of Transactions in Each Category")
        query = """
        SELECT Category, COUNT(*) AS Transaction_Count
        FROM all_expenses
        GROUP BY Category
        ORDER BY Transaction_Count DESC;
        """
        transaction_counts = execute_query(query)
        st.write(transaction_counts)

        # Bar chart to visualize the number of transactions in each category
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Transaction_Count', hue='Category', y='Category', data=transaction_counts, palette='viridis')
        plt.title('Number of Transactions in Each Category')
        plt.xlabel('Transaction Count')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 23. Category with the Least Spending
        st.header("Category with the Least Spending")
        query = """
        SELECT Category, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        GROUP BY Category
        ORDER BY Total_Spent 
        LIMIT 1;
        """
        least_spent_category = execute_query(query)
        st.write(least_spent_category)

        # Bar chart to visualize the least spent category
        plt.figure(figsize=(8, 5))
        sns.barplot(x='Total_Spent', y='Category', data=least_spent_category)
        plt.title('Category with the Least Spending')
        plt.xlabel('Total Spending')
        plt.ylabel('Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 24. Compare Spending on Essential vs. Non-Essential Items
        st.header("Total Spending on Essential vs. Non-Essential Items")
        query = """
        SELECT 
            CASE 
                WHEN Category IN ('Groceries', 'Bills', 'Transportation', 'Subscriptions') THEN 'Essential'
                ELSE 'Non-Essential'
            END AS Spending_Type,
            SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        GROUP BY Spending_Type;
        """
        essential_vs_non_essential = execute_query(query)
        st.write(essential_vs_non_essential)

        # Pie chart to visualize spending types
        plt.figure(figsize=(8, 8))
        plt.pie(essential_vs_non_essential['Total_Spent'], 
                labels=essential_vs_non_essential['Spending_Type'], 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=['#66c2a5', '#fc8d62'])
        plt.title('Total Spending on Essential vs. Non-Essential Items')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(plt)

        # 25. Food Category with the Highest Spending
        st.header("Food Categories and Their Spending")
        query = """
        SELECT Description, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        WHERE Category = 'Food'
        GROUP BY Description
        ORDER BY Total_Spent DESC;
        """
        food_spending = execute_query(query)
        st.write(food_spending)

        # Horizontal bar chart to visualize the highest spending food category
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Total_Spent', y='Description', data=food_spending)
        plt.title('Food Categories and Their Spending')
        plt.xlabel('Total Spending')
        plt.ylabel('Food Category')
        plt.grid(axis='x')
        st.pyplot(plt)

        # 26. Analyze Spending on Investments by Month
        st.header("Monthly Spending on Investments")
        query = """
        SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent_On_Investments
        FROM all_expenses
        WHERE Category = 'Investment'
        GROUP BY MONTH(Date)
        ORDER BY Month;
        """
        investment_spending = execute_query(query)
        st.write(investment_spending)

        # Line chart to visualize spending on investments by month
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Month', y='Total_Spent_On_Investments', data=investment_spending, marker='o', color='blue')
        plt.title('Monthly Spending on Investments')
        plt.xlabel('Month')
        plt.ylabel('Total Spending on Investments')
        plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid()
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        st.pyplot(plt)

        # 28. Gifts Category Description with the Highest Spending
        st.header("Gifts Categories and Their Spending")
        query = """
        SELECT Description, SUM(Amount_Paid) AS Total_Spent
        FROM all_expenses
        WHERE Category = 'Gifts'
        GROUP BY Description
        ORDER BY Total_Spent DESC;
        """
        gifts_spending = execute_query(query)
        st.write(gifts_spending)

        # Horizontal bar chart to visualize the spending for each gifts category
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Total_Spent', y='Description', data=gifts_spending)
        plt.title('Gifts Categories and Their Spending')
        plt.xlabel('Total Spending')
        plt.ylabel('Gifts Category Description')
        plt.grid(axis='x')
        st.pyplot(plt)

    elif options == "Add Expense":
        st.subheader("Add a New Expense")
        with st.form(key='expense_form'):
            description = st.text_input("Expense Description")
            amount = st.number_input("Amount (€)", min_value=0.0, step=0.01)
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Credit Card", "Debit Card", "Online"])
            submit_button = st.form_submit_button("Add Expense")

        if submit_button:
            try:
                cursor = mydb.cursor()
                cursor.execute(
                    "INSERT INTO all_expenses (Description, Amount_Paid, Category, Payment_Mode) VALUES (%s, %s, %s, %s)",
                    (description, amount, category, payment_mode)
                )
                mydb.commit()
                st.success(f"Added: {description} for {amount} € in {category} using {payment_mode}.")
            except Error as e:
                st.error(f"Error adding expense: {e}")
            finally:
                cursor.close()
     
if __name__ == "__main__":
    main()
