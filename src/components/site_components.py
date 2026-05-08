import io

import pandas as pd
import requests
import streamlit as st
from PIL import Image

from components.ui_styles import info_grid, section_header, SECTION_COLORS


def render_site_filters(site_info: pd.DataFrame) -> tuple:
    """Render country and site selection filters."""
    section_header("Site selection", SECTION_COLORS["site"], "🌍")

    # Country filter
    countries = site_info["Country"].dropna().unique().tolist()
    selected_country = st.selectbox(
        "Country", sorted(countries), key="site_country_filter"
    )

    # Filter by country
    filtered_site_info = site_info[site_info["Country"] == selected_country]

    # Site filter
    sites = filtered_site_info["Site"].dropna().unique().tolist()
    selected_site = st.selectbox("Site", sorted(sites), key="site_site_filter")

    return selected_country, selected_site, filtered_site_info


def render_site_details(filtered_data: pd.DataFrame, selected_site: str) -> None:
    """Render detailed site information as icon-labelled info cards."""
    site_data = filtered_data[filtered_data["Site"] == selected_site]

    if site_data.empty:
        st.error(f"No data found for site: {selected_site}")
        return

    r = site_data.iloc[0]

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        section_header("Location & device", SECTION_COLORS["site"], "📍")

        col1, col2, col3 = st.columns(3)

        with col1: 
            info_grid([
                ("🌍", "Country",      str(r.get("Country", "N/A"))),
                ("🏞️", "Site",         str(r.get("Site", "N/A"))),
            ])

        with col2:
            info_grid([
                ("📡", "Device ID",    str(r.get("DeviceID", "N/A"))),
                ("🔖", "Deployment",   str(r.get("DeploymentID", "N/A"))),
            ])

        with col3: 
            info_grid([
                ("🗂️", "Cluster",      str(r.get("Cluster", "N/A"))),
                ("🌿", "Habitat",      str(r.get("12. Habitat", "N/A"))) 
            ])


        section_header("Deployment timeline", SECTION_COLORS["site"], "⏰")
        begin = f"{r.get('deploymentBeginDate','N/A')} {r.get('deploymentBeginTime','')}".strip()
        end   = f"{r.get('deploymentEndDate','N/A')} {r.get('deploymentEndTime','')}".strip()
        info_grid([
            ("▶️", "Start", begin),
            ("⏹️", "End",   end),
        ])

    with col_right:
        section_header("Microphone & GPS", SECTION_COLORS["site"], "🎙️")
        info_grid([
            ("📏", "Mic height",    f"{r.get('Microphone_height', 'N/A')} cm"),
            ("🧭", "Mic direction", str(r.get("Microphone_direction", "N/A"))),
            ("📍", "Coord. uncertainty", f"{r.get('Coordinates_uncertainty', 'N/A')} m"),
            ("🛰️", "GPS device",   str(r.get("GPS_device", "N/A"))),
            ("⭐", "Quality score", str(r.get("Score", "N/A"))),
        ])

        email    = r.get("Adresse e-mail", "N/A")
        comments = r.get("Comments", "N/A")
        extra = []
        if email not in ("N/A", None, ""):
            extra.append(("✉️", "Contact", str(email)))
        if comments not in ("N/A", None, ""):
            extra.append(("💬", "Comments", str(comments)))
        if extra:
            section_header("Additional information", SECTION_COLORS["site"], "📝")
            info_grid(extra)


@st.cache_data
def download_image(url):
    # TODO: create a thumbnail for faster loading
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    image = Image.open(io.BytesIO(response.content))

    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(image.getdata())
    return image_without_exif


def render_image_grid(images_df: pd.DataFrame) -> None:
    """Render images in a responsive grid layout."""
    cols_per_row = 2

    for i in range(0, len(images_df), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, (_, row) in enumerate(images_df.iloc[i : i + cols_per_row].iterrows()):
            with cols[j]:
                try:
                    # Get the original URL (already has /data/ prefix)

                    st.image(
                        download_image(row["url"]),
                        caption=row["picture_type"].title(),
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"Error loading image: {str(e)}")
                    # Fallback to broken link message
                    st.markdown(f"**{row['picture_type'].title()}**: Image unavailable")


def render_device_images(device_id: str, pictures_mapping: pd.DataFrame) -> None:
    """Render device images if available."""
    if pictures_mapping.empty:
        st.info("📸 No device images available for this site.")
        return

    section_header("Device Images", SECTION_COLORS["site"], "📸")
    # Check if deviceID column exists and filter accordingly
    if "deviceID" in pictures_mapping.columns:
        device_images = pictures_mapping[pictures_mapping["deviceID"] == device_id]
    else:
        st.info("📸 Device image mapping not available.")
        return

    if device_images.empty:
        st.info(f"📸 No images found for device {device_id}")
        return

    # Render images in a grid
    render_image_grid(device_images)
