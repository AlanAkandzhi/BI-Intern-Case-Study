import sqlite3
from pathlib import Path


# Database path
DB_PATH = Path(__file__).parent / "bi_home_task.db"


def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Start from a clean database every time the setup script is executed
    cursor.executescript("""
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );
    """)

    # Sample data from the assignment
    customers = [
        (1, "Ана", "София"),
        (2, "Борис", "Пловдив"),
        (3, "Вяра", "София"),
        (4, "Георги", "Варна"),
        (5, "Дария", "София"),
    ]

    orders = [
        (101, 1, "2026-03-01", "completed"),
        (102, 1, "2026-03-05", "cancelled"),
        (103, 2, "2026-03-07", "completed"),
        (104, 3, "2026-03-20", "completed"),
        (105, 3, "2026-04-02", "cancelled"),
    ]

    products = [
        (1, 101, "Хляб", 2, 1.50),
        (2, 101, "Мляко", 1, 2.00),
        (3, 102, "Кафе", 1, 8.00),
        (4, 103, "Мляко", 3, 2.00),
        (5, 104, "Хляб", 1, 1.50),
    ]

    cursor.executemany(
        "INSERT INTO customers (id, name, city) VALUES (?, ?, ?)",
        customers,
    )

    cursor.executemany(
        """
        INSERT INTO orders (id, customer_id, order_date, status)
        VALUES (?, ?, ?, ?)
        """,
        orders,
    )

    cursor.executemany(
        """
        INSERT INTO products
        (id, order_id, product, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
        """,
        products,
    )

    connection.commit()

    print("=" * 50)
    print("BI INTERN HOME TASK - DATABASE CHECK")
    print("=" * 50)

    checks = {
        "Customers": """
            SELECT COUNT(*)
            FROM customers
        """,
        "Orders": """
            SELECT COUNT(*)
            FROM orders
        """,
        "Completed Orders": """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'completed'
        """,
        "Cancelled Orders": """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'cancelled'
        """,
        "Unique Customers": """
            SELECT COUNT(DISTINCT customer_id)
            FROM orders
        """,
        "Completed Revenue": """
            SELECT ROUND(SUM(p.quantity * p.unit_price), 2)
            FROM orders o
            JOIN products p
                ON p.order_id = o.id
            WHERE o.status = 'completed'
        """,
    }

    for name, query in checks.items():
        cursor.execute(query)
        result = cursor.fetchone()[0]

        if name == "Completed Revenue":
            print(f"{name:<22}: EUR {result:.2f}")
        else:
            print(f"{name:<22}: {result}")

    print("=" * 50)
    print(f"Database created: {DB_PATH}")

    connection.close()


if __name__ == "__main__":
    create_database()