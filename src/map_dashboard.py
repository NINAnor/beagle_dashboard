"""
BEAGLE Device Status Dashboard.
"""

import pandas as pd
import streamlit as st

from components.charts import (
    render_country_bar_chart,
    render_activity_heatmap,
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
    tab1, tab2, tab3 = st.tabs(
        [
            f"{TAB_ICONS['map']} Map View",
            f"{TAB_ICONS['status']} Device Status",
            f"{TAB_ICONS['activity']} Recording Activity",
        ]
    )

    with tab1:
        render_map_tab(device_data, data_service)

    with tab2:
        render_status_tab(device_data, metrics, data_service)

    with tab3:
        render_activity_tab(data_service)

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


def render_activity_tab(data_service: DataService):
    """Render the recording activity heatmap tab."""
    with st.spinner("Loading activity data..."):
        recording_data = data_service.load_recording_matrix()

    if recording_data.empty:
        st.info("No recording activity data available.")
        return

    filtered_recording = _filter_activity(recording_data)
    render_activity_heatmap(filtered_recording)


def _filter_activity(recording_data: pd.DataFrame) -> pd.DataFrame:
    """
    Render filter controls and return a filtered slice of the recording matrix.
    The recording matrix has a (country, device_id) MultiIndex and date columns.
    """
    from datetime import date

    section_header("Filters", SECTION_COLORS["activity"], "\U0001f50d")

    all_countries = sorted(recording_data.index.get_level_values(0).unique().tolist())

    date_cols = recording_data.columns.tolist()
    parsed_dates = pd.to_datetime(date_cols, errors="coerce")
    valid_mask = ~parsed_dates.isna()
    valid_cols = [c for c, ok in zip(date_cols, valid_mask) if ok]
    valid_dates = parsed_dates[valid_mask]

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        sel_countries = st.multiselect(
            "\U0001f30d Country",
            options=all_countries,
            default=all_countries,
            key="act_country_filter",
        )

    with col2:
        min_date = valid_dates.min().date() if len(valid_dates) else date(2020, 1, 1)
        max_date = valid_dates.max().date() if len(valid_dates) else date.today()
        start_date = st.date_input(
            "\U0001f4c5 From",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="act_date_start",
        )

    with col3:
        end_date = st.date_input(
            "\U0001f4c5 To",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="act_date_end",
        )

    st.markdown("")  # spacing

    mask_countries = recording_data.index.get_level_values(0).isin(sel_countries)
    filtered = recording_data[mask_countries]

    if valid_cols:
        keep_cols = [
            c for c, d in zip(valid_cols, valid_dates)
            if start_date <= d.date() <= end_date
        ]
        other_cols = [c for c in date_cols if c not in valid_cols]
        filtered = filtered[other_cols + keep_cols]

    if filtered.empty:
        st.warning("No data matches the current filters.")

    return filtered


if __name__ == "__main__":
    app()
