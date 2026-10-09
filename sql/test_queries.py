import sqlite3
from pathlib import Path


DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "bi_home_task.db"
)


def print_result(title, cursor):
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(" | ".join(columns))
    print("-" * 60)

    for row in rows:
        print(" | ".join(str(value) for value in row))


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# TASK 2.1
cursor.execute("""
    SELECT name
    FROM customers
    WHERE city = 'София';
""")

print_result(
    "TASK 2.1 - CUSTOMERS FROM SOFIA",
    cursor
)


# TASK 2.2
cursor.execute("""
    SELECT
        c.name,
        COUNT(o.id) AS completed_orders
    FROM customers c
    LEFT JOIN orders o
        ON c.id = o.customer_id
        AND o.status = 'completed'
    GROUP BY c.id, c.name
    ORDER BY c.id;
""")

print_result(
    "TASK 2.2 - COMPLETED ORDERS BY CUSTOMER",
    cursor
)


# TASK 2.2 BONUS
cursor.execute("""
    SELECT
        c.name,
        COUNT(DISTINCT o.id) AS completed_orders,
        COALESCE(
            ROUND(SUM(p.quantity * p.unit_price), 2),
            0
        ) AS revenue
    FROM customers c
    LEFT JOIN orders o
        ON c.id = o.customer_id
        AND o.status = 'completed'
    LEFT JOIN products p
        ON p.order_id = o.id
    GROUP BY c.id, c.name
    ORDER BY c.id;
""")

print_result(
    "TASK 2.2 BONUS - COMPLETED ORDERS & REVENUE",
    cursor
)


# TASK 2.3
cursor.execute("""
    SELECT
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM orders;
""")

print_result(
    "TASK 2.3 - UNIQUE CUSTOMERS",
    cursor
)


# TASK 2.3 - completed orders only
cursor.execute("""
    SELECT
        COUNT(DISTINCT customer_id)
        AS unique_completed_customers
    FROM orders
    WHERE status = 'completed';
""")

print_result(
    "TASK 2.3 - UNIQUE CUSTOMERS WITH COMPLETED ORDERS",
    cursor
)


connection.close()