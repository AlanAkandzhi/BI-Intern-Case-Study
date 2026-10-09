from pathlib import Path

import streamlit as st


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
CSS_PATH = ROOT_DIR / "assets" / "style.css"


# ------------------------------------------------------------
# Global CSS
# ------------------------------------------------------------

def load_css():
    with open(
        CSS_PATH,
        "r",
        encoding="utf-8",
    ) as css_file:
        css = css_file.read()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Badge
# ------------------------------------------------------------

def badge(
    text,
    variant="blue",
):
    return (
        f'<span class="bi-badge bi-badge-{variant}">'
        f'{text}'
        f'</span>'
    )


# ------------------------------------------------------------
# Hero
# ------------------------------------------------------------

def hero(
    label,
    title,
    subtitle,
    name=None,
    role=None,
    show_scope=True,
):
    scope_html = ""

    if show_scope:
        scope_html = (
            '<div class="hero-scope">'
            '<span class="scope-dot"></span>'
            'SAMPLE DATA'
            '</div>'
        )

    identity_html = ""

    if name:
        role_html = (
            f'<div class="hero-role">{role}</div>'
            if role
            else ""
        )

        identity_html = (
            '<div class="hero-identity">'
            f'<div class="hero-name">{name}</div>'
            f'{role_html}'
            '</div>'
        )

    hero_html = (
        '<div class="hero">'
        '<div class="hero-glow hero-glow-one"></div>'
        '<div class="hero-glow hero-glow-two"></div>'
        '<div class="hero-grid"></div>'
        '<div class="hero-content">'
        '<div class="hero-topline">'
        f'<div class="hero-label">{label}</div>'
        f'{scope_html}'
        '</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-subtitle">{subtitle}</div>'
        f'{identity_html}'
        '</div>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Section heading
# ------------------------------------------------------------

def section_header(
    label,
    title,
    description=None,
):
    description_html = ""

    if description:
        description_html = (
            f'<div class="section-description">'
            f'{description}'
            f'</div>'
        )

    html = (
        '<div class="section-heading">'
        f'<div class="section-label">{label}</div>'
        f'<div class="section-title">{title}</div>'
        f'{description_html}'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def section_label(text):
    st.markdown(
        f'<div class="section-label">{text}</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# KPI card
# ------------------------------------------------------------

def kpi_card(
    label,
    value,
    caption="",
    variant="blue",
):
    html = (
        f'<div class="kpi-card kpi-{variant}">'
        '<div class="kpi-accent"></div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-caption">{caption}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Insight card
# ------------------------------------------------------------

def insight_card(
    title,
    text,
    value=None,
    variant="blue",
):
    value_html = ""

    if value is not None:
        value_html = (
            f'<div class="insight-value">{value}</div>'
        )

    html = (
        f'<div class="insight-card insight-{variant}">'
        '<div class="insight-icon">↗</div>'
        '<div class="insight-content">'
        f'<div class="insight-title">{title}</div>'
        f'{value_html}'
        f'<div class="insight-text">{text}</div>'
        '</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Navigation card
# ------------------------------------------------------------

def navigation_card(
    number,
    title,
    description,
    tag=None,
):
    tag_html = ""

    if tag:
        tag_html = (
            f'<div class="navigation-card-tag">'
            f'{tag}'
            f'</div>'
        )

    html = (
        '<div class="navigation-card">'
        '<div class="navigation-card-top">'
        f'<div class="navigation-card-number">{number}</div>'
        f'{tag_html}'
        '</div>'
        f'<div class="navigation-card-title">{title}</div>'
        f'<div class="navigation-card-text">{description}</div>'
        '<div class="navigation-card-arrow">Explore →</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Methodology step
# ------------------------------------------------------------

def methodology_step(
    number,
    title,
    description,
):
    html = (
        '<div class="method-card">'
        f'<div class="method-number">{number}</div>'
        f'<div class="method-title">{title}</div>'
        f'<div class="method-text">{description}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Status pill
# ------------------------------------------------------------

def status_pill(
    text,
    status="validated",
):
    html = (
        f'<span class="status-pill status-{status}">'
        '<span class="status-pill-dot"></span>'
        f'{text}'
        '</span>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Executive summary card
# ------------------------------------------------------------

def summary_card(
    label,
    title,
    text,
    variant="blue",
):
    number_map = {
        "blue": "01",
        "green": "02",
        "navy": "03",
    }

    number = number_map.get(
        variant,
        "01",
    )

    html = (
        f'<div class="summary-card summary-{variant}">'
        '<div class="summary-card-top">'
        f'<div class="summary-card-icon">{number}</div>'
        f'<div class="summary-card-label">{label}</div>'
        '</div>'
        f'<div class="summary-card-title">{title}</div>'
        f'<div class="summary-card-text">{text}</div>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

def footer():
    footer_html = (
        '<div class="project-footer">'
        '<div class="footer-name">'
        'Alan Akandzhi'
        '<span class="footer-dot"> · </span>'
        'BI Intern Case Study'
        '</div>'
        '<div class="footer-stack">'
        'Python'
        '<span> · </span>'
        'SQL'
        '<span> · </span>'
        'SQLite'
        '<span> · </span>'
        'Pandas'
        '<span> · </span>'
        'Streamlit'
        '<span> · </span>'
        'Plotly'
        '</div>'
        '</div>'
    )

    st.markdown(
        footer_html,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Legacy sidebar helper
# ------------------------------------------------------------

def sidebar_brand():
    """
    Temporary compatibility helper.

    The existing project pages still import sidebar_brand().
    Navigation and sidebar branding are now handled globally
    by app.py, so this function intentionally does nothing.

    It can be removed after all pages are migrated to the
    new application structure.
    """
    pass