"""
Site Dashboard for BEAGLE.
Provides detailed site metadata exploration and device information.
"""

import streamlit as st

from components.sidebar import render_complete_sidebar
from components.site_components import (
    render_device_images,
    render_site_details,
    render_site_filters,
)
from components.ui_styles import load_custom_css, page_banner, section_header, SECTION_COLORS
from services.data_service import DataService
from services.site_service import SiteService
from utils.utils import extract_device_id


def show_site_dashboard() -> None:
    """Main site metadata dashboard function."""
    load_custom_css()

    page_banner(
        "Site Metadata",
        "Explore recording sites, device deployments, and site images",
        SECTION_COLORS["site"],
        "🏞️",
    )

    # Initialize services
    data_service = DataService()
    site_service = SiteService()

    # Load data
    with st.spinner("🔄 Loading site and device information..."):
        site_info = data_service.load_site_info()
        device_data = data_service.load_device_status()

    with st.spinner("🔄 Loading device images..."):
        pictures_mapping = site_service.get_image_mapping()

    # Calculate metrics for the sidebar
    metrics = data_service.calculate_metrics(device_data)

    # Render complete sidebar with status information only
    with st.sidebar:
        render_complete_sidebar(metrics=metrics)

    if site_info.empty:
        st.error("❌ No site information available.")
        return

    # Main site information section
    selected_country, selected_site, filtered_site_info = render_site_filters(site_info)

    # Get site data
    site_data = filtered_site_info[filtered_site_info["Site"] == selected_site]

    if site_data.empty:
        st.error(f"❌ No data found for site: {selected_site}")
        return

    # Get the first (and typically only) record for the site
    record = site_data.iloc[0]

    st.divider()
    is_active = bool(record.get("Active", False))
    active_badge = (
        "<span style='background:#d1fae5;color:#065f46;padding:3px 12px;"
        "border-radius:20px;font-size:0.85em;font-weight:700;'>● Active</span>"
        if is_active else
        "<span style='background:#fee2e2;color:#991b1b;padding:3px 12px;"
        "border-radius:20px;font-size:0.85em;font-weight:700;'>● Inactive</span>"
    )
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:0.3rem;'>"
        f"<span style='font-size:1.3rem;font-weight:800;color:#1C2B3A;'>{selected_site}</span>"
        f"<span style='color:#6b8fa3;font-size:0.9rem;'>{selected_country}</span>"
        f"{active_badge}</div>",
        unsafe_allow_html=True,
    )

    # Render site details (contains its own section headers)
    render_site_details(filtered_site_info, selected_site)

    st.divider()
    # Render device images (contains its own header)
    # Extract short device ID for image matching
    short_device_id = extract_device_id(record)
    render_device_images(short_device_id, pictures_mapping)
