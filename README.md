# DYNAFOLD Hub 🧬

> **The unified platform for open-source AI drug discovery models**
>
> Access AlphaFold 3, Chai-1, Chai-2, Boltz-2, RFdiffusion, ProteinMPNN, ESM3 and more — all from one place. Compare predictions across models. Build custom workflows. No infrastructure setup required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Pre-Alpha](https://img.shields.io/badge/status-pre--alpha-orange)](https://github.com/dynafold-ai/dynafold-hub)

---

## 🎯 Why DYNAFOLD Hub?

There are 30+ state-of-the-art open source AI models for drug discovery (AlphaFold 3, Chai-1, Boltz-2, RFdiffusion, ProteinMPNN, ESM3, and many more). Each one requires:

- Reading documentation and setting up environments
- Different input/output formats
- GPU configuration
- Custom code for combining models

**DYNAFOLD Hub solves this**: one unified interface, all models, instant comparison.

## ✨ Features (Roadmap)

### Phase 1 — MVP (current)
- [ ] **Structure Prediction**: AlphaFold 3 vs Chai-1 vs Boltz-2 side-by-side
- [ ] **Consensus Engine**: see where models agree/disagree
- [ ] **3D Visualization**: interactive viewer with confidence overlay
- [ ] **One-click export**: PDB, FASTA, JSON

### Phase 2 — Workflows (months 2-4)
- [ ] **Pre-built workflows**: antibody design, kinase discovery, allosteric sites
- [ ] **REST API**: programmatic access
- [ ] **More models**: OpenFold3, Protenix, RFdiffusion, ProteinMPNN, Chai-2, ESM3
- [ ] **MD validation**: optional physics-based validation

### Phase 3 — Platform (months 5-12)
- [ ] **Cloud GPU**: no infrastructure needed
- [ ] **Workflow marketplace**: community-contributed pipelines
- [ ] **Enterprise**: private deployments, custom models

---

## 🚀 Quick Start

> **Note**: Project is in early development. Quick start coming in Phase 1.

```bash
# Coming soon
pip install dynafold-hub
dynafold-hub launch
```

---

## 📊 Why us?

### vs Schrödinger
- ✅ Free and open source (vs $50-200K/year licenses)
- ✅ Modern AI-first (vs legacy molecular mechanics)
- ✅ Model-agnostic (vs Schrödinger-only stack)

### vs DIY scripts
- ✅ Save 4-8 hours per analysis
- ✅ Best practices automated
- ✅ Multiple models integrated effortlessly

### vs Each individual model
- ✅ Unified interface
- ✅ Cross-model consensus
- ✅ Built-in benchmarking

---

## 🛠️ Built on these amazing open source models

We don't build models — we make them accessible. Thanks to:

- [AlphaFold](https://github.com/google-deepmind/alphafold) by DeepMind
- [Chai-1 / Chai-2](https://github.com/chaidiscovery/chai-lab) by Chai Discovery
- [Boltz-2](https://github.com/jwohlwend/boltz) by MIT Wohlwend Lab
- [OpenFold3](https://github.com/aqlaboratory/openfold) by AQ Laboratory
- [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion) by Rosetta Commons
- [ProteinMPNN / LigandMPNN](https://github.com/dauparas/ProteinMPNN) by Justas Dauparas
- [ESM3](https://github.com/evolutionaryscale/esm) by EvolutionaryScale
- And many more in our [adapters](src/dynafold_hub/adapters/) directory

---

## 📖 Documentation

- [Quickstart Guide](docs/quickstart.md) — coming soon
- [Architecture Overview](docs/architecture.md) — coming soon
- [Add Your Own Model](docs/adapters/contributing.md) — coming soon
- [API Reference](docs/api.md) — coming soon

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- Adding new model adapters
- Creating workflows for your favorite use case
- Improving documentation
- Reporting bugs

See [CONTRIBUTING.md](CONTRIBUTING.md) for details (coming soon).

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 💬 Community

- 🐦 Twitter: [@dynafold_ai](https://twitter.com/dynafold_ai) — coming soon
- 💼 LinkedIn: [DYNAFOLD](https://linkedin.com/company/dynafold-ai) — coming soon
- 🌐 Website: [dynafold.io](https://dynafold.io) — coming soon
- 💬 Discord: coming soon

---

## ⚡ Why this matters

The future of drug discovery is AI-driven. But that AI is fragmented across dozens of independent models, each requiring specialized knowledge to use.

**DYNAFOLD Hub democratizes access** to this fragmented ecosystem, so any researcher — not just those at well-funded labs — can leverage the best AI models for their drug discovery work.

We believe **better tools → faster drug discovery → better medicines for everyone.**

---

*Built with ❤️ for the open science community*
