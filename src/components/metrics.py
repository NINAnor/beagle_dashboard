"""
Metrics components for the BEAGLE dashboard.
"""

import streamlit as st


def _card(label: str, value, sub: str, color_class: str) -> str:
    return f"""
    <div class="beagle-card {color_class}">
        <p class="card-label">{label}</p>
        <p class="card-value">{value}</p>
        <p class="card-sub">{sub}</p>
    </div>
    """


def render_status_metrics(metrics: dict):
    """Render coloured status metric cards."""
    if not metrics:
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            _card(
                "Total devices",
                metrics["total_devices"],
                "across all countries",
                "card-total",
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            _card(
                "Online",
                metrics["online_devices"],
                f"{metrics['online_percentage']:.1f}% of fleet",
                "card-online",
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            _card(
                "Offline",
                metrics["offline_devices"],
                f"{metrics['offline_percentage']:.1f}% of fleet",
                "card-offline",
            ),
            unsafe_allow_html=True,
        )

