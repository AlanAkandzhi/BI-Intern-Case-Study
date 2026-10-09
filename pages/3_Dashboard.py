import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from assets.ui import (
    footer,
    hero,
    insight_card,
    kpi_card,
    section_header,
)


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "database" / "bi_home_task.db"


# ------------------------------------------------------------
# Visual constants
# ------------------------------------------------------------

BLUE = "#3B82F6"
BLUE_DARK = "#2563EB"
GREEN = "#10B981"
RED = "#EF4444"
NAVY = "#0F172A"
SLATE = "#64748B"
GRID = "#E2E8F0"

STATUS_COLORS = {
    "completed": GREEN,
    "cancelled": RED,
}


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as connection:
        customers = pd.read_sql_query(
            "SELECT * FROM customers",
            connection,
        )

        orders = pd.read_sql_query(
            "SELECT * FROM orders",
            connection,
        )

        products = pd.read_sql_query(
            "SELECT * FROM products",
            connection,
        )

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    return customers, orders, products


customers, orders, products = load_data()


# ------------------------------------------------------------
# Prepare analytical dataset
# ------------------------------------------------------------

# Product data is at order-line grain.
# Aggregate it first so the analytical dataset contains
# one row per order before calculating order-level metrics.

order_values = (
    products
    .assign(
        line_value=(
            products["quantity"]
            * products["unit_price"]
        )
    )
    .groupby(
        "order_id",
        as_index=False,
    )["line_value"]
    .sum()
    .rename(
        columns={
            "line_value": "order_value",
        }
    )
)


analysis_df = (
    orders
    .merge(
        customers,
        left_on="customer_id",
        right_on="id",
        how="left",
        suffixes=("_order", "_customer"),
    )
    .merge(
        order_values,
        left_on="id_order",
        right_on="order_id",
        how="left",
    )
)


analysis_df["order_value"] = (
    analysis_df["order_value"].fillna(0)
)


# ------------------------------------------------------------
# Plotly theme helper
# ------------------------------------------------------------

def apply_chart_theme(
    figure,
    show_legend=False,
):
    figure.update_layout(
        template="plotly_white",
        showlegend=show_legend,
        font=dict(
            family="Arial, sans-serif",
            color="#475569",
            size=13,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        margin=dict(
            l=24,
            r=24,
            t=25,
            b=25,
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            bordercolor=NAVY,
            font=dict(
                color="#FFFFFF",
                size=13,
            ),
        ),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    figure.update_xaxes(
        showgrid=False,
        linecolor=GRID,
        tickfont=dict(
            color=SLATE,
        ),
        title_font=dict(
            color=SLATE,
        ),
    )

    figure.update_yaxes(
        gridcolor="#F1F5F9",
        zeroline=False,
        linecolor=GRID,
        tickfont=dict(
            color=SLATE,
        ),
        title_font=dict(
            color=SLATE,
        ),
    )

    return figure


# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------

hero(
    label="Interactive Analysis",
    title="Sales Dashboard",
    subtitle=(
        "Explore order activity, customer behavior and completed "
        "revenue through an interactive view of the provided "
        "sample dataset."
    ),
    show_scope=True,
)


# ------------------------------------------------------------
# Dashboard context
# ------------------------------------------------------------

section_header(
    label="Dashboard",
    title="Interactive sample-data overview.",
    description=(
        "Use the filters below to explore the supplied order data. "
        "All KPIs, charts and insights update from the current "
        "selection."
    ),
)


# ------------------------------------------------------------
# Filters
# ------------------------------------------------------------

with st.container(border=True):

    filter_title_col, reset_col = st.columns(
        [5, 1]
    )

    with filter_title_col:
        st.markdown("#### Filters")
        st.caption(
            "Filter the dashboard by customer city and order status."
        )

    with reset_col:
        st.write("")

        if st.button(
            "Reset Filters",
            icon=":material/restart_alt:",
            use_container_width=True,
        ):
            st.session_state["dashboard_cities"] = (
                sorted(
                    analysis_df["city"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

            st.session_state["dashboard_statuses"] = (
                sorted(
                    analysis_df["status"]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )

            st.rerun()

    city_options = sorted(
        analysis_df["city"]
        .dropna()
        .unique()
        .tolist()
    )

    status_options = sorted(
        analysis_df["status"]
        .dropna()
        .unique()
        .tolist()
    )

    if "dashboard_cities" not in st.session_state:
        st.session_state["dashboard_cities"] = (
            city_options.copy()
        )

    if "dashboard_statuses" not in st.session_state:
        st.session_state["dashboard_statuses"] = (
            status_options.copy()
        )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_cities = st.multiselect(
            "City",
            options=city_options,
            key="dashboard_cities",
        )

    with filter_col2:
        selected_statuses = st.multiselect(
            "Order Status",
            options=status_options,
            key="dashboard_statuses",
        )


# ------------------------------------------------------------
# Apply filters
# ------------------------------------------------------------

filtered_df = analysis_df[
    analysis_df["city"].isin(selected_cities)
    & analysis_df["status"].isin(selected_statuses)
].copy()


# ------------------------------------------------------------
# Empty state
# ------------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No records match the current filter selection. "
        "Select at least one city and one order status, "
        "or use Reset Filters."
    )

    footer()
    st.stop()


# ------------------------------------------------------------
# KPI calculations
# ------------------------------------------------------------

total_orders = filtered_df[
    "id_order"
].nunique()


completed_orders = filtered_df.loc[
    filtered_df["status"] == "completed",
    "id_order",
].nunique()


cancelled_orders = filtered_df.loc[
    filtered_df["status"] == "cancelled",
    "id_order",
].nunique()


unique_customers = filtered_df[
    "customer_id"
].nunique()


completed_revenue = filtered_df.loc[
    filtered_df["status"] == "completed",
    "order_value",
].sum()


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


# ------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------

section_header(
    label="Current Selection",
    title="Key performance indicators.",
    description=(
        "The metrics below respond directly to the active dashboard "
        "filters."
    ),
)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    kpi_card(
        label="Total Orders",
        value=total_orders,
        caption="Current selection",
        variant="blue",
    )

with kpi2:
    kpi_card(
        label="Completed",
        value=completed_orders,
        caption=f"{completion_rate:.0f}% completion rate",
        variant="green",
    )

with kpi3:
    kpi_card(
        label="Cancelled",
        value=cancelled_orders,
        caption=f"{cancellation_rate:.0f}% cancellation rate",
        variant="red",
    )

with kpi4:
    kpi_card(
        label="Unique Customers",
        value=unique_customers,
        caption="Customers in selection",
        variant="navy",
    )

with kpi5:
    kpi_card(
        label="Completed Revenue",
        value=f"€{completed_revenue:.2f}",
        caption="Completed orders only",
        variant="blue",
    )


# ------------------------------------------------------------
# Dynamic insight
# ------------------------------------------------------------

st.write("")


if completed_orders and cancelled_orders:
    insight_text = (
        f"The current selection contains {total_orders} orders "
        f"from {unique_customers} unique customers. "
        f"{completed_orders} orders were completed and "
        f"{cancelled_orders} were cancelled. Completed orders "
        f"generated €{completed_revenue:.2f} in revenue."
    )

elif completed_orders and not cancelled_orders:
    insight_text = (
        f"The current selection contains {total_orders} completed "
        f"{'order' if total_orders == 1 else 'orders'} from "
        f"{unique_customers} unique "
        f"{'customer' if unique_customers == 1 else 'customers'}, "
        f"generating €{completed_revenue:.2f} in completed revenue. "
        f"No cancelled orders are included under the active filters."
    )

elif cancelled_orders and not completed_orders:
    insight_text = (
        f"The current selection contains {total_orders} cancelled "
        f"{'order' if total_orders == 1 else 'orders'} from "
        f"{unique_customers} unique "
        f"{'customer' if unique_customers == 1 else 'customers'}. "
        f"No completed orders are included, so completed revenue "
        f"is €0.00."
    )

else:
    insight_text = (
        "The current filter selection contains order activity, "
        "but no completed or cancelled orders under the defined "
        "status categories."
    )


insight_card(
    title="Dynamic Insight",
    value=f"{completion_rate:.0f}% completion rate",
    text=insight_text,
)

# ------------------------------------------------------------
# Export current selection
# ------------------------------------------------------------

section_header(
    label="Export Data",
    title="Take the current analysis with you.",
    description=(
        "Downloads reflect the active dashboard filters and use "
        "the same order-level data and KPI definitions shown above."
    ),
)


# Prepare a clean order-level export.
# The dashboard analytical dataset already contains one row per order,
# so exporting from filtered_df preserves the correct grain.

export_df = (
    filtered_df[
        [
            "id_order",
            "order_date",
            "customer_id",
            "name",
            "city",
            "status",
            "order_value",
        ]
    ]
    .copy()
    .rename(
        columns={
            "id_order": "order_id",
            "name": "customer_name",
        }
    )
    .sort_values(
        [
            "order_date",
            "order_id",
        ]
    )
)


# Format the date for a clean CSV output.

export_df["order_date"] = (
    export_df["order_date"]
    .dt.strftime("%Y-%m-%d")
)


# Round monetary values for export.

export_df["order_value"] = (
    export_df["order_value"]
    .round(2)
)


current_view_csv = export_df.to_csv(
    index=False
).encode("utf-8-sig")


# Prepare a compact KPI summary for the same active selection.

kpi_export_df = pd.DataFrame(
    {
        "Metric": [
            "Total Orders",
            "Completed Orders",
            "Cancelled Orders",
            "Unique Customers",
            "Completed Revenue",
            "Completion Rate",
            "Cancellation Rate",
        ],
        "Value": [
            str(total_orders),
            str(completed_orders),
            str(cancelled_orders),
            str(unique_customers),
            f"{completed_revenue:.2f}",
            f"{completion_rate:.2f}%",
            f"{cancellation_rate:.2f}%",
        ],
    }
)


kpi_summary_csv = kpi_export_df.to_csv(
    index=False
).encode("utf-8-sig")


export_col1, export_col2, export_space = st.columns(
    [1.8, 1.8, 2.4]
)


with export_col1:
    st.download_button(
        label="Download Current View",
        data=current_view_csv,
        file_name="bi_dashboard_current_view.csv",
        mime="text/csv",
        icon=":material/download:",
        use_container_width=True,
    )


with export_col2:
    st.download_button(
        label="Download KPI Summary",
        data=kpi_summary_csv,
        file_name="bi_dashboard_kpi_summary.csv",
        mime="text/csv",
        icon=":material/download:",
        use_container_width=True,
    )


st.caption(
    "CSV exports contain only the records and metrics included "
    "under the current dashboard filters."
)


# ------------------------------------------------------------
# Order status and customer activity
# ------------------------------------------------------------

section_header(
    label="Order Activity",
    title="Status and customer distribution.",
    description=(
        "Order counts are calculated at order grain so product-line "
        "rows do not inflate the results."
    ),
)


status_counts = (
    filtered_df
    .groupby(
        "status",
        as_index=False,
    )
    .agg(
        orders=("id_order", "nunique")
    )
)


customer_orders = (
    filtered_df
    .groupby(
        [
            "customer_id",
            "name",
        ],
        as_index=False,
    )
    .agg(
        orders=("id_order", "nunique")
    )
    .sort_values(
        [
            "orders",
            "name",
        ],
        ascending=[
            True,
            False,
        ],
    )
)


chart_col1, chart_col2 = st.columns(
    [0.9, 1.1]
)


# ------------------------------------------------------------
# Donut chart
# ------------------------------------------------------------

with chart_col1:

    st.markdown("#### Order Completion")

    donut_colors = [
        STATUS_COLORS.get(
            status,
            BLUE,
        )
        for status in status_counts["status"]
    ]

    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=status_counts["status"],
                values=status_counts["orders"],
                hole=0.70,
                marker=dict(
                    colors=donut_colors,
                    line=dict(
                        color="#FFFFFF",
                        width=3,
                    ),
                ),
                textinfo="none",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Orders: %{value}<br>"
                    "Share: %{percent}"
                    "<extra></extra>"
                ),
                sort=False,
            )
        ]
    )

    fig_donut.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=70,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            title=None,
        ),
        annotations=[
            dict(
                text=(
                    f"<b>{completion_rate:.0f}%</b>"
                    "<br>"
                    "<span style='font-size:12px'>completed</span>"
                ),
                x=0.5,
                y=0.5,
                font=dict(
                    size=22,
                    color=NAVY,
                ),
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )


# ------------------------------------------------------------
# Orders by customer
# ------------------------------------------------------------

with chart_col2:

    st.markdown("#### Orders by Customer")

    fig_customers = px.bar(
        customer_orders,
        x="orders",
        y="name",
        orientation="h",
        text="orders",
        labels={
            "name": "",
            "orders": "Orders",
        },
    )

    fig_customers.update_traces(
        marker_color=BLUE,
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Orders: %{x}"
            "<extra></extra>"
        ),
    )

    fig_customers.update_layout(
        height=390,
    )

    fig_customers = apply_chart_theme(
        fig_customers,
        show_legend=False,
    )

    fig_customers.update_yaxes(
        categoryorder="array",
        categoryarray=customer_orders["name"].tolist(),
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )


# ------------------------------------------------------------
# Completed revenue
# ------------------------------------------------------------

section_header(
    label="Revenue",
    title="Completed revenue by customer.",
    description=(
        "Revenue is calculated only from completed orders using "
        "quantity multiplied by unit price at product-line level."
    ),
)


completed_df = filtered_df[
    filtered_df["status"] == "completed"
].copy()


if not completed_df.empty:

    revenue_by_customer = (
        completed_df
        .groupby(
            [
                "customer_id",
                "name",
            ],
            as_index=False,
        )
        .agg(
            revenue=("order_value", "sum")
        )
        .sort_values(
            [
                "revenue",
                "name",
            ],
            ascending=[
                True,
                False,
            ],
        )
    )

    fig_revenue = px.bar(
        revenue_by_customer,
        x="revenue",
        y="name",
        orientation="h",
        text="revenue",
        labels={
            "name": "",
            "revenue": "Completed Revenue (€)",
        },
    )

    fig_revenue.update_traces(
        marker_color=BLUE_DARK,
        texttemplate="€%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Completed revenue: €%{x:.2f}"
            "<extra></extra>"
        ),
    )

    fig_revenue.update_layout(
        height=380,
    )

    fig_revenue = apply_chart_theme(
        fig_revenue,
        show_legend=False,
    )

    fig_revenue.update_yaxes(
        categoryorder="array",
        categoryarray=revenue_by_customer["name"].tolist(),
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

else:

    st.info(
        "No completed orders are included in the current "
        "filter selection, so there is no completed revenue "
        "to visualize."
    )


# ------------------------------------------------------------
# Timeline
# ------------------------------------------------------------

section_header(
    label="Timeline",
    title="Orders over time.",
    description=(
        "The timeline shows order activity by date and status "
        "within the current filter selection."
    ),
)


orders_over_time = (
    filtered_df
    .groupby(
        [
            "order_date",
            "status",
        ],
        as_index=False,
    )
    .agg(
        orders=("id_order", "nunique")
    )
)


fig_timeline = px.bar(
    orders_over_time,
    x="order_date",
    y="orders",
    color="status",
    barmode="group",
    color_discrete_map=STATUS_COLORS,
    labels={
        "order_date": "Order Date",
        "orders": "Orders",
        "status": "Status",
    },
)


fig_timeline.update_traces(
    hovertemplate=(
        "<b>%{x|%d %b %Y}</b><br>"
        "Orders: %{y}"
        "<extra></extra>"
    ),
)


fig_timeline.update_layout(
    height=400,
    bargap=0.32,
)


fig_timeline = apply_chart_theme(
    fig_timeline,
    show_legend=True,
)


fig_timeline.update_xaxes(
    tickformat="%d %b",
)


st.plotly_chart(
    fig_timeline,
    use_container_width=True,
    config={
        "displayModeBar": False,
    },
)


# ------------------------------------------------------------
# Geography
# ------------------------------------------------------------

section_header(
    label="Customer Geography",
    title="Order activity by city.",
    description=(
        "Only cities represented by customers with orders appear "
        "in this dashboard view."
    ),
)


city_summary = (
    filtered_df
    .groupby(
        "city",
        as_index=False,
    )
    .agg(
        customers=("customer_id", "nunique"),
        orders=("id_order", "nunique"),
    )
    .sort_values(
        "orders",
        ascending=False,
    )
)


city_summary_display = city_summary.rename(
    columns={
        "city": "City",
        "customers": "Unique Customers",
        "orders": "Orders",
    }
)


st.dataframe(
    city_summary_display,
    use_container_width=True,
    hide_index=True,
)


# ------------------------------------------------------------
# Full sample observations
# ------------------------------------------------------------

section_header(
    label="Full Sample",
    title="What the complete sample tells us.",
    description=(
        "The observations below refer to the complete dataset and "
        "do not change with the dashboard filters."
    ),
)


full_total_orders = analysis_df[
    "id_order"
].nunique()


full_completed_orders = analysis_df.loc[
    analysis_df["status"] == "completed",
    "id_order",
].nunique()


full_cancelled_orders = analysis_df.loc[
    analysis_df["status"] == "cancelled",
    "id_order",
].nunique()


full_unique_customers = analysis_df[
    "customer_id"
].nunique()


full_completed_revenue = analysis_df.loc[
    analysis_df["status"] == "completed",
    "order_value",
].sum()


full_cancellation_rate = (
    full_cancelled_orders
    / full_total_orders
    * 100
    if full_total_orders
    else 0
)


observation_col1, observation_col2 = st.columns(
    [1.15, 0.85]
)


with observation_col1:

    st.markdown(
        f"""
        - **{full_total_orders} orders** are present in the sample.
        - **{full_completed_orders} orders** are completed.
        - **{full_cancelled_orders} orders** are cancelled.
        - **{full_unique_customers} unique customers** placed an order.
        - Completed orders generate **€{full_completed_revenue:.2f}**.
        - The sample cancellation rate is **{full_cancellation_rate:.0f}%**.
        """
    )


with observation_col2:

    insight_card(
        title="Interpretation Limit",
        value="Sample only",
        text=(
            "These observations validate the analytical logic, "
            "but the dataset is too small to support broader "
            "business-performance conclusions."
        ),
    )


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

footer()