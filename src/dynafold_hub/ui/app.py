"""DYNAFOLD Hub — Streamlit Web Application.

Main entry point for the web UI. Launches a multi-page Streamlit app.

Run locally:
    poetry run streamlit run src/dynafold_hub/ui/app.py
Or:
    poetry run dynafold launch-ui
"""

from __future__ import annotations

import streamlit as st

from dynafold_hub import __version__

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DYNAFOLD Hub",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/dynafold-ai/dynafold-hub",
        "Report a bug": "https://github.com/dynafold-ai/dynafold-hub/issues",
        "About": (
            "**DYNAFOLD Hub** — Unified platform for open-source " "AI drug discovery models."
        ),
    },
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .trust-score-high { color: #22c55e; font-weight: bold; }
    .trust-score-medium { color: #eab308; font-weight: bold; }
    .trust-score-low { color: #ef4444; font-weight: bold; }
    div[data-testid="stMetricValue"] { font-size: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🧬 DYNAFOLD Hub")
    st.caption(f"v{__version__} · pre-alpha")
    st.markdown("---")

    st.markdown("""
        **The unified platform for AI drug discovery models.**

        Access AlphaFold 3, Chai-1, Boltz-2, RFdiffusion, ProteinMPNN
        and more — all from one place.
        """)
    st.markdown("---")

    st.markdown("### 🔗 Links")
    st.markdown(
        "- [GitHub](https://github.com/dynafold-ai/dynafold-hub)\n"
        "- [Documentation](https://github.com/dynafold-ai/dynafold-hub#readme)\n"
        "- [Report issue](https://github.com/dynafold-ai/dynafold-hub/issues)"
    )

# ─────────────────────────────────────────────
# Main content (landing page)
# ─────────────────────────────────────────────
st.markdown('<p class="main-header">DYNAFOLD Hub</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Compare AI model predictions. Find consensus. '
    "Design experiments. All from one place.</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Value proposition
# ─────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        ### 🤝 Multi-Model Consensus
        Upload predictions from AlphaFold 3,
        Chai-1, Boltz-2 and others. See instantly
        where they agree and where they disagree.
        """)

with col2:
    st.markdown("""
        ### 🎯 Trust Score
        Get a single 0-100 score showing how
        much to trust your prediction. Combines
        model agreement + confidence.
        """)

with col3:
    st.markdown("""
        ### 🧪 Experimental Recommendations
        Automatically recommend specific wet-lab
        experiments to validate predictions where
        models disagree.
        """)

st.markdown("---")

# ─────────────────────────────────────────────
# Quick start
# ─────────────────────────────────────────────
st.markdown("## 🚀 Get started")

quick_start_col1, quick_start_col2 = st.columns([2, 1])

with quick_start_col1:
    st.markdown("""
        ### Try the Consensus Analyzer

        Have predictions from multiple AI models? Upload them and get instant
        cross-model analysis with experimental recommendations.

        👈 **Open "Consensus Analyzer" from the sidebar** to start.
        """)

with quick_start_col2:
    st.info(
        "**Don't have predictions yet?**\n\n"
        "Generate some using:\n"
        "- [AlphaFold Server](https://alphafoldserver.com) (free)\n"
        "- [Chai Discovery](https://tamarind.bio/tools/chai-1)\n"
        "- [Boltz](https://tamarind.bio/tools/boltz)\n\n"
        "Download as PDB/CIF, then upload here."
    )

# ─────────────────────────────────────────────
# Supported models
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🤖 Supported Models")

models_data = [
    {
        "name": "AlphaFold 3",
        "org": "Google DeepMind",
        "license": "Free non-commercial",
        "status": "🟢 Web UI",
    },
    {
        "name": "Chai-1",
        "org": "Chai Discovery",
        "license": "Apache 2.0",
        "status": "🟡 Coming soon",
    },
    {
        "name": "Chai-2",
        "org": "Chai Discovery",
        "license": "Apache 2.0",
        "status": "🟡 Coming soon",
    },
    {"name": "Boltz-2", "org": "MIT Wohlwend Lab", "license": "MIT", "status": "🟡 Coming soon"},
    {"name": "OpenFold3", "org": "AQ Laboratory", "license": "Apache 2.0", "status": "⏳ Planned"},
    {"name": "Protenix", "org": "ByteDance", "license": "Apache 2.0", "status": "⏳ Planned"},
    {"name": "RFdiffusion", "org": "Rosetta Commons", "license": "BSD-3", "status": "⏳ Planned"},
    {"name": "ProteinMPNN", "org": "Justas Dauparas", "license": "MIT", "status": "⏳ Planned"},
    {"name": "ESM3", "org": "EvolutionaryScale", "license": "Mixed", "status": "⏳ Planned"},
]

st.dataframe(
    models_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "name": st.column_config.TextColumn("Model", width="medium"),
        "org": st.column_config.TextColumn("Organization", width="medium"),
        "license": st.column_config.TextColumn("License", width="medium"),
        "status": st.column_config.TextColumn("Status", width="small"),
    },
)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
    Built with ❤️ for the open science community ·
    <a href='https://github.com/dynafold-ai/dynafold-hub'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)
