import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from assets.ui import (
    footer,
    hero,
    insight_card,
    kpi_card,
    section_header,
    status_pill,
)



ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "database" / "bi_home_task.db"



@st.cache_data
def run_query(query):
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(
            query,
            connection,
        )


def show_query_result(query):
    result = run_query(query)

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
    )

    return result



def notebook_header(
    task,
    title,
    description,
    badge_text="VALIDATED",
):
    st.write("")

    header_col1, header_col2 = st.columns(
        [5, 1]
    )

    with header_col1:
        st.markdown(
            f'<div class="section-label">{task}</div>',
            unsafe_allow_html=True,
        )

    with header_col2:
        status_pill(
            badge_text,
            status="validated",
        )

    st.markdown(
        f"## {title}"
    )

    st.markdown(
        (
            '<div class="section-description">'
            f'{description}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def notebook_label(text):
    st.markdown(
        (
            '<div style="'
            'color: #64748B;'
            'font-size: 0.68rem;'
            'font-weight: 800;'
            'letter-spacing: 0.1em;'
            'text-transform: uppercase;'
            'margin-top: 1.25rem;'
            'margin-bottom: 0.5rem;'
            '">'
            f'{text}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )



hero(
    label="Task 2 · SQL Analysis",
    title="SQL Solutions",
    subtitle=(
        "Queries executed directly against the project database, "
        "with live results, reasoning and validation against the "
        "provided sample data."
    ),
    show_scope=True,
)



section_header(
    label="SQL Notebook",
    title="Query, inspect, explain, validate.",
    description=(
        "Each solution follows the same workflow: understand the "
        "business question, choose the appropriate data grain, "
        "execute the SQL and verify the result."
    ),
)


intro_col1, intro_col2 = st.columns(
    [1.2, 0.8]
)


with intro_col1:
    st.markdown(
        """
The results on this page are **not manually entered**.
Each query is executed against the SQLite database used by
the project and the returned data is displayed directly below
the SQL.

This makes the page both a solution to the assignment and a
small executable SQL notebook.
        """
    )


with intro_col2:
    insight_card(
        title="Schema Note",
        value="products = order lines",
        text=(
            "The assignment names the third table products, while "
            "the colleague query refers to order_items. I treat both "
            "references as the supplied order-line table and use "
            "the provided name products."
        ),
    )


# ============================================================
# TASK 2.1
# ============================================================

notebook_header(
    task="Task 2.1",
    title="Customers from Sofia",
    description=(
        "Return the names of all customers whose city is Sofia."
    ),
)


query_1 = """
SELECT name
FROM customers
WHERE city = 'София';
"""


notebook_label("Business Question")

st.markdown(
    "**Show the names of all customers from Sofia.**"
)


query_col, reasoning_col = st.columns(
    [1.05, 0.95]
)


with query_col:

    notebook_label("SQL Query")

    st.code(
        query_1.strip(),
        language="sql",
    )


with reasoning_col:

    notebook_label("Why This Works")

    st.markdown(
        """
The requested information is available entirely in the
`customers` table, so a JOIN would add unnecessary complexity.

The query filters on `city` and returns only `name`, which
directly matches the requested output.
        """
    )


notebook_label("Live Result")

result_1 = show_query_result(query_1)


expected_sofia_customers = [
    "Ана",
    "Вяра",
    "Дария",
]

validation_1 = (
    result_1["name"].tolist()
    == expected_sofia_customers
)


if validation_1:
    st.success(
        f"Validation passed: {len(result_1)} customers from Sofia "
        "were returned as expected."
    )
else:
    st.error(
        "Validation failed: the returned Sofia customers do not "
        "match the expected sample-data result."
    )


# ============================================================
# TASK 2.2
# ============================================================

notebook_header(
    task="Task 2.2",
    title="Completed Orders by Customer",
    description=(
        "Count completed orders for every customer, including "
        "customers who have zero completed orders."
    ),
)


query_2 = """
SELECT
    c.name,
    COUNT(o.id) AS completed_orders
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
    AND o.status = 'completed'
GROUP BY c.id, c.name
ORDER BY c.id;
"""


notebook_label("Business Question")

st.markdown(
    """
**For every customer, show the number of completed orders.**

All customers should remain in the output, even when their
completed-order count is zero.
    """
)


query_col, reasoning_col = st.columns(
    [1.05, 0.95]
)


with query_col:

    notebook_label("SQL Query")

    st.code(
        query_2.strip(),
        language="sql",
    )


with reasoning_col:

    notebook_label("Key SQL Decisions")

    st.markdown(
        """
**1. `LEFT JOIN`**

The task asks for every customer, so customers without a
completed order must remain in the result.

**2. Status filter inside `ON`**

`o.status = 'completed'` belongs in the JOIN condition.
Moving it to `WHERE` would remove customers without a
completed order.

**3. `COUNT(o.id)` instead of `COUNT(*)`**

For unmatched customers, `o.id` is `NULL`.
`COUNT(o.id)` therefore correctly returns **0**.
        """
    )


notebook_label("Live Result")

result_2 = show_query_result(query_2)


expected_completed = {
    "Ана": 1,
    "Борис": 1,
    "Вяра": 1,
    "Георги": 0,
    "Дария": 0,
}


actual_completed = dict(
    zip(
        result_2["name"],
        result_2["completed_orders"],
    )
)


validation_2 = (
    actual_completed
    == expected_completed
)


if validation_2:
    st.success(
        "Validation passed: completed-order counts match the "
        "provided sample data."
    )
else:
    st.error(
        "Validation failed: completed-order counts do not match "
        "the expected sample-data result."
    )


# ============================================================
# TASK 2.2 BONUS
# ============================================================

notebook_header(
    task="Task 2.2 · Bonus",
    title="Completed Revenue by Customer",
    description=(
        "Extend the completed-order analysis by calculating the "
        "revenue generated by each customer's completed orders."
    ),
)


query_bonus = """
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
"""


notebook_label("Business Question")

st.markdown(
    """
**Calculate the completed-order revenue for every customer.**

Customers without completed orders should remain in the result
with zero completed orders and zero revenue.
    """
)


query_col, reasoning_col = st.columns(
    [1.05, 0.95]
)


with query_col:

    notebook_label("SQL Query")

    st.code(
        query_bonus.strip(),
        language="sql",
    )


with reasoning_col:

    notebook_label("Why Grain Matters")

    st.markdown(
        """
Revenue is calculated at **product-row grain**:

`quantity × unit_price`

One order may contain multiple product rows. Once `orders`
is joined to `products`, the same order can therefore appear
multiple times.

That is why the query uses `COUNT(DISTINCT o.id)` for the
order count.

`COALESCE` converts missing revenue to **0** for customers
without completed orders.
        """
    )


notebook_label("Live Result")

result_bonus = show_query_result(
    query_bonus
)


total_revenue = float(
    result_bonus["revenue"].sum()
)


customers_with_revenue = int(
    (
        result_bonus["revenue"] > 0
    ).sum()
)


bonus_kpi1, bonus_kpi2, bonus_space = st.columns(
    [1, 1, 2]
)


with bonus_kpi1:
    kpi_card(
        label="Completed Revenue",
        value=f"€{total_revenue:.2f}",
        caption="Across all completed orders",
        variant="blue",
    )


with bonus_kpi2:
    kpi_card(
        label="Customers with Revenue",
        value=customers_with_revenue,
        caption="Sample dataset",
        variant="green",
    )


validation_bonus = (
    round(
        total_revenue,
        2,
    )
    == 12.50
)


if validation_bonus:
    st.success(
        "Validation passed: total completed revenue is €12.50."
    )
else:
    st.error(
        "Validation failed: expected total completed revenue "
        "is €12.50."
    )


# ============================================================
# TASK 2.3
# ============================================================

notebook_header(
    task="Task 2.3",
    title="Different Customers Who Placed an Order",
    description=(
        "Review a colleague's query, explain why its result is "
        "misleading and provide a query that answers the actual "
        "business question."
    ),
)


notebook_label("Business Question")

st.markdown(
    '**"How many different customers have placed an order?"**'
)


colleague_query = """
SELECT COUNT(*)
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id;
"""


notebook_label("Colleague Query")

st.code(
    colleague_query.strip(),
    language="sql",
)


st.error(
    "Incorrect interpretation: the returned value 5 is the number "
    "of joined rows, not the number of different customers."
)



section_header(
    label="Join Cardinality",
    title="Why 5 is not the answer.",
    description=(
        "The JOIN changes the grain of the result. COUNT(*) then "
        "counts those joined rows rather than unique customers."
    ),
)


join_demo_query = """
SELECT
    c.id AS customer_id,
    c.name,
    o.id AS order_id,
    p.product
FROM customers c
JOIN orders o
    ON o.customer_id = c.id
JOIN products p
    ON p.order_id = o.id
ORDER BY o.id, p.id;
"""


notebook_label("Joined Data")

join_demo = show_query_result(
    join_demo_query
)


joined_rows = len(
    join_demo
)


joined_unique_customers = (
    join_demo["customer_id"].nunique()
)


comparison_col1, comparison_col2 = st.columns(2)


with comparison_col1:
    kpi_card(
        label="Joined Rows",
        value=joined_rows,
        caption="What COUNT(*) sees",
        variant="red",
    )


with comparison_col2:
    kpi_card(
        label="Unique Customers",
        value=joined_unique_customers,
        caption="What the question asks for",
        variant="green",
    )


st.write("")


insight_card(
    title="The Grain Problem",
    value=(
        f"{joined_rows} rows ≠ "
        f"{joined_unique_customers} customers"
    ),
    text=(
        "Order 101 contains two product rows. After joining orders "
        "to the order-line table, that order appears twice. "
        "COUNT(*) counts both rows, even though they belong to "
        "the same order and customer."
    ),
)



section_header(
    label="Correct Approach",
    title="Count the entity the question actually asks for.",
    description=(
        "The orders table already contains customer_id, so no JOIN "
        "is required to count customers who placed an order."
    ),
)


query_3 = """
SELECT
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
"""


correct_col1, correct_col2 = st.columns(
    [1.05, 0.95]
)


with correct_col1:

    notebook_label("Correct SQL")

    st.code(
        query_3.strip(),
        language="sql",
    )


with correct_col2:

    notebook_label("Why This Is Better")

    st.markdown(
        """
The business question asks for **different customers**.

The `orders` table already stores `customer_id`, so the
simplest and clearest solution is:

`COUNT(DISTINCT customer_id)`

No additional JOIN is needed, and product-level rows cannot
multiply the count.
        """
    )


notebook_label("Live Result")

result_3 = show_query_result(
    query_3
)


unique_customers = int(
    result_3.loc[
        0,
        "unique_customers",
    ]
)


validation_3 = (
    unique_customers == 3
)


if validation_3:
    st.success(
        "Validation passed: 3 different customers placed at "
        "least one order."
    )
else:
    st.error(
        "Validation failed: expected 3 different customers "
        "with at least one order."
    )



section_header(
    label="Definition Check",
    title="Placed an order is not the same as completed an order.",
    description=(
        "The distinction does not change the numerical result in "
        "this tiny sample, but it changes the business definition."
    ),
)


completed_customer_query = """
SELECT
    COUNT(DISTINCT customer_id)
        AS unique_completed_customers
FROM orders
WHERE status = 'completed';
"""


alternative_col1, alternative_col2 = st.columns(
    [1.05, 0.95]
)


with alternative_col1:

    notebook_label("Alternative SQL")

    st.code(
        completed_customer_query.strip(),
        language="sql",
    )


with alternative_col2:

    notebook_label("Business Meaning")

    st.markdown(
        """
This version answers a different question:

**"How many different customers have completed an order?"**

A customer with only cancelled orders would be counted by
the original definition, but excluded from this one.
        """
    )


notebook_label("Live Result")

completed_customer_result = show_query_result(
    completed_customer_query
)


completed_unique = int(
    completed_customer_result.loc[
        0,
        "unique_completed_customers",
    ]
)


st.info(
    f"In this particular sample the result is also "
    f"{completed_unique}, but the two metrics remain "
    f"conceptually different."
)



section_header(
    label="Validation Summary",
    title="All SQL outputs reconciled with the sample data.",
    description=(
        "The checks below summarize the expected outputs used to "
        "verify the SQL logic."
    ),
)


check_1 = validation_1
check_2 = validation_2
check_3 = validation_bonus
check_4 = validation_3


validation_col1, validation_col2, validation_col3, validation_col4 = (
    st.columns(4)
)


with validation_col1:
    kpi_card(
        label="Sofia Customers",
        value=(
            "PASS"
            if check_1
            else "FAIL"
        ),
        caption="Expected: 3",
        variant=(
            "green"
            if check_1
            else "red"
        ),
    )


with validation_col2:
    kpi_card(
        label="Completed Counts",
        value=(
            "PASS"
            if check_2
            else "FAIL"
        ),
        caption="All 5 customers checked",
        variant=(
            "green"
            if check_2
            else "red"
        ),
    )


with validation_col3:
    kpi_card(
        label="Revenue",
        value=(
            "PASS"
            if check_3
            else "FAIL"
        ),
        caption="Expected: €12.50",
        variant=(
            "green"
            if check_3
            else "red"
        ),
    )


with validation_col4:
    kpi_card(
        label="Unique Customers",
        value=(
            "PASS"
            if check_4
            else "FAIL"
        ),
        caption="Expected: 3",
        variant=(
            "green"
            if check_4
            else "red"
        ),
    )



section_header(
    label="SQL Takeaways",
    title="The important part is not only writing valid SQL.",
    description=(
        "Correct analysis depends on matching the query logic to "
        "the business definition and understanding the grain of "
        "the underlying tables."
    ),
)


takeaway_col1, takeaway_col2 = st.columns(2)


with takeaway_col1:
    st.markdown(
        """
**Query design**

- Use the simplest table that can answer the question.
- Use `LEFT JOIN` when zero-match entities must remain.
- Place filters carefully when using `LEFT JOIN`.
- Count the entity requested by the business question.
        """
    )


with takeaway_col2:
    st.markdown(
        """
**Data validation**

- Understand table grain before joining.
- Expect one-to-many JOINs to multiply rows.
- Use `DISTINCT` when uniqueness is part of the metric.
- Reconcile query outputs with the source sample.
        """
    )



footer()