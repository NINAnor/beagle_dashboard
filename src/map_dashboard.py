"""
BEAGLE Device Status Dashboard.
"""

import pandas as pd
import streamlit as st

from components.charts import (
    render_country_bar_chart,
)
from components.filters import render_complete_filters
from components.map_viz import render_device_map
from components.metrics import render_status_metrics
from components.sidebar import render_complete_sidebar
from components.tables import render_status_table, render_summary_table
from components.ui_styles import (
    load_custom_css,
    page_banner,
    section_header,
    info_grid,
    SECTION_COLORS,
)
from config.settings import TAB_ICONS
from services.data_service import DataService


def app():
    """Main map dashboard application."""
    load_custom_css()

    page_banner(
        "Device Status",
        "Live map and health overview of all BEAGLE recording devices",
        SECTION_COLORS["map"],
        "🗺️",
    )

    # Initialize data service
    data_service = DataService()

    # Load all data
    with st.spinner("Loading device data..."):
        device_data = data_service.load_device_status()

    # Calculate metrics
    metrics = data_service.calculate_metrics(device_data)

    # Render sidebar with controls and metrics
    with st.sidebar:
        render_complete_sidebar(metrics=metrics)

    # Main dashboard tabs
    tab1, tab2 = st.tabs(
        [
            f"{TAB_ICONS['map']} Map View",
            f"{TAB_ICONS['status']} Device Status",
        ]
    )

    with tab1:
        render_map_tab(device_data, data_service)

    with tab2:
        render_status_tab(device_data, metrics, data_service)

    # Footer
    st.caption(
        f"BEAGLE Dashboard · Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"
    )


def render_map_tab(device_data: pd.DataFrame, data_service: DataService):
    """Render the interactive map tab."""

    # Filters for map view
    filtered_data, active_filters = render_complete_filters(
        device_data, key_prefix="map"
    )

    if not filtered_data.empty:
        # Get site info for the map
        site_info = data_service.load_site_info()

        # Render the interactive map
        render_device_map(site_info, filtered_data)

        # Quick stats chips below the map
        online_n = len(filtered_data[filtered_data["status"] == "Online"])
        offline_n = len(filtered_data) - online_n
        countries_n = filtered_data["Country"].nunique()
        sites_n = filtered_data["site_name"].nunique() if "site_name" in filtered_data.columns else 0
        info_grid([
            ("📍", "Devices shown", str(len(filtered_data))),
            ("🟢", "Online",        f"{online_n} ({online_n/len(filtered_data)*100:.0f}%)"),
            ("🔴", "Offline",       f"{offline_n} ({offline_n/len(filtered_data)*100:.0f}%)"),
            ("🌍", "Countries",     str(countries_n)),
            ("🏞️", "Sites",         str(sites_n)),
        ])
    else:
        st.warning("No devices match the current filters.")


def render_status_tab(
    device_data: pd.DataFrame, metrics: dict, data_service: DataService
):
    """Render the device status overview tab."""
    section_header("Fleet health", SECTION_COLORS["status"], "📡")

    # Display status metrics cards
    render_status_metrics(metrics)
    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    # Status visualizations
    section_header("By country", SECTION_COLORS["status"], "🌍")
    render_country_bar_chart(device_data)

    section_header("Device list", SECTION_COLORS["status"], "📋")

    # Filters for status table
    filtered_data, _ = render_complete_filters(device_data, key_prefix="status")

    col1, col2, col3 = st.columns(3)

    with col2:
        sort_by = st.selectbox(
            "Sort by",
            ["device_name", "Country", "status", "last_file", "total_recordings"],
            index=2, 
        )
    with col3:
        ascending = st.checkbox("Ascending order", value=False)

    # Sort and display table
    sorted_data = filtered_data.sort_values(by=sort_by, ascending=ascending)
    render_status_table(sorted_data)

    # Summary statistics
    section_header("Summary", SECTION_COLORS["status"], "📊")
    render_summary_table(filtered_data)


if __name__ == "__main__":
    app()
