"""
BEAGLE Dashboard Application
"""

from pathlib import Path

import streamlit as st

from config.settings import APP_TITLE
from data_overview_dashboard import show_data_overview_dashboard
from map_dashboard import app as map_app
from site_dashboard import show_site_dashboard
from components.ui_styles import load_custom_css, SECTION_COLORS


def main():
    """Main application entry point."""

    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]

    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="⛵",
    )
    load_custom_css()

    # Logo — fall back gracefully if no image present
    logo_path = Path("/app/src/images/beagle_logo.png")
    if logo_path.exists():
        st.sidebar.image(logo_path, width=260)

    st.sidebar.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0A9396 0%, #005F73 100%);
            border-radius: 10px;
            padding: 0.7rem 1rem;
            margin-bottom: 0.4rem;
        ">
            <div style="font-size:1.25rem;font-weight:800;color:white;">⛵ BEAGLE</div>
            <div style="font-size:0.76rem;color:rgba(255,255,255,0.8);">
                BIODIVERSITY METHODS FOR ADVANCED MONITORING AT LARGE SCALES
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    NAV_ITEMS = {
        "🗺️ Device status":  ("Device status",  SECTION_COLORS["map"]),
        "📊 Data overview":  ("Data overview",   SECTION_COLORS["data"]),
        "🏞️ Site metadata":  ("Site metadata",   SECTION_COLORS["site"]),
    }

    selected_label = st.sidebar.radio(
        "Navigate",
        list(NAV_ITEMS.keys()),
        index=0,
        label_visibility="collapsed",
    )
    option = NAV_ITEMS[selected_label][0]

    st.sidebar.divider()
    st.sidebar.caption(
        "🗺️ **Device status** — map & device health\n\n"
        "📊 **Data overview** — recordings & activity\n\n"
        "🏞️ **Site metadata** — site details & images"
    )

    if option == "Device status":
        map_app()
    elif option == "Data overview":
        show_data_overview_dashboard()
    elif option == "Site metadata":
        show_site_dashboard()


if __name__ == "__main__":
    main()
