---
title: DYNAFOLD Hub
emoji: 🧬
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.58.0
app_file: streamlit_app.py
pinned: true
license: mit
short_description: Compare AI drug discovery model predictions (AF3, Chai, Boltz)
tags:
  - drug-discovery
  - alphafold
  - chai-1
  - boltz-2
  - protein-structure
  - bioinformatics
---

# DYNAFOLD Hub 🧬

**The unified platform for open-source AI drug discovery models.**

Compare predictions from AlphaFold 3, Chai-1, Boltz-2 and more. Get instant
cross-model consensus analysis with experimental recommendations.

## What is this?

Just upload 2+ structure predictions (PDB/CIF) from different AI models and get:

- **Trust Score (0-100)**: how much to trust the consensus
- **Divergent regions**: where models disagree
- **Experimental recommendations**: specific wet-lab experiments to validate

## Try the demo

Open the **Consensus Analyzer** in the sidebar and toggle "Use demo data" — no upload needed.

## More info

- 🌐 GitHub: [dynafold-ai/dynafold-hub](https://github.com/dynafold-ai/dynafold-hub)
- 📜 License: MIT
- 🛠️ Built with [Streamlit](https://streamlit.io) + [py3Dmol](https://github.com/avirshup/py3Dmol)
