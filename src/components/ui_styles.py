"""
UI styling and custom CSS for the BEAGLE dashboard.
"""

import streamlit as st

# Per-section accent colors
SECTION_COLORS = {
    "map":      "#0A9396",   # teal
    "status":   "#2DC653",   # green
    "data":     "#5E60CE",   # indigo
    "site":     "#F4A261",   # amber
    "activity": "#48CAE4",   # sky blue
}


def page_banner(title: str, subtitle: str, color: str = "#0A9396", icon: str = "") -> None:
    """Full-width gradient page banner with title and subtitle."""
    dark = _darken(color)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color} 0%, {dark} 100%);
            padding: 1.1rem 1.6rem;
            border-radius: 12px;
            margin-bottom: 1.2rem;
            box-shadow: 0 3px 12px {color}55;
        ">
            <div style="font-size:1.55rem; font-weight:800; color:white; letter-spacing:-0.01em;">
                {icon + ' ' if icon else ''}{title}
            </div>
            <div style="font-size:0.88rem; color:rgba(255,255,255,0.82); margin-top:0.2rem;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, color: str = "#0A9396", icon: str = "") -> None:
    """Colored left-border section header."""
    st.markdown(
        f"""
        <div style="
            border-left: 5px solid {color};
            background: {color}18;
            padding: 0.55rem 1rem;
            border-radius: 0 8px 8px 0;
            margin: 0.9rem 0 0.7rem 0;
        ">
            <span style="font-size:1.0rem; font-weight:700; color:{color};">
                {icon + ' &nbsp;' if icon else ''}{title}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_grid(fields: list[tuple[str, str, str]]) -> None:
    """
    Render a responsive grid of info chips.
    fields: list of (icon, label, value) tuples
    """
    cards_html = ""
    for icon, label, value in fields:
        cards_html += f"""
        <div style="
            background:white;
            border-radius:10px;
            padding:0.65rem 0.9rem;
            border-left:4px solid #0A9396;
            box-shadow:0 1px 5px rgba(0,0,0,0.07);
            flex:1 1 180px;
        ">
            <div style="font-size:0.72em;color:#6b8fa3;font-weight:600;
                        text-transform:uppercase;letter-spacing:.05em;">
                {icon} {label}
            </div>
            <div style="font-size:1.0em;font-weight:700;color:#1C2B3A;margin-top:.25rem;">
                {value if value not in (None, 'N/A', '', 'nan') else '—'}
            </div>
        </div>"""
    st.markdown(
        f"<div style='display:flex;flex-wrap:wrap;gap:0.6rem;margin:0.5rem 0 0.8rem 0;'>"
        f"{cards_html}</div>",
        unsafe_allow_html=True,
    )


def _darken(hex_color: str) -> str:
    """Return a ~25% darker version of a hex color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r, g, b = max(0, int(r * 0.72)), max(0, int(g * 0.72)), max(0, int(b * 0.72))
    return f"#{r:02x}{g:02x}{b:02x}"


def load_custom_css():
    """Load custom CSS styles for the dashboard."""
    st.markdown(
        """
    <style>
    /* ── Page ───────────────────────────────────────────────────── */
    .main > div { padding-top: 1.2rem; }

    /* ── Tabs ───────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }

    .stTabs [data-baseweb="tab"] {
        height: 38px;
        padding: 0 18px;
        border-radius: 8px;
        background-color: #e8f4f8;
        border: none;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0A9396 0%, #005F73 100%);
        color: white !important;
        box-shadow: 0 2px 8px rgba(10, 147, 150, 0.35);
    }

    /* ── Native metric containers ───────────────────────────────── */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        border-left: 4px solid #0A9396;
        box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    }

    [data-testid="metric-container"] > div:first-child {
        color: #5a7a8a;
        font-size: 0.78em;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* ── Status metric cards ─────────────────────────────────────── */
    .beagle-card {
        border-radius: 12px;
        padding: 1rem 1.4rem;
        color: white;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 0.2rem;
    }

    .beagle-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.16);
    }

    .beagle-card .card-label {
        font-size: 0.75em;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        opacity: 0.85;
        margin: 0 0 0.25rem 0;
    }

    .beagle-card .card-value {
        font-size: 2.1em;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }

    .beagle-card .card-sub {
        font-size: 0.8em;
        margin: 0.3rem 0 0 0;
        opacity: 0.82;
    }

    .card-total  { background: linear-gradient(135deg, #0A9396 0%, #005F73 100%); }
    .card-online { background: linear-gradient(135deg, #2DC653 0%, #1B7A30 100%); }
    .card-offline{ background: linear-gradient(135deg, #E76F51 0%, #9B2226 100%); }

    /* ── Filter container ────────────────────────────────────────── */
    .filter-box {
        background: #f0f8ff;
        border: 1px solid #c8e6f0;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
    }

    /* ── Selectbox / multiselect focus ──────────────────────────── */
    .stMultiSelect [data-baseweb="select"] > div:first-child,
    .stSelectbox [data-baseweb="select"] > div:first-child {
        border-radius: 8px !important;
        border-color: #b2d8e8 !important;
    }

    /* ── Alerts ─────────────────────────────────────────────────── */
    .stAlert > div { border-radius: 8px; }

    /* ── Sidebar ────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8F4F8 0%, #F8FAFB 100%);
        border-right: 1px solid #d0e8ef;
    }

    /* ── Radio nav items (sidebar) ──────────────────────────────── */
    .stRadio [data-testid="stMarkdownContainer"] p { font-weight: 500; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_info_section_header(
    title: str, level: str = "h3", style_class: str = "section-info"
):
    """Legacy shim — delegates to section_header."""
    section_header(title)
