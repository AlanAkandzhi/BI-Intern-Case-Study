# BI Intern Case Study

An end-to-end Business Intelligence case study covering business analysis, SQL, data validation and interactive reporting.

Built by **Alan Akandzhi** as part of a BI Intern home assignment.

> **Live Demo:** Coming soon

---

## Overview

The project starts with a short business request and follows the analytical process from clarification to final reporting.

The goal is not only to calculate the requested numbers, but also to:

- clarify business definitions before analysis;
- choose meaningful KPIs;
- understand the data model and table grain;
- write and explain the required SQL queries;
- validate results against the supplied data;
- communicate assumptions and limitations clearly;
- provide an interactive view of the sample dataset.

The application is built with **Python, SQL, SQLite, Pandas, Streamlit and Plotly**.

---

## Case Study Structure

### Task 1 - Business Analysis

The first part considers how to approach a request for the number of orders in the previous month and compare the result with the month before.

The analysis covers:

- questions to clarify with the stakeholder;
- the definition of an order;
- treatment of cancelled orders;
- reporting-period assumptions;
- month-over-month comparison;
- cancellation rate;
- unique customers and repeat ordering;
- interpretation of the free-delivery campaign.

Because no actual monthly dataset is provided for Task 1, the project describes the analytical approach without inventing a month-over-month result.

### Task 2 - SQL Analysis

The second part uses the supplied sample tables to answer the SQL questions.

It includes:

- customers from Sofia;
- completed orders for every customer;
- completed revenue as a bonus metric;
- explanation of why counting rows after a one-to-many join can produce an incorrect customer count;
- the correct distinct-customer calculation.

The SQL queries are executed against the local SQLite database and their outputs are validated against the supplied sample.

---

## Verified Sample Results

| Metric | Result |
|---|---:|
| Total Orders | 5 |
| Completed Orders | 3 |
| Cancelled Orders | 2 |
| Unique Customers | 3 |
| Completion Rate | 60% |
| Cancellation Rate | 40% |
| Completed Revenue | €12.50 |

Customers from Sofia:

- Ана
- Вяра
- Дария

Completed orders by customer:

| Customer | Completed Orders | Completed Revenue |
|---|---:|---:|
| Ана | 1 | €5.00 |
| Борис | 1 | €6.00 |
| Вяра | 1 | €1.50 |
| Георги | 0 | €0.00 |
| Дария | 0 | €0.00 |

---

## Interactive Dashboard

The Streamlit dashboard provides an interactive view of the supplied sample data.

It includes:

- filtering by customer city;
- filtering by order status;
- dynamic KPIs;
- completion and cancellation rates;
- order-status distribution;
- orders by customer;
- completed revenue by customer;
- order activity over time;
- city-level summary;
- dynamic analytical insights;
- CSV export of the current filtered view;
- CSV export of the current KPI summary.

All dashboard calculations use an order-level analytical dataset so that product-line rows do not inflate order counts.

---

## Data Model

The supplied data is represented by three tables:

```text
customers
    |
    | 1:N
    v
orders
    |
    | 1:N
    v
products
```

### Grain

- `customers`: one row per customer
- `orders`: one row per order
- `products`: one row per order line

The product-line data is aggregated to order grain before it is joined into the dashboard analytical dataset.

This prevents orders with multiple products from being counted multiple times.

---

## SQL Example

A key issue in the assignment is the difference between counting joined rows and counting distinct customers.

A join between customers, orders and order lines can return multiple rows for a single order because one order may contain multiple products.

For the supplied definition of a customer who has placed an order, the direct calculation is:

```sql
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
```

Result:

```text
3
```

The project also documents the alternative definition of customers with completed orders separately.

---

## Assumptions

The main analytical assumptions are documented explicitly in the application.

Key examples include:

- completed orders are used as the primary fulfilled-order metric;
- cancelled orders are reported separately;
- completed revenue includes only completed orders;
- a unique customer is identified by `customer_id`;
- Task 1 uses the last full calendar month compared with the immediately preceding full calendar month;
- campaign effects should not be interpreted causally without additional evidence.

The assignment refers to the order-line table as both `products` and `order_items`. The project uses `products`, matching the supplied sample table, while documenting this naming discrepancy.

---

## Data Validation

The project checks:

- duplicate primary keys;
- missing values;
- unexpected order statuses;
- orders without matching customers;
- product rows without matching orders;
- aggregate order counts;
- completed and cancelled order counts;
- unique-customer count;
- completed revenue.

The supplied sample passes the implemented validation checks.

---

## Project Structure

```text
BI-Intern-Home-Task/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── __init__.py
│   ├── style.css
│   └── ui.py
│
├── database/
│   ├── bi_home_task.db
│   └── setup_database.py
│
├── pages/
│   ├── 0_Overview.py
│   ├── 1_Business_Analysis.py
│   ├── 2_SQL_Solutions.py
│   ├── 3_Dashboard.py
│   ├── 4_Data_Explorer.py
│   └── 5_Project_Notes.py
│
└── sql/
    ├── solutions.sql
    └── test_queries.py
```

---

## Run Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd BI-Intern-Home-Task
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Rebuild the sample database if needed

```bash
python database/setup_database.py
```

### 5. Run the SQL validation

```bash
python sql/test_queries.py
```

### 6. Start the Streamlit application

```bash
streamlit run app.py
```

---

## Technology

- Python
- SQL
- SQLite
- Pandas
- Streamlit
- Plotly

---

## Scope

The application uses only the sample data supplied with the home assignment.

The dataset is sufficient to demonstrate SQL logic, data modeling, validation and reporting, but it is too small to support broader conclusions about real business performance.

Task 1 is therefore kept conceptual where actual monthly data is not available, while Task 2 and the interactive dashboard use the supplied sample dataset.

---

## Author

**Alan Akandzhi**

BI Intern Candidate