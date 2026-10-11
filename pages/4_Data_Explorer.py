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
def load_table(table_name):
    allowed_tables = {
        "customers",
        "orders",
        "products",
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            connection,
        )


customers = load_table("customers")
orders = load_table("orders")
products = load_table("products")



def model_card(
    table_name,
    grain,
    rows,
    fields,
):
    field_html = ""

    for field_name, field_type in fields:
        field_html += (
            '<div style="'
            'display:flex;'
            'align-items:center;'
            'justify-content:space-between;'
            'gap:1rem;'
            'padding:0.55rem 0;'
            'border-bottom:1px solid #F1F5F9;'
            '">'
            '<span style="'
            'color:#334155;'
            'font-size:0.82rem;'
            'font-family:monospace;'
            '">'
            f'{field_name}'
            '</span>'
            '<span style="'
            'color:#64748B;'
            'font-size:0.62rem;'
            'font-weight:800;'
            'letter-spacing:0.06em;'
            '">'
            f'{field_type}'
            '</span>'
            '</div>'
        )

    card_html = (
        '<div style="'
        'background:#FFFFFF;'
        'border:1px solid #E2E8F0;'
        'border-radius:15px;'
        'overflow:hidden;'
        'box-shadow:0 1px 2px rgba(15,23,42,0.04);'
        'min-height:355px;'
        '">'
        '<div style="'
        'padding:1.15rem 1.2rem;'
        'background:linear-gradient(135deg,#0F172A,#1E293B);'
        '">'
        '<div style="'
        'color:#93C5FD;'
        'font-size:0.64rem;'
        'font-weight:800;'
        'letter-spacing:0.12em;'
        'text-transform:uppercase;'
        '">'
        'TABLE'
        '</div>'
        '<div style="'
        'color:#FFFFFF;'
        'font-size:1.2rem;'
        'font-weight:750;'
        'margin-top:0.25rem;'
        '">'
        f'{table_name}'
        '</div>'
        '<div style="'
        'color:#94A3B8;'
        'font-size:0.72rem;'
        'margin-top:0.25rem;'
        '">'
        f'{rows} rows · {grain}'
        '</div>'
        '</div>'
        '<div style="padding:0.75rem 1.2rem 1rem 1.2rem;">'
        f'{field_html}'
        '</div>'
        '</div>'
    )

    st.markdown(
        card_html,
        unsafe_allow_html=True,
    )


def relationship_arrow(
    left_label,
    right_label,
):
    arrow_html = (
        '<div style="'
        'display:flex;'
        'align-items:center;'
        'justify-content:center;'
        'min-height:355px;'
        '">'
        '<div style="text-align:center;width:100%;">'
        '<div style="'
        'color:#2563EB;'
        'font-size:0.65rem;'
        'font-weight:800;'
        'letter-spacing:0.08em;'
        'margin-bottom:0.45rem;'
        '">'
        f'{left_label} : {right_label}'
        '</div>'
        '<div style="'
        'display:flex;'
        'align-items:center;'
        'width:100%;'
        '">'
        '<div style="'
        'height:2px;'
        'background:#BFDBFE;'
        'flex:1;'
        '">'
        '</div>'
        '<div style="'
        'color:#3B82F6;'
        'font-size:1.35rem;'
        'line-height:1;'
        'padding-left:0.2rem;'
        '">'
        '›'
        '</div>'
        '</div>'
        '<div style="'
        'color:#64748B;'
        'font-size:0.68rem;'
        'margin-top:0.45rem;'
        '">'
        'one-to-many'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        arrow_html,
        unsafe_allow_html=True,
    )


def health_card(
    label,
    value,
    caption,
    passed=True,
):
    variant = "green" if passed else "red"

    kpi_card(
        label=label,
        value=value,
        caption=caption,
        variant=variant,
    )



duplicate_customers = int(
    customers["id"].duplicated().sum()
)

duplicate_orders = int(
    orders["id"].duplicated().sum()
)

duplicate_products = int(
    products["id"].duplicated().sum()
)


missing_customers = int(
    customers.isna().sum().sum()
)

missing_orders = int(
    orders.isna().sum().sum()
)

missing_products = int(
    products.isna().sum().sum()
)


valid_statuses = {
    "completed",
    "cancelled",
}

unexpected_statuses = (
    set(orders["status"].dropna().unique())
    - valid_statuses
)


orphan_orders = orders[
    ~orders["customer_id"].isin(
        customers["id"]
    )
]


orphan_products = products[
    ~products["order_id"].isin(
        orders["id"]
    )
]


total_duplicate_ids = (
    duplicate_customers
    + duplicate_orders
    + duplicate_products
)


total_missing_values = (
    missing_customers
    + missing_orders
    + missing_products
)


total_orphans = (
    len(orphan_orders)
    + len(orphan_products)
)


all_checks_passed = (
    total_duplicate_ids == 0
    and total_missing_values == 0
    and len(unexpected_statuses) == 0
    and total_orphans == 0
)



hero(
    label="Source Data · Validation",
    title="Data Explorer",
    subtitle=(
        "Inspect the source tables, understand their grain and "
        "relationships, and review the checks used to validate "
        "the sample dataset."
    ),
    show_scope=True,
)



section_header(
    label="Source Data",
    title="A transparent view of the analytical foundation.",
    description=(
        "The project uses the sample dataset supplied with the "
        "assignment and stores it locally in SQLite. No additional "
        "customers, orders or product rows have been added."
    ),
)


intro_col1, intro_col2 = st.columns(
    [1.2, 0.8]
)


with intro_col1:
    st.markdown(
        """
Before calculating metrics, I first look at the **grain of each
table**, the relationships between them and basic data-quality
conditions.

This is especially important here because joining order-level
data to product-level data can multiply rows and change the
meaning of a count.
        """
    )


with intro_col2:
    insight_card(
        title="Data Scope",
        value="Provided sample only",
        text=(
            "All tables on this page come from the assignment "
            "dataset. The explorer is intended to make the source "
            "and validation logic visible."
        ),
    )



section_header(
    label="Dataset Overview",
    title="Three tables, three different grains.",
    description=(
        "Row counts alone are simple, but the meaning of each row "
        "changes from table to table."
    ),
)


overview_col1, overview_col2, overview_col3 = st.columns(3)


with overview_col1:
    kpi_card(
        label="Customers",
        value=len(customers),
        caption="1 row per customer",
        variant="blue",
    )


with overview_col2:
    kpi_card(
        label="Orders",
        value=len(orders),
        caption="1 row per order",
        variant="navy",
    )


with overview_col3:
    kpi_card(
        label="Product Rows",
        value=len(products),
        caption="1 row per order item",
        variant="blue",
    )



section_header(
    label="Data Model",
    title="How the source tables connect.",
    description=(
        "A customer can place multiple orders, and an order can "
        "contain multiple product rows. Understanding these "
        "one-to-many relationships is essential before joining."
    ),
)


model_col1, arrow_col1, model_col2, arrow_col2, model_col3 = st.columns(
    [1.45, 0.45, 1.45, 0.45, 1.45]
)


with model_col1:
    model_card(
        table_name="customers",
        grain="customer grain",
        rows=len(customers),
        fields=[
            ("id", "PK"),
            ("name", "TEXT"),
            ("city", "TEXT"),
        ],
    )


with arrow_col1:
    relationship_arrow(
        "1",
        "N",
    )


with model_col2:
    model_card(
        table_name="orders",
        grain="order grain",
        rows=len(orders),
        fields=[
            ("id", "PK"),
            ("customer_id", "FK"),
            ("order_date", "DATE"),
            ("status", "TEXT"),
        ],
    )


with arrow_col2:
    relationship_arrow(
        "1",
        "N",
    )


with model_col3:
    model_card(
        table_name="products",
        grain="order-line grain",
        rows=len(products),
        fields=[
            ("id", "PK"),
            ("order_id", "FK"),
            ("product", "TEXT"),
            ("quantity", "INTEGER"),
            ("unit_price", "REAL"),
        ],
    )


st.write("")


insight_card(
    title="Why Grain Matters",
    value="Customer → Order → Order Line",
    text=(
        "Joining customers to orders can create multiple rows per "
        "customer. Joining orders to products can create multiple "
        "rows per order. Metrics such as unique customers and order "
        "counts must therefore be calculated at the intended grain."
    ),
)



section_header(
    label="Relationships",
    title="Primary and foreign keys define the path.",
)


relationship_col1, relationship_col2 = st.columns(2)


with relationship_col1:
    st.markdown(
        """
**customers → orders**

`customers.id` = `orders.customer_id`

- One customer can have many orders.
- Every order should reference an existing customer.
- Customer-level counts can be multiplied after this JOIN.
        """
    )


with relationship_col2:
    st.markdown(
        """
**orders → products**

`orders.id` = `products.order_id`

- One order can contain many product rows.
- Every product row should reference an existing order.
- Order counts can be multiplied after this JOIN.
        """
    )



section_header(
    label="Table Explorer",
    title="Inspect the source rows directly.",
    description=(
        "Select a table and optionally search across all of its "
        "columns. The displayed data comes directly from SQLite."
    ),
)


control_col1, control_col2 = st.columns(
    [0.7, 1.3]
)


with control_col1:
    selected_table = st.selectbox(
        "Source Table",
        options=[
            "customers",
            "orders",
            "products",
        ],
    )


with control_col2:
    search_value = st.text_input(
        "Search Table",
        placeholder=(
            "Search names, cities, IDs, statuses, products..."
        ),
    )


if selected_table == "customers":
    selected_df = customers.copy()

elif selected_table == "orders":
    selected_df = orders.copy()

else:
    selected_df = products.copy()


if search_value:
    mask = selected_df.astype(str).apply(
        lambda column: column.str.contains(
            search_value,
            case=False,
            na=False,
        )
    )

    selected_df = selected_df[
        mask.any(axis=1)
    ]


table_title_col, table_count_col = st.columns(
    [4, 1]
)


with table_title_col:
    st.markdown(
        f"#### {selected_table.capitalize()} Table"
    )


with table_count_col:
    st.caption(
        f"{len(selected_df)} row(s) shown"
    )


st.dataframe(
    selected_df,
    use_container_width=True,
    hide_index=True,
)



section_header(
    label="Quick Summary",
    title=f"{selected_table.capitalize()} table profile.",
)


if selected_table == "customers":

    unique_cities = int(
        customers["city"].nunique()
    )

    sofia_customers = int(
        (
            customers["city"] == "София"
        ).sum()
    )

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        kpi_card(
            label="Customers",
            value=len(customers),
            caption="Total customer rows",
            variant="blue",
        )

    with summary_col2:
        kpi_card(
            label="Cities",
            value=unique_cities,
            caption="Distinct cities",
            variant="navy",
        )

    with summary_col3:
        kpi_card(
            label="Sofia Customers",
            value=sofia_customers,
            caption="Customers from Sofia",
            variant="blue",
        )


    city_counts = (
        customers
        .groupby(
            "city",
            as_index=False,
        )
        .agg(
            customers=("id", "count")
        )
        .sort_values(
            [
                "customers",
                "city",
            ],
            ascending=[
                False,
                True,
            ],
        )
    )


    st.write("")

    st.dataframe(
        city_counts.rename(
            columns={
                "city": "City",
                "customers": "Customers",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


elif selected_table == "orders":

    completed = int(
        (
            orders["status"] == "completed"
        ).sum()
    )

    cancelled = int(
        (
            orders["status"] == "cancelled"
        ).sum()
    )

    unique_customers = int(
        orders["customer_id"].nunique()
    )

    completion_rate = (
        completed / len(orders) * 100
        if len(orders)
        else 0
    )


    summary_col1, summary_col2, summary_col3, summary_col4 = (
        st.columns(4)
    )


    with summary_col1:
        kpi_card(
            label="Orders",
            value=len(orders),
            caption="Total order rows",
            variant="blue",
        )


    with summary_col2:
        kpi_card(
            label="Completed",
            value=completed,
            caption=f"{completion_rate:.0f}% of orders",
            variant="green",
        )


    with summary_col3:
        kpi_card(
            label="Cancelled",
            value=cancelled,
            caption="Cancelled orders",
            variant="red",
        )


    with summary_col4:
        kpi_card(
            label="Customers",
            value=unique_customers,
            caption="Customers with orders",
            variant="navy",
        )


elif selected_table == "products":

    product_data = products.copy()

    product_data["line_value"] = (
        product_data["quantity"]
        * product_data["unit_price"]
    )


    total_quantity = int(
        product_data["quantity"].sum()
    )


    total_value = float(
        product_data["line_value"].sum()
    )


    unique_products = int(
        product_data["product"].nunique()
    )


    summary_col1, summary_col2, summary_col3, summary_col4 = (
        st.columns(4)
    )


    with summary_col1:
        kpi_card(
            label="Product Rows",
            value=len(product_data),
            caption="Order-line records",
            variant="blue",
        )


    with summary_col2:
        kpi_card(
            label="Units",
            value=total_quantity,
            caption="Total listed quantity",
            variant="navy",
        )


    with summary_col3:
        kpi_card(
            label="Products",
            value=unique_products,
            caption="Distinct product names",
            variant="blue",
        )


    with summary_col4:
        kpi_card(
            label="Listed Value",
            value=f"€{total_value:.2f}",
            caption="All product rows",
            variant="navy",
        )


    st.write("")

    st.warning(
        "The listed value includes product rows from both completed "
        "and cancelled orders. It is not completed revenue."
    )



section_header(
    label="Data Health",
    title="Automated checks before analysis.",
    description=(
        "These checks look for common issues that could change "
        "query results or make relationships unreliable."
    ),
)


health_col1, health_col2, health_col3, health_col4 = st.columns(4)


with health_col1:
    health_card(
        label="Duplicate IDs",
        value=total_duplicate_ids,
        caption="Across all primary keys",
        passed=(
            total_duplicate_ids == 0
        ),
    )


with health_col2:
    health_card(
        label="Missing Values",
        value=total_missing_values,
        caption="Across all source tables",
        passed=(
            total_missing_values == 0
        ),
    )


with health_col3:
    health_card(
        label="Unexpected Statuses",
        value=len(unexpected_statuses),
        caption="Outside expected values",
        passed=(
            len(unexpected_statuses) == 0
        ),
    )


with health_col4:
    health_card(
        label="Orphan Records",
        value=total_orphans,
        caption="Broken relationships",
        passed=(
            total_orphans == 0
        ),
    )


st.write("")


if all_checks_passed:
    status_pill(
        "ALL CHECKS PASSED",
        status="validated",
    )

    st.success(
        "No issues were found by the implemented data-quality "
        "and relationship checks."
    )

else:
    st.warning(
        "One or more implemented data checks require review."
    )



section_header(
    label="Validation Detail",
    title="What was checked.",
    description=(
        "The summary above is expanded below so each validation "
        "result remains visible and auditable."
    ),
)


quality_checks = pd.DataFrame(
    {
        "Validation Check": [
            "Duplicate customer IDs",
            "Duplicate order IDs",
            "Duplicate product-row IDs",
            "Missing customer values",
            "Missing order values",
            "Missing product values",
            "Unexpected order statuses",
            "Orders without matching customer",
            "Product rows without matching order",
        ],
        "Issues Found": [
            duplicate_customers,
            duplicate_orders,
            duplicate_products,
            missing_customers,
            missing_orders,
            missing_products,
            len(unexpected_statuses),
            len(orphan_orders),
            len(orphan_products),
        ],
    }
)


quality_checks["Status"] = quality_checks[
    "Issues Found"
].apply(
    lambda value: (
        "PASS"
        if value == 0
        else "REVIEW"
    )
)


st.dataframe(
    quality_checks,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Validation Check": st.column_config.TextColumn(
            "Validation Check",
            width="large",
        ),
        "Issues Found": st.column_config.NumberColumn(
            "Issues Found",
            format="%d",
        ),
        "Status": st.column_config.TextColumn(
            "Status",
        ),
    },
)



validation_col1, validation_col2 = st.columns(2)


with validation_col1:

    st.markdown("#### Primary Key Checks")

    st.markdown(
        f"""
- `customers.id`: **{duplicate_customers} duplicate IDs**
- `orders.id`: **{duplicate_orders} duplicate IDs**
- `products.id`: **{duplicate_products} duplicate IDs**
        """
    )


with validation_col2:

    st.markdown("#### Relationship Checks")

    st.markdown(
        f"""
- Orders without a customer: **{len(orphan_orders)}**
- Product rows without an order: **{len(orphan_products)}**
- Unexpected order statuses: **{len(unexpected_statuses)}**
        """
    )



section_header(
    label="Analytical Note",
    title="Clean data does not remove the need to understand grain.",
)


insight_card(
    title="Key Takeaway",
    value="Validate before aggregating",
    text=(
        "The implemented checks confirm that the sample has no "
        "duplicate primary keys, missing values, unexpected statuses "
        "or broken relationships. The remaining analytical risk is "
        "therefore mainly logical: choosing the correct grain and "
        "avoiding row multiplication when tables are joined."
    ),
)



footer()