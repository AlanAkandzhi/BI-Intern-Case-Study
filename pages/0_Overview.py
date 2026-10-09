import sqlite3
from pathlib import Path

import streamlit as st

from assets.ui import (
    footer,
    hero,
    insight_card,
    kpi_card,
    methodology_step,
    navigation_card,
    section_header,
    summary_card,
)


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "database" / "bi_home_task.db"


# ------------------------------------------------------------
# Load project metrics
# ------------------------------------------------------------

@st.cache_data
def load_project_metrics():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            """
        )
        total_orders = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'completed'
            """
        )
        completed_orders = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'cancelled'
            """
        )
        cancelled_orders = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(DISTINCT customer_id)
            FROM orders
            """
        )
        unique_customers = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(p.quantity * p.unit_price),
                0
            )
            FROM orders o
            JOIN products p
                ON p.order_id = o.id
            WHERE o.status = 'completed'
            """
        )
        revenue = cursor.fetchone()[0]

    completion_rate = (
        completed_orders / total_orders * 100
        if total_orders
        else 0
    )

    cancellation_rate = (
        cancelled_orders / total_orders * 100
        if total_orders
        else 0
    )

    return {
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "unique_customers": unique_customers,
        "revenue": revenue,
        "completion_rate": completion_rate,
        "cancellation_rate": cancellation_rate,
    }


metrics = load_project_metrics()


# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------

hero(
    label="BI Intern Case Study",
    title=(
        "From a business question<br>"
        "to a validated BI analysis."
    ),
    subtitle=(
        "A small end-to-end Business Intelligence case study "
        "combining business reasoning, SQL, data validation "
        "and interactive visualization."
    ),
    name="Alan Akandzhi",
    role="BI Intern Candidate",
    show_scope=True,
)


# ------------------------------------------------------------
# Hero actions
# ------------------------------------------------------------

action_col1, action_col2, action_space = st.columns(
    [1.15, 1.15, 5.7]
)

with action_col1:
    st.page_link(
        "pages/3_Dashboard.py",
        label="Explore Dashboard",
        icon=":material/dashboard:",
        use_container_width=True,
    )

with action_col2:
    st.page_link(
        "pages/2_SQL_Solutions.py",
        label="View SQL Solutions",
        icon=":material/database:",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Project introduction
# ------------------------------------------------------------

section_header(
    label="Project Overview",
    title="A business question is only the starting point.",
    description=(
        "The goal of this project is not only to return the requested "
        "numbers. It is to clarify the business definitions, understand "
        "the data model, write correct SQL, validate the results and "
        "communicate the findings clearly."
    ),
)


# ------------------------------------------------------------
# KPI overview
# ------------------------------------------------------------

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    kpi_card(
        label="Total Orders",
        value=metrics["total_orders"],
        caption="Orders in the sample",
        variant="blue",
    )

with kpi_col2:
    kpi_card(
        label="Completed",
        value=metrics["completed_orders"],
        caption=f'{metrics["completion_rate"]:.0f}% completion rate',
        variant="green",
    )

with kpi_col3:
    kpi_card(
        label="Cancelled",
        value=metrics["cancelled_orders"],
        caption=f'{metrics["cancellation_rate"]:.0f}% cancellation rate',
        variant="red",
    )

with kpi_col4:
    kpi_card(
        label="Unique Customers",
        value=metrics["unique_customers"],
        caption="Customers who placed an order",
        variant="navy",
    )

with kpi_col5:
    kpi_card(
        label="Completed Revenue",
        value=f'€{metrics["revenue"]:.2f}',
        caption="Completed orders only",
        variant="blue",
    )


# ------------------------------------------------------------
# Key observation
# ------------------------------------------------------------

st.write("")

insight_card(
    title="Sample Data Snapshot",
    value=f'{metrics["completion_rate"]:.0f}% completed',
    text=(
        f'{metrics["completed_orders"]} of '
        f'{metrics["total_orders"]} sample orders were completed, '
        f'generating €{metrics["revenue"]:.2f} in completed-order '
        f'revenue across {metrics["unique_customers"]} customers '
        f'who placed an order. These figures describe only the '
        f'provided sample dataset.'
    ),
)


# ------------------------------------------------------------
# Executive summary
# ------------------------------------------------------------

section_header(
    label="Case Study Summary",
    title="What this case study demonstrates.",
    description=(
        "The project combines business reasoning, SQL and data "
        "validation into one small end-to-end BI workflow."
    ),
)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    summary_card(
        label="Business",
        title="Define before measuring",
        text=(
            "The business request is clarified before analysis: "
            "what counts as an order, which periods should be "
            "compared and how cancellations should be treated."
        ),
        variant="blue",
    )

with summary_col2:
    summary_card(
        label="SQL",
        title="Query at the right grain",
        text=(
            "The SQL solutions answer the requested questions and "
            "demonstrate why joined row counts are not always the "
            "same as distinct customer or order counts."
        ),
        variant="green",
    )

with summary_col3:
    summary_card(
        label="Data",
        title="Validate the result",
        text=(
            f'The supplied sample contains '
            f'{metrics["total_orders"]} orders: '
            f'{metrics["completed_orders"]} completed and '
            f'{metrics["cancelled_orders"]} cancelled, with '
            f'€{metrics["revenue"]:.2f} in completed revenue.'
        ),
        variant="navy",
    )


# ------------------------------------------------------------
# What's inside
# ------------------------------------------------------------

section_header(
    label="Explore the Project",
    title="From business reasoning to interactive analysis.",
    description=(
        "Each section focuses on a different part of the BI workflow. "
        "The analysis, SQL results and dashboard are all based on the "
        "same provided sample dataset."
    ),
)

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    navigation_card(
        number="01",
        title="Business Analysis",
        description=(
            "Clarifying the request, defining the right metrics "
            "and outlining the analysis workflow before querying data."
        ),
        tag="Task 1",
    )

    st.page_link(
        "pages/1_Business_Analysis.py",
        label="Open Business Analysis",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )

with nav_col2:
    navigation_card(
        number="02",
        title="SQL Solutions",
        description=(
            "SQL queries executed against the project database, "
            "together with outputs, reasoning and validation."
        ),
        tag="Task 2",
    )

    st.page_link(
        "pages/2_SQL_Solutions.py",
        label="Open SQL Solutions",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )

with nav_col3:
    navigation_card(
        number="03",
        title="Interactive Dashboard",
        description=(
            "An interactive view of order status, customers, "
            "completed revenue and the sample order timeline."
        ),
        tag="Interactive",
    )

    st.page_link(
        "pages/3_Dashboard.py",
        label="Open Dashboard",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )


st.write("")

nav_col4, nav_col5, nav_space = st.columns(
    [1, 1, 1]
)

with nav_col4:
    navigation_card(
        number="04",
        title="Data Explorer",
        description=(
            "Source tables, data-grain documentation, "
            "relationship checks and data-quality validation."
        ),
        tag="Data",
    )

    st.page_link(
        "pages/4_Data_Explorer.py",
        label="Open Data Explorer",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )

with nav_col5:
    navigation_card(
        number="05",
        title="Project Notes",
        description=(
            "Assumptions, limitations, data-model decisions "
            "and the methodology used throughout the case study."
        ),
        tag="Methodology",
    )

    st.page_link(
        "pages/5_Project_Notes.py",
        label="Open Project Notes",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Methodology
# ------------------------------------------------------------

section_header(
    label="Analysis Workflow",
    title="A structured approach to a small BI request.",
    description=(
        "The workflow separates business understanding, data validation "
        "and technical analysis so that the final result can be traced "
        "back to clear definitions and source data."
    ),
)

method_col1, method_col2, method_col3 = st.columns(3)

with method_col1:
    methodology_step(
        number="01",
        title="Understand",
        description=(
            "Clarify the business question, reporting period "
            "and the definition of the requested metrics."
        ),
    )

with method_col2:
    methodology_step(
        number="02",
        title="Validate",
        description=(
            "Review the source tables, data grain, relationships "
            "and potential data-quality issues."
        ),
    )

with method_col3:
    methodology_step(
        number="03",
        title="Analyze",
        description=(
            "Use SQL at the appropriate grain to calculate "
            "the requested results."
        ),
    )


st.write("")

method_col4, method_col5, method_col6 = st.columns(3)

with method_col4:
    methodology_step(
        number="04",
        title="Verify",
        description=(
            "Reconcile calculated outputs with the underlying "
            "sample data before presenting them."
        ),
    )

with method_col5:
    methodology_step(
        number="05",
        title="Visualize",
        description=(
            "Use visualizations where they make patterns and "
            "results easier to understand."
        ),
    )

with method_col6:
    methodology_step(
        number="06",
        title="Communicate",
        description=(
            "Present the result clearly while separating facts, "
            "assumptions and limitations."
        ),
    )


# ------------------------------------------------------------
# Data scope
# ------------------------------------------------------------

section_header(
    label="Data Scope",
    title="Small dataset, careful conclusions.",
)

scope_col1, scope_col2 = st.columns(
    [1.35, 1]
)

with scope_col1:
    st.markdown(
        """
The application uses only the sample tables supplied with the
home assignment. The figures shown throughout the project are
therefore demonstrations of the analysis logic rather than
measurements of real business performance.

This distinction is important because a small sample can verify
calculations and SQL logic, but it is not sufficient for broader
commercial conclusions.
        """
    )

with scope_col2:
    insight_card(
        title="Scope Reminder",
        value="Sample data",
        text=(
            "Metrics and visualizations should be interpreted only "
            "within the supplied dataset."
        ),
    )


# ------------------------------------------------------------
# Built with
# ------------------------------------------------------------

section_header(
    label="Technology",
    title="Built with a lightweight BI stack.",
)

st.markdown(
    """
`Python` &nbsp;&nbsp; `SQL` &nbsp;&nbsp; `SQLite`
&nbsp;&nbsp; `Pandas` &nbsp;&nbsp; `Streamlit`
&nbsp;&nbsp; `Plotly`
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

footer()