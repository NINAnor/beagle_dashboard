"""
Data Overview Dashboard for BEAGLE.
Combines site metadata, recording statistics, activity heatmap, and site images.
"""

import streamlit as st

from components.audio import render_audio_stats
from components.charts import render_activity_heatmap
from components.sidebar import render_complete_sidebar
from components.site_components import render_site_details, render_device_images
from components.ui_styles import load_custom_css, page_banner, section_header, SECTION_COLORS
from services.audio_service import AudioService
from services.data_service import DataService
from services.site_service import SiteService
from utils.utils import extract_device_id


def _render_active_badge(record) -> None:
    """Render site name with active/inactive badge."""
    is_active = bool(record.get("Active", False))
    badge = (
        "<span style='background:#d1fae5;color:#065f46;padding:3px 12px;"
        "border-radius:20px;font-size:0.85em;font-weight:700;'>● Active</span>"
        if is_active else
        "<span style='background:#fee2e2;color:#991b1b;padding:3px 12px;"
        "border-radius:20px;font-size:0.85em;font-weight:700;'>● Inactive</span>"
    )
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.3rem;'>"
        f"<span style='font-size:1.3rem;font-weight:800;color:#1C2B3A;'>"
        f"{record.get('Site', '')}</span>"
        f"<span style='color:#6b8fa3;font-size:0.9rem;'>"
        f"{record.get('Country', '')}</span>"
        f"{badge}</div>",
        unsafe_allow_html=True,
    )


def show_data_overview_dashboard() -> None:
    """Main data overview dashboard function."""
    load_custom_css()

    page_banner(
        "Data Overview",
        "Site details, recording statistics, activity and images",
        SECTION_COLORS["data"],
        "📊",
    )

    # Initialize services
    data_service = DataService()
    audio_service = AudioService()
    site_service = SiteService()

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

    # ── Shared site selector ─────────────────────────────────────────────────
    section_header("Site selection", SECTION_COLORS["data"], "🌍")
    sel_col1, sel_col2 = st.columns(2)
    with sel_col1:
        countries = sorted(site_info["Country"].dropna().unique().tolist())
        selected_country = st.selectbox("Country", countries, key="ov_country")
    filtered_site_info = site_info[site_info["Country"] == selected_country]
    with sel_col1:
        sites = sorted(filtered_site_info["Site"].dropna().unique().tolist())
        selected_site = st.selectbox("Site", sites, key="ov_site")

    site_data = filtered_site_info[filtered_site_info["Site"] == selected_site]
    if site_data.empty:
        st.error(f"No data found for site: {selected_site}")
        return

    record = site_data.iloc[0]

    st.divider()
    _render_active_badge(record)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_details, tab_pictures = st.tabs(
        ["📋 Site Details", "📸 Pictures"]
    )

    # ── Site details tab ─────────────────────────────────────────────────────
    with tab_details:
        render_site_details(filtered_site_info, selected_site)

        short_device_id = extract_device_id(record)
        if short_device_id:
            with st.spinner("Loading statistics..."):
                total_stats = audio_service.get_total_dataset_stats()
                device_stats = audio_service.get_device_stats(short_device_id)

            if device_stats:
                section_header("Recording statistics", SECTION_COLORS["data"], "📊")
                render_audio_stats(device_stats, total_stats)
            else:
                st.warning(f"No statistics found for device: {short_device_id}")
                if total_stats and total_stats.get("total_recordings", 0) > 0:
                    st.info(
                        f"Total dataset: {total_stats['total_recordings']:,} recordings "
                        f"({total_stats['total_size_gb']:.2f} GB)"
                    )
        else:
            st.warning("No device ID found for this site.")

    # ── Pictures tab ─────────────────────────────────────────────────────────
    with tab_pictures:
        short_device_id = extract_device_id(record)
        if short_device_id:
            with st.spinner("Loading images..."):
                pictures_mapping = site_service.get_image_mapping()
            render_device_images(short_device_id, pictures_mapping)
        else:
            st.info("No device ID found — cannot load images.")

