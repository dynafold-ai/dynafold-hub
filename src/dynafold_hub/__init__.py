"""DYNAFOLD Hub — Unified platform for open-source AI drug discovery models.

The Hub provides a unified interface to access, compare, and orchestrate
state-of-the-art open-source AI models for drug discovery including:
- AlphaFold 3 (DeepMind)
- Chai-1 / Chai-2 (Chai Discovery)
- Boltz-2 (MIT Wohlwend Lab)
- OpenFold3 (AQ Laboratory)
- Protenix (ByteDance)
- RFdiffusion (Rosetta Commons)
- ProteinMPNN / LigandMPNN
- ESM3 (EvolutionaryScale)
- And many more

Example:
    >>> from dynafold_hub.adapters import Chai1Adapter
    >>> adapter = Chai1Adapter()
    >>> result = adapter.predict_structure(sequence="MGKLSTAA...")
"""

__version__ = "0.1.0"
__author__ = "Sergio León Martínez-Losa"
__license__ = "MIT"
__all__ = ["__version__"]
