"""Consensus Analyzer page — the core product of DYNAFOLD Hub.

Upload 2+ structure predictions (PDB/CIF) from different AI models.
Get back: Trust Score, divergent regions, experimental recommendations.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dynafold_hub.orchestration import ConsensusEngine
from dynafold_hub.utils import load_prediction_from_file

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Consensus Analyzer — DYNAFOLD Hub",
    page_icon="🔬",
    layout="wide",
)

st.markdown("# 🔬 Consensus Analyzer")
st.markdown(
    "Compare structure predictions from 2+ AI models. "
    "**Find consensus. Identify divergence. Get experimental recommendations.**"
)

# ─────────────────────────────────────────────
# How it works (collapsible)
# ─────────────────────────────────────────────
with st.expander("ℹ️ How it works", expanded=False):
    st.markdown("""
        1. **Upload** 2 or more structure files (PDB or CIF format) from
           different AI models predicting the SAME protein.
        2. **Name** each model (e.g., "AlphaFold 3", "Chai-1", "Boltz-2").
        3. **Analyze**: DYNAFOLD computes per-residue agreement, identifies
           divergent regions, and recommends specific experiments.

        ### Where to get predictions
        - **AlphaFold 3**: [alphafoldserver.com](https://alphafoldserver.com) (free, web UI)
        - **Chai-1**: [tamarind.bio/tools/chai-1](https://tamarind.bio/tools/chai-1)
        - **Boltz**: [tamarind.bio/tools/boltz](https://tamarind.bio/tools/boltz)

        ### What you get back
        - **Trust Score (0-100)**: overall confidence in the consensus
        - **Agreement fraction**: % of residues where all models agree
        - **Divergent regions**: residues where models disagree (with severity)
        - **Experimental recommendations**: specific wet-lab experiments
          to validate disagreements
        """)

# ─────────────────────────────────────────────
# Demo data option
# ─────────────────────────────────────────────
demo_col, real_col = st.columns([1, 2])

with demo_col:
    use_demo = st.checkbox(
        "Use demo data (no upload needed)",
        value=False,
        help="Use 3 example predictions to see how the tool works",
    )

with real_col:
    if use_demo:
        st.info(
            "Using synthetic demo data: 3 predictions of a 20-residue peptide "
            "with one divergent loop region."
        )

# ─────────────────────────────────────────────
# File upload section
# ─────────────────────────────────────────────
predictions_data: list[dict] = []

if use_demo:
    # Load demo files from examples directory
    demo_dir = Path(__file__).parent.parent.parent.parent.parent / "examples" / "01_consensus_demo"
    if not demo_dir.exists():
        st.error(
            f"Demo data not found at {demo_dir}. "
            "Run `python examples/01_consensus_demo/generate_example_data.py` first."
        )
        st.stop()

    demo_files = [
        (demo_dir / "af3.pdb", "AlphaFold 3"),
        (demo_dir / "chai1.pdb", "Chai-1"),
        (demo_dir / "boltz2.pdb", "Boltz-2"),
    ]
    for path, name in demo_files:
        predictions_data.append({"path": path, "name": name})

else:
    st.markdown("### 📤 Upload Predictions")
    st.markdown("Upload **2 or more** PDB/CIF files from different models:")

    uploaded_files = st.file_uploader(
        "Select structure files",
        type=["pdb", "cif", "mmcif"],
        accept_multiple_files=True,
        help="Drag and drop or click to browse. Each file = one model's prediction.",
    )

    if uploaded_files:
        st.markdown(f"#### Loaded {len(uploaded_files)} file(s):")
        for i, uf in enumerate(uploaded_files):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.text(f"📄 {uf.name}")
            with col2:
                model_name = st.text_input(
                    f"Model name for {uf.name}",
                    value=Path(uf.name).stem,
                    key=f"model_name_{i}",
                    label_visibility="collapsed",
                    placeholder="e.g., AlphaFold 3, Chai-1, Boltz-2",
                )

            # Save uploaded file to temp dir to use existing loader
            tmp_dir = Path(tempfile.gettempdir()) / "dynafold_uploads"
            tmp_dir.mkdir(exist_ok=True)
            tmp_path = tmp_dir / uf.name
            tmp_path.write_bytes(uf.getbuffer())

            predictions_data.append({"path": tmp_path, "name": model_name})

# ─────────────────────────────────────────────
# Run analysis
# ─────────────────────────────────────────────
st.markdown("---")

can_run = len(predictions_data) >= 2

if not can_run:
    st.warning("👆 Upload at least 2 structure files (or use demo data) to run analysis.")
    st.stop()

if not st.button("🚀 Run Consensus Analysis", type="primary", use_container_width=True):
    st.stop()

# ─────────────────────────────────────────────
# Load + analyze
# ─────────────────────────────────────────────
with st.spinner("Loading predictions..."):
    predictions = []
    for p in predictions_data:
        try:
            pred = load_prediction_from_file(p["path"], model_name=p["name"])
            predictions.append(pred)
        except Exception as e:
            st.error(f"Failed to load {p['name']}: {e}")
            st.stop()

with st.spinner("Computing consensus..."):
    try:
        engine = ConsensusEngine()
        result = engine.compare(predictions)
    except ValueError as e:
        st.error(f"Consensus failed: {e}")
        st.stop()

# ─────────────────────────────────────────────
# Display results
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📊 Results")

# Trust Score - prominent
trust_color = (
    "#22c55e" if result.trust_score > 80 else "#eab308" if result.trust_score > 50 else "#ef4444"
)
trust_label = (
    "HIGH TRUST"
    if result.trust_score > 80
    else "MODERATE" if result.trust_score > 50 else "LOW TRUST"
)
trust_emoji = "✓" if result.trust_score > 80 else "⚠" if result.trust_score > 50 else "✗"

st.markdown(
    f"""
    <div style='
        background: linear-gradient(135deg, {trust_color}22 0%, {trust_color}11 100%);
        border-left: 6px solid {trust_color};
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    '>
        <div style='font-size: 0.9rem; color: #888;'>TRUST SCORE</div>
        <div style='font-size: 3.5rem; font-weight: bold; color: {trust_color};'>
            {trust_emoji} {result.trust_score:.1f}/100
        </div>
        <div style='font-size: 1rem; color: {trust_color}; font-weight: bold;'>
            {trust_label}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Key metrics row
metric_cols = st.columns(4)
metric_cols[0].metric(
    "Models compared",
    len(result.models_compared),
    help="Number of AI models in this comparison",
)
metric_cols[1].metric(
    "Residues",
    result.n_residues,
    help="Number of residues analyzed",
)
metric_cols[2].metric(
    "Global RMSD",
    f"{result.global_rmsd:.2f} Å",
    help="Mean displacement between models (lower = better agreement)",
)
metric_cols[3].metric(
    "Agreement",
    f"{result.agreement_fraction * 100:.1f}%",
    help="% of residues where models agree (RMSD < 2 Å)",
)

st.caption(f"Models: {', '.join(result.models_compared)}")

# ─────────────────────────────────────────────
# Per-residue RMSD plot
# ─────────────────────────────────────────────
st.markdown("### 📈 Per-Residue Agreement")

residue_ids = np.arange(1, result.n_residues + 1)

fig = go.Figure()

# RMSD bars colored by severity
colors = []
for rmsd in result.per_residue_rmsd:
    if rmsd > 6.0:
        colors.append("#ef4444")  # critical red
    elif rmsd > 4.0:
        colors.append("#f97316")  # moderate orange
    elif rmsd > 2.0:
        colors.append("#eab308")  # minor yellow
    else:
        colors.append("#22c55e")  # agreement green

fig.add_trace(
    go.Bar(
        x=residue_ids,
        y=result.per_residue_rmsd,
        marker_color=colors,
        name="RMSD (Å)",
        hovertemplate="Residue %{x}<br>RMSD: %{y:.2f} Å<extra></extra>",
    )
)

# Threshold lines
fig.add_hline(
    y=2.0,
    line_dash="dash",
    line_color="#eab308",
    annotation_text="Agreement threshold (2 Å)",
    annotation_position="top right",
)
fig.add_hline(
    y=6.0,
    line_dash="dash",
    line_color="#ef4444",
    annotation_text="Critical threshold (6 Å)",
    annotation_position="bottom right",
)

fig.update_layout(
    xaxis_title="Residue Position",
    yaxis_title="Inter-Model RMSD (Å)",
    height=400,
    margin={"l": 20, "r": 20, "t": 30, "b": 20},
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# Divergent regions table
# ─────────────────────────────────────────────
if result.divergent_regions:
    st.markdown(f"### ⚠️ {len(result.divergent_regions)} Divergent Region(s)")
    st.caption("Regions where models disagree — sorted by severity")

    regions_data = []
    for region in result.divergent_regions:
        start, end = region.residue_range
        regions_data.append(
            {
                "Residues": f"{start} – {end}",
                "Size": end - start + 1,
                "Severity": region.severity.upper(),
                "Max Displacement": f"{region.max_displacement_angstroms:.2f} Å",
                "Mean Confidence": f"{region.mean_confidence:.1f}",
            }
        )

    df = pd.DataFrame(regions_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Severity": st.column_config.TextColumn(
                "Severity",
                help="critical >6 Å, moderate 4-6 Å, minor 2-4 Å",
            ),
        },
    )
else:
    st.success("✅ All models agree across all residues. No divergent regions detected.")

# ─────────────────────────────────────────────
# Recommendations
# ─────────────────────────────────────────────
st.markdown("### 🧪 Experimental Recommendations")

if not result.recommendations:
    st.info("No specific recommendations needed.")
else:
    for rec in result.recommendations:
        if rec.startswith("[CRITICAL]"):
            st.error(rec)
        elif rec.startswith("[MODERATE]"):
            st.warning(rec)
        elif rec.startswith("[MINOR]"):
            st.info(rec)
        elif rec.startswith("⚠"):
            st.error(rec)
        elif rec.startswith("✓"):
            st.success(rec)
        else:
            st.write(rec)

# ─────────────────────────────────────────────
# Download results
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Export Results")

# Build JSON report
report = {
    "models_compared": result.models_compared,
    "n_residues": result.n_residues,
    "global_rmsd_angstroms": result.global_rmsd,
    "agreement_fraction": result.agreement_fraction,
    "trust_score": result.trust_score,
    "divergent_regions": [
        {
            "residue_range": list(r.residue_range),
            "severity": r.severity,
            "max_displacement_angstroms": r.max_displacement_angstroms,
            "mean_confidence": r.mean_confidence,
        }
        for r in result.divergent_regions
    ],
    "per_residue_rmsd": result.per_residue_rmsd.tolist(),
    "recommendations": result.recommendations,
}

st.download_button(
    "📥 Download report (JSON)",
    data=json.dumps(report, indent=2),
    file_name="dynafold_consensus_report.json",
    mime="application/json",
)
