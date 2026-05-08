"""
Audio / dataset statistics components for the BEAGLE dashboard.
"""

import streamlit as st

from components.ui_styles import info_grid, section_header, SECTION_COLORS


def render_audio_stats(stats: dict, total_stats: dict = None) -> None:
    """Render audio statistics with dataset contribution information."""
    if not stats:
        return

    site_recordings = stats.get("total_recordings", 0)
    size_gb = stats.get("total_size_gb", 0)
    date_range = stats.get("date_range", {})
    days_str = "N/A"
    if date_range.get("earliest") and date_range.get("latest"):
        days = (date_range["latest"] - date_range["earliest"]).days
        days_str = f"{days} days"

    site_fields = [
        ("🎙️", "Recordings",  f"{site_recordings:,}"),
        ("💾", "Size",         f"{size_gb:.2f} GB"),
        ("📅", "Date span",    days_str),
    ]

    if total_stats:
        total_recordings = total_stats.get("total_recordings", 0)
        total_size = total_stats.get("total_size_gb", 0)

        rec_share = (
            f"{site_recordings / total_recordings * 100:.2f}%  "
            f"({site_recordings:,} / {total_recordings:,})"
            if total_recordings > 0 else "N/A"
        )
        size_share = (
            f"{size_gb / total_size * 100:.2f}%  "
            f"({size_gb:.2f} / {total_size:.2f} GB)"
            if total_size > 0 else "N/A"
        )
        site_fields += [
            ("📊", "Recordings share", rec_share),
            ("📦", "Size share",       size_share),
            ("🌐", "Total dataset",    f"{total_recordings:,} rec · {total_size:.2f} GB"),
        ]

    info_grid(site_fields)
