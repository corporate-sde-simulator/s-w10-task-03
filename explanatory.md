# Beginner Explanatory Guide: DATA-201: Fix Broken Sales Reporting Queries

> **Task Type**: Bug Fix  
> **Domain/Focus**: SQL Queries and Database Reporting

---

## 1. The Goal (In-Depth Beginner Explanation)

### The Core Problem
The quarterly sales dashboard is crucial for the Finance Team as it provides insights into the company's revenue performance across different regions. However, the dashboard is currently displaying incorrect figures due to bugs in three SQL queries within the reporting module. These bugs stem from improper JOIN operations, missing WHERE clauses, and errors in the GROUP BY statements. 

For instance, the revenue calculation might include cancelled orders, leading to inflated revenue figures. Additionally, the customer report may include customers who have not placed any orders, which is misleading. These inaccuracies can result in poor business decisions, as stakeholders rely on this data to assess performance and strategize future actions. Therefore, fixing these queries is essential to ensure that the dashboard reflects accurate and reliable data.

### Jargon Buster (Key Terms Explained)
* **SQL (Structured Query Language)**: SQL is a programming language designed for managing and manipulating relational databases. It allows users to perform tasks such as querying data, updating records, and managing database structures. For example, a simple SQL query to retrieve all customers might look like this: `SELECT * FROM customers;`.

* **JOIN**: A JOIN operation in SQL is used to combine rows from two or more tables based on a related column between them. For instance, if you want to get a list of customers along with their orders, you would use a JOIN to connect the `customers` table with the `orders` table on the `customer_id` field.

* **WHERE Clause**: This clause is used to filter records that meet a certain condition. For example, if you want to find all completed orders, you would use a WHERE clause like this: `SELECT * FROM orders WHERE status = 'completed';`.

* **GROUP BY**: This SQL statement is used to arrange identical data into groups. It is often used with aggregate functions like SUM or COUNT. For example, to calculate total sales per region, you would use: `SELECT region, SUM(amount) FROM orders GROUP BY region;`.

### Expected Outcome
After implementing the necessary fixes, the system should accurately reflect the sales data in the quarterly dashboard. 

**Before vs. After Comparison**:
- **Before**: The revenue query might incorrectly include cancelled orders, leading to inflated totals. The customer report could show customers without any orders, and the monthly breakdown might not group data correctly by month.
- **After**: The revenue query will only sum amounts from completed orders, the customer report will only include customers who have placed orders, and the monthly breakdown will correctly group sales data by month.

---

## 2. Related Coding Concepts & Syntax (50% Theory, 50% Practice)

### Concept 1: SQL Queries
#### 📘 Theoretical Overview (50%)
SQL queries are the backbone of data retrieval and manipulation in relational databases. They allow users to interact with the database to perform various operations such as selecting, inserting, updating, and deleting data. Without SQL, it would be challenging to extract meaningful insights from large datasets. 

The core mechanics of SQL involve understanding how to structure queries correctly, including the use of SELECT statements to retrieve data, WHERE clauses to filter results, and JOINs to combine data from multiple tables. If these elements are not used correctly, it can lead to inaccurate results, as seen in the current task.

#### 💻 Syntax & Practical Examples (50%)
* **Language Syntax**:
  ```sql
  SELECT column1, column2
  FROM table_name
  WHERE condition
  GROUP BY column
  ORDER BY column;
  ```
  - `SELECT`: Specifies the columns to retrieve.
  - `FROM`: Indicates the table from which to retrieve data.
  - `WHERE`: Filters records based on specified conditions.
  - `GROUP BY`: Groups rows sharing a property so aggregate functions can be applied.
  - `ORDER BY`: Sorts the result set based on one or more columns.

* **Real-World Application**:
  ```sql
  SELECT c.region, SUM(o.amount) AS total_revenue
  FROM customers c
  INNER JOIN orders o ON c.id = o.customer_id
  WHERE o.status = 'completed'
  GROUP BY c.region;
  ```
  This query retrieves the total revenue per region, ensuring only completed orders are counted.

---

## 3. Step-by-Step Logic & Walkthrough

1. **Step 1: Locate and Analyze the Target File**
   * Navigate to the `salesReporter.py` file within the `s-w10-task-03` folder.
   * Focus on the `revenue_by_region` method, specifically lines where SQL queries are executed.

2. **Step 2: Input Verification & Validation**
   * Check if the current implementation correctly filters out cancelled orders. Ensure that the SQL query uses the correct JOIN type and WHERE clause.

3. **Step 3: Core Implementation / Modification**
   * Modify the SQL query in the `revenue_by_region` method to use an INNER JOIN instead of a LEFT JOIN. This ensures that only customers with completed orders are included in the revenue calculation.
   * Add a WHERE clause to filter out orders that are not completed.

4. **Step 4: Output Verification & Testing**
   * Run the test suite using pytest to ensure all tests pass. This will confirm that the changes made to the SQL queries yield the expected results.

---

## 4. Detailed Walkthrough of Test Cases

### Test Case 1: Standard / Success Case
* **Description**: This test checks if the revenue calculation correctly excludes cancelled orders.
* **Inputs**:
  ```json
  {
    "orders": [
      {"id": 101, "customer_id": 1, "amount": 150.00, "status": "completed"},
      {"id": 102, "customer_id": 1, "amount": 200.00, "status": "completed"},
      {"id": 103, "customer_id": 2, "amount": 75.00, "status": "completed"},
      {"id": 105, "customer_id": 2, "amount": 50.00, "status": "cancelled"}
    ]
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `revenue_by_region` method is called.
  2. The SQL query executes, filtering out the cancelled order (id: 105).
  3. The total revenue for the South region is calculated as 75.00.
  4. Returns the final result.

* **Expected Output**: 
  ```json
  {
    "region": "South",
    "total_revenue": 75.00
  }
  ```

### Test Case 2: Edge Case / Validation Fail
* **Description**: This test checks the scenario where there are no completed orders for a region.
* **Inputs**:
  ```json
  {
    "orders": [
      {"id": 104, "customer_id": 3, "amount": 300.00, "status": "cancelled"}
    ]
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `revenue_by_region` method is called.
  2. The SQL query executes, but since there are no completed orders, the result set is empty.
  3. The method returns an empty list or a revenue of 0 for the North region.
  
* **Expected Output**: 
  ```json
  {
    "region": "North",
    "total_revenue": 0.00
  }
  ``` 

This guide provides a comprehensive understanding of the task at hand, ensuring that even beginners can grasp the concepts and steps necessary to fix the broken sales reporting queries.