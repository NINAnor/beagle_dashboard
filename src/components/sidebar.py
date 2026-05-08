"""
Sidebar components for the BEAGLE dashboard.
"""

import streamlit as st


def render_dashboard_sidebar(metrics: dict = None):
    """Render the compact device status sidebar with visual health bar."""
    if metrics:
        total = metrics.get("total_devices", 0)
        online = metrics.get("online_devices", 0)
        offline = metrics.get("offline_devices", 0)

        if total > 0:
            online_pct = online / total * 100
            offline_pct = offline / total * 100

            # Health bar
            st.markdown(
                f"""
                <div style="margin-bottom:0.6rem;">
                    <div style="font-size:0.72em;font-weight:700;color:#5a7a8a;
                                text-transform:uppercase;letter-spacing:.05em;
                                margin-bottom:0.35rem;">
                        🟢 Network health
                    </div>
                    <div style="background:#e8f4f8;border-radius:20px;height:10px;overflow:hidden;">
                        <div style="background:linear-gradient(90deg,#2DC653,#0A9396);
                                    width:{online_pct:.1f}%;height:100%;
                                    border-radius:20px;transition:width .4s ease;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;
                                font-size:0.75em;margin-top:0.25rem;">
                        <span style="color:#2DC653;font-weight:600;">
                            ● {online} online ({online_pct:.0f}%)
                        </span>
                        <span style="color:#E76F51;font-weight:600;">
                            ● {offline} offline ({offline_pct:.0f}%)
                        </span>
                    </div>
                </div>
                <div style="font-size:0.78em;color:#6b8fa3;
                            background:#e8f4f8;border-radius:8px;
                            padding:0.3rem 0.6rem;display:inline-block;
                            margin-bottom:0.4rem;">
                    📡 {total} devices total
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption("Online = active within 3 days")
    st.divider()


def render_about_section():
    """Render about information in the sidebar."""
    with st.expander("ℹ️ About BEAGLE", expanded=False):
        st.markdown(
            "**BEAGLE** is set to deliver up to 1 billion data points from next-generation biodiversity monitoring across "
            "terrestrial, freshwater, and marine ecosystems in EU Member States and Associated Countries. "
            "using acoustic sensors across Europe.\n\n"
        )


def render_complete_sidebar(metrics: dict = None):
    """Render the complete sidebar with all components."""
    render_dashboard_sidebar(metrics)
    render_about_section()
