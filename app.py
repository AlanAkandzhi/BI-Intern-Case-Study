import streamlit as st

from assets.ui import load_css


# ------------------------------------------------------------
# Application configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="BI Intern Case Study | Alan Akandzhi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# Global styling
# ------------------------------------------------------------

load_css()


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------

overview_page = st.Page(
    "pages/0_Overview.py",
    title="Overview",
    icon=":material/home:",
    default=True,
)

business_analysis_page = st.Page(
    "pages/1_Business_Analysis.py",
    title="Business Analysis",
    icon=":material/analytics:",
)

sql_solutions_page = st.Page(
    "pages/2_SQL_Solutions.py",
    title="SQL Solutions",
    icon=":material/database:",
)

dashboard_page = st.Page(
    "pages/3_Dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
)

data_explorer_page = st.Page(
    "pages/4_Data_Explorer.py",
    title="Data Explorer",
    icon=":material/table_view:",
)

project_notes_page = st.Page(
    "pages/5_Project_Notes.py",
    title="Project Notes",
    icon=":material/description:",
)


# ------------------------------------------------------------
# Navigation structure
# ------------------------------------------------------------

navigation = st.navigation(
    {
        "Overview": [
            overview_page,
        ],
        "Analysis": [
            business_analysis_page,
            sql_solutions_page,
            dashboard_page,
        ],
        "Data": [
            data_explorer_page,
        ],
        "Documentation": [
            project_notes_page,
        ],
    }
)


# ------------------------------------------------------------
# Sidebar branding
# ------------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-mark">BI</div>
            <div>
                <div class="sidebar-brand-title">
                    Business Intelligence
                </div>
                <div class="sidebar-brand-subtitle">
                    Intern Case Study
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-profile">
            <div class="sidebar-profile-name">
                Alan Akandzhi
            </div>
            <div class="sidebar-profile-role">
                BI Intern Candidate
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Run selected page
# ------------------------------------------------------------

navigation.run()