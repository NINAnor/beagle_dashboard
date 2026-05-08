"""
Data Overview Dashboard for BEAGLE.
Combines per-site audio statistics with network-wide recording activity.
"""

import streamlit as st

from components.audio import (
    render_audio_stats,
    render_site_details,
    render_site_selection,
)
from components.charts import render_activity_heatmap
from components.sidebar import render_complete_sidebar
from components.ui_styles import load_custom_css, page_banner, section_header, SECTION_COLORS
from services.audio_service import AudioService
from services.data_service import DataService
from utils.utils import extract_device_id


def show_data_overview_dashboard() -> None:
    """Main data overview dashboard function."""
    load_custom_css()

    page_banner(
        "Data Overview",
        "Per-site recording statistics and network-wide activity",
        SECTION_COLORS["data"],
        "📊",
    )

    # Initialize services
    data_service = DataService()
    audio_service = AudioService()

    # Load data
    with st.spinner("Loading data..."):
        site_info = data_service.load_site_info()
        device_data = data_service.load_device_status()

    metrics = data_service.calculate_metrics(device_data)

    with st.sidebar:
        render_complete_sidebar(metrics=metrics)

    if site_info.empty:
        st.error("No site information available.")
        return

    tab_site, tab_activity = st.tabs(["📈 Site Statistics", "🌡️ Recording Activity"])

    # ── Site statistics tab ──────────────────────────────────────────────────
    with tab_site:
        col1, col2 = st.columns([1, 2])

        with col1:
            selected_country, selected_site, filtered_site_info = render_site_selection(
                site_info
            )

        site_data = filtered_site_info[filtered_site_info["Site"] == selected_site]

        if site_data.empty:
            st.error(f"No data found for site: {selected_site}")
            return

        record = site_data.iloc[0]

        st.divider()
        section_header(selected_site, SECTION_COLORS["data"], "📍")

        render_site_details(record)

        short_device_id = extract_device_id(record)

        if not short_device_id:
            st.error("No device ID found for this site.")
            return

        with st.spinner("Loading statistics..."):
            total_stats = audio_service.get_total_dataset_stats()
            device_stats = audio_service.get_device_stats(short_device_id)

        if device_stats:
            section_header("Recording statistics", SECTION_COLORS["data"], "📊")
            render_audio_stats(device_stats, total_stats)
        else:
            st.warning(f"No statistics found for device: {short_device_id}")
            if total_stats and total_stats.get("total_recordings", 0) > 0:
                total_recordings = total_stats["total_recordings"]
                total_size_gb = total_stats["total_size_gb"]
                st.info(
                    f"Total dataset: {total_recordings:,} recordings "
                    f"({total_size_gb:.2f} GB)"
                )

    # ── Recording activity tab ───────────────────────────────────────────────
    with tab_activity:
        with st.spinner("Loading activity data..."):
            recording_data = data_service.load_recording_matrix()

        if recording_data.empty:
            st.info("No recording activity data available.")
        else:
            filtered_recording = _filter_activity(recording_data)
            render_activity_heatmap(filtered_recording)


def _filter_activity(recording_data: "pd.DataFrame") -> "pd.DataFrame":
    """
    Render filter controls and return a filtered slice of the recording matrix.
    The recording matrix has a (country, device_id) MultiIndex and date columns.
    """
    import pandas as pd
    from datetime import date
    from components.ui_styles import section_header, SECTION_COLORS

    section_header("Filters", SECTION_COLORS["activity"], "🔍")

    all_countries = sorted(recording_data.index.get_level_values(0).unique().tolist())

    # Parse column dates (columns are date strings e.g. "2025-01-01")
    date_cols = recording_data.columns.tolist()
    parsed_dates = pd.to_datetime(date_cols, errors="coerce")
    valid_mask = ~parsed_dates.isna()
    valid_cols = [c for c, ok in zip(date_cols, valid_mask) if ok]
    valid_dates = parsed_dates[valid_mask]

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        sel_countries = st.multiselect(
            "🌍 Country",
            options=all_countries,
            default=all_countries,
            key="act_country_filter",
        )

    with col2:
        min_date = valid_dates.min().date() if len(valid_dates) else date(2020, 1, 1)
        max_date = valid_dates.max().date() if len(valid_dates) else date.today()
        start_date = st.date_input(
            "📅 From",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="act_date_start",
        )

    with col3:
        end_date = st.date_input(
            "📅 To",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="act_date_end",
        )

    st.markdown("")  # spacing

    # ── Apply country filter ─────────────────────────────────────────────────
    mask_countries = recording_data.index.get_level_values(0).isin(sel_countries)
    filtered = recording_data[mask_countries]

    # ── Apply date range filter ──────────────────────────────────────────────
    if valid_cols:
        keep_cols = [
            c for c, d in zip(valid_cols, valid_dates)
            if start_date <= d.date() <= end_date
        ]
        # Keep any non-date columns too (shouldn't exist but be safe)
        other_cols = [c for c in date_cols if c not in valid_cols]
        filtered = filtered[other_cols + keep_cols]

    if filtered.empty:
        st.warning("No data matches the current filters.")

    return filtered

