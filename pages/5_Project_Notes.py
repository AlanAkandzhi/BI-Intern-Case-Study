import streamlit as st

from assets.ui import (
    footer,
    hero,
    insight_card,
    kpi_card,
    methodology_step,
    section_header,
    status_pill,
)



hero(
    label="Methodology · Documentation",
    title="Project Notes",
    subtitle=(
        "Assumptions, metric definitions, data-model decisions, "
        "limitations and methodology used throughout the case study."
    ),
    show_scope=True,
)



section_header(
    label="Documentation",
    title="Making the analytical decisions visible.",
    description=(
        "This page documents the assumptions and decisions behind "
        "the analysis so that calculated results can be separated "
        "from interpretation and unsupported assumptions."
    ),
)


intro_col1, intro_col2 = st.columns(
    [1.2, 0.8]
)


with intro_col1:
    st.markdown(
        """
The assignment itself is small, but several analytical choices
still matter: what counts as revenue, what defines a unique
customer, how table grain affects JOINs and which conclusions are
actually supported by the provided data.

Documenting those decisions makes the analysis easier to review,
reproduce and challenge.
        """
    )


with intro_col2:
    insight_card(
        title="Documentation Principle",
        value="Facts ≠ assumptions",
        text=(
            "Calculated results, business assumptions and analytical "
            "limitations are kept separate throughout the project."
        ),
    )



section_header(
    label="Core Rules",
    title="The definitions used throughout the project.",
    description=(
        "These rules keep the SQL, dashboard and written analysis "
        "consistent with one another."
    ),
)


rule_col1, rule_col2, rule_col3, rule_col4 = st.columns(4)


with rule_col1:
    kpi_card(
        label="Revenue",
        value="Completed",
        caption="Only completed orders contribute to completed revenue",
        variant="green",
    )


with rule_col2:
    kpi_card(
        label="Customer",
        value="customer_id",
        caption="Used to identify unique customers",
        variant="blue",
    )


with rule_col3:
    kpi_card(
        label="Task 1 Period",
        value="Full Month",
        caption="Last full calendar month vs previous full month",
        variant="navy",
    )


with rule_col4:
    kpi_card(
        label="SQL Grain",
        value="Explicit",
        caption="Counts are calculated at the intended entity grain",
        variant="blue",
    )



section_header(
    label="Assumptions",
    title="What I assume and why.",
    description=(
        "Where the assignment leaves room for interpretation, "
        "the assumption is documented rather than silently embedded "
        "inside a calculation."
    ),
)


assumption_col1, assumption_col2 = st.columns(2)


with assumption_col1:

    with st.expander(
        "1. Order Status",
        expanded=True,
    ):
        st.markdown(
            """
The sample contains two order statuses:

- `completed`
- `cancelled`

For **completed revenue**, only completed orders are included.
A cancelled order should not be treated as realized revenue.

For general order-volume analysis, both statuses may be relevant
depending on the business definition being used.
            """
        )


    with st.expander(
        "2. Revenue Definition",
        expanded=True,
    ):
        st.markdown(
            """
Revenue in this case study is calculated from product rows as:

**quantity × unit_price**

Only product rows belonging to completed orders contribute to the
metric when it is labelled **completed revenue**.

The sample does not contain taxes, discounts, refunds or delivery
fees, so those components cannot be included.
            """
        )


with assumption_col2:

    with st.expander(
        "3. Unique Customer Definition",
        expanded=True,
    ):
        st.markdown(
            """
A unique customer is identified by `customer_id`.

When answering how many different customers placed an order,
each customer is counted once regardless of how many orders that
customer placed.
            """
        )


    with st.expander(
        "4. Task 1 Reporting Period",
        expanded=True,
    ):
        st.markdown(
            """
I interpret **last month** as the last full calendar month and
**previous month** as the full calendar month immediately before it.

In a real business request, I would confirm this interpretation
with the stakeholder before starting the analysis.
            """
        )



section_header(
    label="Schema Decision",
    title="products vs order_items",
    description=(
        "The assignment uses two names for what appears to be the "
        "same order-line dataset."
    ),
)


schema_col1, schema_col2 = st.columns(
    [1.15, 0.85]
)


with schema_col1:
    st.markdown(
        """
The supplied sample names the third table `products`.

In the final SQL question, the colleague's example query instead
references `order_items`.

Based on the structure of the assignment, I treat both references
as the same supplied order-line dataset and use **`products`**
throughout the SQLite implementation.

This keeps the implementation consistent with the table that was
actually provided.
        """
    )


with schema_col2:
    insight_card(
        title="Schema Assumption",
        value="products = order lines",
        text=(
            "In a real environment I would verify this against the "
            "database schema or data dictionary rather than relying "
            "on the assumption."
        ),
    )



section_header(
    label="Data Grain",
    title="One row means something different in every table.",
    description=(
        "Understanding grain before joining is one of the most "
        "important safeguards in this case study."
    ),
)


grain_col1, grain_col2, grain_col3 = st.columns(3)


with grain_col1:
    kpi_card(
        label="customers",
        value="1 row",
        caption="per customer",
        variant="blue",
    )


with grain_col2:
    kpi_card(
        label="orders",
        value="1 row",
        caption="per order",
        variant="navy",
    )


with grain_col3:
    kpi_card(
        label="products",
        value="1 row",
        caption="per order line",
        variant="blue",
    )


st.write("")


insight_card(
    title="Grain Risk",
    value="1 order can become N rows",
    text=(
        "Joining orders directly to product-level data can create "
        "multiple rows for the same order. Order and customer counts "
        "must therefore use the appropriate grain or DISTINCT where "
        "required."
    ),
)



section_header(
    label="Scope Control",
    title="Why Task 1 and Task 2 remain separate.",
    description=(
        "The two tasks serve different purposes and do not provide "
        "the same data."
    ),
)


scope_col1, scope_col2 = st.columns(2)


with scope_col1:
    st.markdown(
        """
#### Task 1

Task 1 describes a business scenario requiring a comparison
between two months.

However, it does **not** provide the actual monthly dataset
required to calculate that comparison.

The response therefore focuses on:

- clarifying questions
- metric definitions
- analytical process
- expected reporting structure
        """
    )


with scope_col2:
    st.markdown(
        """
#### Task 2

Task 2 provides a small sample dataset intended for the SQL
questions.

That sample is used for:

- SQL execution
- validation
- sample-data KPIs
- dashboard visualizations
- data-quality checks
        """
    )


st.write("")


insight_card(
    title="Scope Rule",
    value="No invented MoM result",
    text=(
        "The Task 2 March and April sample is not used to manufacture "
        "a month-over-month answer for Task 1. Calculated results are "
        "shown only where the supplied data supports them."
    ),
)



section_header(
    label="Data Quality",
    title="Validation happens before interpretation.",
    description=(
        "The Data Explorer implements a small set of checks that "
        "protect the calculations from common structural issues."
    ),
)


quality_row1 = st.columns(3)


with quality_row1[0]:
    methodology_step(
        number="01",
        title="Primary Keys",
        description=(
            "Check customer, order and product-row IDs for duplicates."
        ),
    )


with quality_row1[1]:
    methodology_step(
        number="02",
        title="Missing Values",
        description=(
            "Check the source tables for missing values before analysis."
        ),
    )


with quality_row1[2]:
    methodology_step(
        number="03",
        title="Order Status",
        description=(
            "Verify that statuses match the expected completed and "
            "cancelled values."
        ),
    )


st.write("")


quality_row2 = st.columns(2)


with quality_row2[0]:
    methodology_step(
        number="04",
        title="Customer Relationship",
        description=(
            "Check that every order references an existing customer."
        ),
    )


with quality_row2[1]:
    methodology_step(
        number="05",
        title="Order Relationship",
        description=(
            "Check that every product row references an existing order."
        ),
    )


st.write("")


status_pill(
    "IMPLEMENTED IN DATA EXPLORER",
    status="validated",
)



section_header(
    label="Limitations",
    title="What the supplied data cannot tell us.",
    description=(
        "The sample is sufficient for demonstrating SQL and analytical "
        "reasoning, but it is not sufficient for broad business conclusions."
    ),
)


limitation_col1, limitation_col2 = st.columns(2)


with limitation_col1:

    with st.expander(
        "Small Sample Size",
        expanded=True,
    ):
        st.markdown(
            """
The dataset contains only a few customers and orders.

It is useful for demonstrating SQL logic, table relationships and
validation methodology, but not for drawing broad conclusions about
business performance or customer behaviour.
            """
        )


    with st.expander(
        "No Free-Delivery Indicator",
        expanded=True,
    ):
        st.markdown(
            """
Task 1 mentions a free-delivery campaign, but the provided data does
not contain campaign dates or a field identifying whether an order
was placed during the campaign.

The campaign effect therefore cannot be calculated from this sample.
            """
        )


with limitation_col2:

    with st.expander(
        "No Delivery Cost",
        expanded=True,
    ):
        st.markdown(
            """
The sample contains product quantity and unit price but no delivery
fees or delivery costs.

The project can calculate completed product revenue, but it cannot
evaluate the financial cost or profitability impact of free delivery.
            """
        )


    with st.expander(
        "No Causal Conclusion",
        expanded=True,
    ):
        st.markdown(
            """
Even if higher order volume overlapped with the free-delivery
campaign, that alone would not prove that the campaign caused
the increase.

Seasonality, marketing activity, customer mix and other external
factors could also affect order volume.
            """
        )



section_header(
    label="Production Extension",
    title="What I would add with real business data.",
    description=(
        "With a larger dataset and richer business context, the same "
        "analytical foundation could support deeper reporting."
    ),
)


production_col1, production_col2 = st.columns(2)


with production_col1:
    st.markdown(
        """
#### Order Performance

- month-over-month trends
- completion and cancellation trends
- average order value
- revenue trends
- orders per active customer

#### Customer Analysis

- new vs returning customers
- repeat-order behaviour
- purchase frequency
- customer segmentation
        """
    )


with production_col2:
    st.markdown(
        """
#### Campaign Analysis

- campaign vs non-campaign periods
- order-volume difference
- customer participation
- average order value during campaign
- delivery-cost impact

#### Reporting

- automated refresh
- date filters
- KPI monitoring
- anomaly checks
- scheduled reporting
        """
    )



section_header(
    label="Methodology",
    title="The workflow used across the case study.",
    description=(
        "The project follows the same basic sequence from the initial "
        "business question through validation and communication."
    ),
)


method_row1 = st.columns(4)


with method_row1[0]:
    methodology_step(
        number="01",
        title="Understand",
        description=(
            "Clarify what the stakeholder actually wants to measure."
        ),
    )


with method_row1[1]:
    methodology_step(
        number="02",
        title="Define",
        description=(
            "Agree on statuses, periods and metric definitions."
        ),
    )


with method_row1[2]:
    methodology_step(
        number="03",
        title="Model",
        description=(
            "Understand table grain, keys and relationships."
        ),
    )


with method_row1[3]:
    methodology_step(
        number="04",
        title="Validate Data",
        description=(
            "Check source quality before calculating results."
        ),
    )


st.write("")


method_row2 = st.columns(4)


with method_row2[0]:
    methodology_step(
        number="05",
        title="Query",
        description=(
            "Use SQL at the appropriate grain and avoid unnecessary joins."
        ),
    )


with method_row2[1]:
    methodology_step(
        number="06",
        title="Reconcile",
        description=(
            "Validate calculated values against the source sample."
        ),
    )


with method_row2[2]:
    methodology_step(
        number="07",
        title="Visualize",
        description=(
            "Use charts where they improve understanding of the result."
        ),
    )


with method_row2[3]:
    methodology_step(
        number="08",
        title="Communicate",
        description=(
            "Separate facts, assumptions, interpretation and limitations."
        ),
    )



section_header(
    label="Final Principles",
    title="What I wanted the solution to demonstrate.",
)


principle_col1, principle_col2, principle_col3 = st.columns(3)


with principle_col1:
    kpi_card(
        label="Principle 01",
        value="Correct",
        caption="Metrics answer the intended business question",
        variant="green",
    )


with principle_col2:
    kpi_card(
        label="Principle 02",
        value="Traceable",
        caption="Results can be connected back to source data and SQL",
        variant="blue",
    )


with principle_col3:
    kpi_card(
        label="Principle 03",
        value="Clear",
        caption="The output remains understandable to a business user",
        variant="navy",
    )


st.write("")


insight_card(
    title="Final Note",
    value="Reasoning before complexity",
    text=(
        "The goal of the additional application, validation and "
        "visualization is to make the requested analysis easier to "
        "understand and verify. They support the core business and SQL "
        "answers rather than replacing them."
    ),
)



footer()