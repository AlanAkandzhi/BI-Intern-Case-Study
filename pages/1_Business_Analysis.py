import streamlit as st

from assets.ui import (
    footer,
    hero,
    insight_card,
    kpi_card,
    methodology_step,
    section_header,
)



hero(
    label="Task 1 · Business Analysis",
    title="Business Analysis",
    subtitle=(
        "Turning a short business request into clear definitions, "
        "meaningful KPIs and a reliable analytical approach."
    ),
    show_scope=True,
)



section_header(
    label="Business Request",
    title="A simple question can hide several definitions.",
    description=(
        "The request sounds straightforward, but cancellations, "
        "repeat customers and the free-delivery campaign can all "
        "change how the result should be interpreted."
    ),
)


request_col1, request_col2 = st.columns(
    [1.25, 0.75]
)


with request_col1:
    st.info(
        """
**Request from Sales**

"Hi, I need a report on the number of orders for last month.
How did we perform compared with the previous month?"
        """
    )

    st.markdown(
        """
Before calculating the comparison, I would clarify what the
business means by **orders**, which periods should be compared
and how cancellations should be treated.

Otherwise, the calculation could be technically correct while
still answering the wrong business question.
        """
    )


with request_col2:
    insight_card(
        title="Analyst Mindset",
        value="Define before calculating",
        text=(
            "The first step is not writing a query. It is making "
            "sure the metric, period and business definition are "
            "clear enough that the result will be meaningful."
        ),
    )



section_header(
    label="Known Context",
    title="Three details can materially affect the answer.",
)


context_col1, context_col2, context_col3 = st.columns(3)


with context_col1:
    kpi_card(
        label="Order Status",
        value="Cancelled",
        caption="Some orders are cancelled by customers",
        variant="red",
    )


with context_col2:
    kpi_card(
        label="Customer Behavior",
        value="Repeat",
        caption="One customer can place multiple orders",
        variant="blue",
    )


with context_col3:
    kpi_card(
        label="Commercial Context",
        value="Campaign",
        caption="Free delivery was active during part of the period",
        variant="navy",
    )



section_header(
    label="Clarify First",
    title="Questions I would ask before starting.",
    description=(
        "Each question resolves an ambiguity that could change "
        "the metric, the comparison or the final interpretation."
    ),
)


question_col1, question_col2 = st.columns(2)


with question_col1:

    with st.expander(
        "1. What should count as an order?",
        expanded=True,
    ):
        st.markdown(
            """
I would clarify whether the manager wants to see **all orders
created** during the period or only **successfully completed
orders**.

Because some orders are cancelled, these definitions can produce
different conclusions.

For a performance comparison, I would use completed orders as
the primary metric and analyse cancellations separately.
            """
        )


    with st.expander(
        "2. What exactly are the comparison periods?"
    ):
        st.markdown(
            """
I would confirm that **last month** means the last full calendar
month and that it should be compared with the full calendar month
immediately before it.

Clear date boundaries prevent incomplete or inconsistent periods
from being compared.
            """
        )


    with st.expander(
        "3. Do we need the percentage change as well?"
    ):
        st.markdown(
            """
I would ask whether the manager needs only the absolute order
counts or also the **month-over-month percentage change**.

I would recommend showing both. The counts provide scale, while
the percentage makes the direction and size of the change easier
to interpret.
            """
        )


with question_col2:

    with st.expander(
        "4. Should cancelled orders be analysed separately?",
        expanded=True,
    ):
        st.markdown(
            """
Yes. An increase in created orders does not necessarily mean
better performance if cancellations also increased significantly.

I would therefore include the **cancellation rate** alongside
completed-order volume.
            """
        )


    with st.expander(
        "5. Do we also want to understand how many customers ordered?"
    ):
        st.markdown(
            """
Because one customer can place multiple orders, growth in order
volume can come from two different sources:

- more customers placing orders
- existing customers ordering more frequently

I would therefore include unique customers as supporting context
if the manager wants to understand what is driving the change.
            """
        )


    with st.expander(
        "6. When exactly was the free-delivery campaign active?"
    ):
        st.markdown(
            """
I would ask for the exact campaign start and end dates.

If higher order volume overlaps with the campaign, I would show
that as useful context and, where possible, compare campaign and
non-campaign periods.

I would **not automatically claim causation**. The available data
may show an association, but proving that free delivery caused the
change would require additional analysis.
            """
        )



section_header(
    label="Metric Framework",
    title="Three metrics answer the core question.",
    description=(
        "I would keep the main report focused. Supporting metrics "
        "can then explain what may be driving the result."
    ),
)


metric_col1, metric_col2, metric_col3 = st.columns(3)


with metric_col1:
    kpi_card(
        label="Primary KPI",
        value="Completed Orders",
        caption="Successfully completed orders in each month",
        variant="green",
    )

    st.markdown(
        """
**Why**

This represents realized order activity more clearly than simply
counting every order created.
        """
    )


with metric_col2:
    kpi_card(
        label="Comparison KPI",
        value="MoM Change",
        caption="Relative change versus the previous month",
        variant="blue",
    )

    st.markdown(
        """
**Why**

The percentage change makes the direction and relative size of
the month-to-month movement easy to interpret.
        """
    )


with metric_col3:
    kpi_card(
        label="Quality KPI",
        value="Cancellation Rate",
        caption="Cancelled orders as a share of all orders",
        variant="red",
    )

    st.markdown(
        """
**Why**

Order volume alone can be misleading when a meaningful share of
orders are later cancelled.
        """
    )



section_header(
    label="Definitions",
    title="The calculations should be explicit.",
)


formula_col1, formula_col2 = st.columns(2)


with formula_col1:
    st.markdown("#### Month-over-Month Change")

    st.latex(
        r"""
        \frac{
            Orders_{last} - Orders_{previous}
        }{
            Orders_{previous}
        }
        \times 100
        """
    )

    st.caption(
        "Calculated using the agreed order definition for both periods."
    )


with formula_col2:
    st.markdown("#### Cancellation Rate")

    st.latex(
        r"""
        \frac{
            Cancelled\ Orders
        }{
            Total\ Orders
        }
        \times 100
        """
    )

    st.caption(
        "Shows the share of orders that were cancelled."
    )


st.warning(
    """
**Edge case**

If the previous month has zero completed orders, the standard
month-over-month percentage change cannot be calculated because
the denominator is zero.

In that case, I would report the absolute change and mark the
percentage change as **N/A** rather than forcing a misleading value.
    """
)



section_header(
    label="Supporting Context",
    title="Customer metrics help explain the change.",
)


support_col1, support_col2 = st.columns(2)


with support_col1:
    kpi_card(
        label="Supporting Metric",
        value="Unique Customers",
        caption="Distinct customers who placed an order",
        variant="blue",
    )

    st.markdown(
        """
This helps distinguish growth caused by **more customers** from
growth caused by existing customers ordering more frequently.
        """
    )


with support_col2:
    kpi_card(
        label="Supporting Metric",
        value="Orders / Customer",
        caption="Average ordering frequency",
        variant="navy",
    )

    st.markdown(
        """
If useful for the business question, this shows whether active
customers are ordering more or less frequently between periods.
        """
    )



section_header(
    label="Analytical Workflow",
    title="From request to business answer.",
    description=(
        "I would structure the work as a sequence of definition, "
        "validation, calculation and communication steps."
    ),
)


workflow_row1 = st.columns(3)


with workflow_row1[0]:
    methodology_step(
        number="01",
        title="Clarify",
        description=(
            "Confirm what counts as an order, the reporting periods, "
            "cancellation treatment and expected output."
        ),
    )


with workflow_row1[1]:
    methodology_step(
        number="02",
        title="Define",
        description=(
            "Set exact date boundaries and document the KPI "
            "definitions that will be applied consistently."
        ),
    )


with workflow_row1[2]:
    methodology_step(
        number="03",
        title="Validate",
        description=(
            "Check missing values, duplicate IDs, dates, statuses "
            "and whether records fall inside the required periods."
        ),
    )


st.write("")


workflow_row2 = st.columns(3)


with workflow_row2[0]:
    methodology_step(
        number="04",
        title="Check Grain",
        description=(
            "Confirm what one row represents before joining tables "
            "so order counts are not inflated by product rows."
        ),
    )


with workflow_row2[1]:
    methodology_step(
        number="05",
        title="Calculate",
        description=(
            "Calculate completed orders, month-over-month change "
            "and cancellation rate for both periods."
        ),
    )


with workflow_row2[2]:
    methodology_step(
        number="06",
        title="Explain",
        description=(
            "Use customer metrics and campaign timing as supporting "
            "context for the observed change."
        ),
    )


st.write("")


workflow_row3 = st.columns(3)


with workflow_row3[0]:
    methodology_step(
        number="07",
        title="Review Campaign",
        description=(
            "Compare campaign and non-campaign periods where the "
            "dates allow it, without assuming causation."
        ),
    )


with workflow_row3[1]:
    methodology_step(
        number="08",
        title="Reconcile",
        description=(
            "Perform sanity checks and reconcile totals before "
            "sharing the result with the business."
        ),
    )


with workflow_row3[2]:
    methodology_step(
        number="09",
        title="Communicate",
        description=(
            "Present a concise KPI comparison, a simple visual "
            "and a short interpretation of what changed."
        ),
    )



section_header(
    label="Business Context",
    title="The free-delivery campaign needs careful interpretation.",
)


campaign_col1, campaign_col2 = st.columns(
    [1.15, 0.85]
)


with campaign_col1:
    st.markdown(
        """
If the campaign dates are available, I would compare order
activity during the campaign with relevant non-campaign periods.

Useful questions would include:

- Did completed-order volume change during the campaign?
- Did unique customer activity change?
- Did cancellation behavior change?
- Was the pattern already moving before the campaign started?

This provides context without overstating what the data proves.
        """
    )


with campaign_col2:
    insight_card(
        title="Interpretation Rule",
        value="Association ≠ causation",
        text=(
            "A visible increase during the campaign does not by "
            "itself prove that free delivery caused the increase. "
            "Other factors may have changed at the same time."
        ),
    )



section_header(
    label="Final Output",
    title="The manager should get the answer quickly.",
    description=(
        "The final report should lead with the comparison and keep "
        "methodological detail available without making the result "
        "difficult to read."
    ),
)


example_data = {
    "Metric": [
        "Completed Orders",
        "Cancellation Rate",
        "Unique Customers",
    ],
    "Previous Month": [
        "X",
        "X%",
        "X",
    ],
    "Last Month": [
        "Y",
        "Y%",
        "Y",
    ],
    "Change": [
        "+/- X%",
        "+/- X pp",
        "+/- X%",
    ],
}


st.table(
    example_data
)


st.caption(
    "X and Y are placeholders because Task 1 does not provide "
    "the monthly dataset required to calculate these values."
)


output_col1, output_col2 = st.columns(
    [1.1, 0.9]
)


with output_col1:
    st.markdown(
        """
#### Short business interpretation

I would finish the report by explaining:

- whether completed-order volume increased or decreased
- whether the cancellation rate changed
- whether customer activity helps explain the movement
- whether the free-delivery campaign overlaps with the observed change
        """
    )


with output_col2:
    insight_card(
        title="Communication Goal",
        value="Answer first",
        text=(
            "The manager should be able to understand what changed "
            "before reading the supporting methodology. Detail "
            "should strengthen the answer, not hide it."
        ),
    )



section_header(
    label="Conclusion",
    title="A reliable answer starts with the right definition.",
)


st.success(
    """
My priority would be to agree on the business definitions before
calculating the result. Once the metric, periods and treatment of
cancellations are clear, the comparison itself is straightforward.

This reduces the risk of delivering a technically correct report
that answers a different question from the one the business
actually meant.
    """
)



footer()