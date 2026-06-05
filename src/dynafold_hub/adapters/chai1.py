"""Chai-1 adapter.

Chai-1 is an open-source structure prediction model from Chai Discovery,
matching AlphaFold 3 performance on PoseBusters benchmark (77% vs 76%).

Reference: Chai Discovery, 2024
URL: https://github.com/chaidiscovery/chai-lab
License: Apache 2.0 (commercial use allowed)
Install: pip install chai_lab
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    PredictionInput,
    StructurePrediction,
    TaskType,
)


class Chai1Adapter(BaseModelAdapter):
    """Adapter for Chai-1 structure prediction model.

    Chai-1 supports prediction of:
    - Proteins
    - Small molecule ligands
    - DNA / RNA
    - Glycans
    - Multi-chain complexes

    GPU is strongly recommended (CPU inference is very slow).

    Example:
        >>> adapter = Chai1Adapter(device="cuda")
        >>> result = adapter.predict_structure(
        ...     PredictionInput(sequence="MGKLSTAA...")
        ... )
    """

    name = "chai-1"
    supported_tasks = [
        TaskType.STRUCTURE_PREDICTION,
        TaskType.PROTEIN_LIGAND_DOCKING,
    ]
    requires_gpu = False  # Works on CPU but extremely slow

    paper_url = "https://www.biorxiv.org/content/10.1101/2024.10.10.615955"
    code_url = "https://github.com/chaidiscovery/chai-lab"
    license = "Apache 2.0"

    def __init__(
        self,
        device: str = "auto",
        cache_dir: Path | None = None,
        num_diffn_timesteps: int = 200,
        seed: int = 42,
        **kwargs: Any,
    ) -> None:
        """Initialize Chai-1 adapter.

        Args:
            device: 'cpu', 'cuda', or 'auto' to detect.
            cache_dir: Directory for model weights cache.
            num_diffn_timesteps: Diffusion timesteps (more = better quality, slower).
            seed: Random seed for reproducibility.
        """
        self.device = self._resolve_device(device)
        self.cache_dir = cache_dir or Path.home() / ".cache" / "dynafold_hub" / "chai1"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.num_diffn_timesteps = num_diffn_timesteps
        self.seed = seed
        super().__init__(**kwargs)

    def _resolve_device(self, device: str) -> str:
        """Auto-detect device if requested."""
        if device != "auto":
            return device
        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"  # Apple Silicon
        except ImportError:
            pass
        return "cpu"

    def predict_structure(
        self,
        input_data: PredictionInput,
    ) -> StructurePrediction:
        """Run Chai-1 structure prediction.

        Args:
            input_data: Input with sequence (required).

        Returns:
            StructurePrediction with coordinates and confidence.
        """
        input_data.validate()

        # TODO: Implement actual Chai-1 call in Week 1 Day 5-7
        # Pseudocode:
        # 1. Write FASTA file from input_data.sequence
        # 2. Call chai_lab.chai1.run_inference(fasta_file, output_dir, ...)
        # 3. Parse output CIF
        # 4. Extract per-residue confidence from result
        # 5. Return StructurePrediction
        raise NotImplementedError("Chai-1 inference coming in Week 1 implementation")

    @classmethod
    def is_available(cls) -> bool:
        """Check if chai_lab is installed."""
        try:
            import chai_lab  # noqa: F401

            return True
        except ImportError:
            return False
