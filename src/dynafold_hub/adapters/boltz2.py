"""Boltz-2 adapter.

Boltz-2 is an open-source structure prediction model from MIT Wohlwend Lab.
First fully open model approaching AlphaFold 3 performance, with added
binding affinity prediction (approaching FEP accuracy at fraction of cost).

Reference: Wohlwend et al., 2024
URL: https://github.com/jwohlwend/boltz
License: MIT (fully open commercial use)
Install: pip install boltz
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


class Boltz2Adapter(BaseModelAdapter):
    """Adapter for Boltz-2 structure + affinity prediction model.

    Boltz-2 is unique in offering:
    - Structure prediction (proteins, ligands, NA)
    - Binding affinity estimation (FEP-quality at lower cost)
    - Fully open MIT license (most permissive)

    Example:
        >>> adapter = Boltz2Adapter(device="cuda")
        >>> result = adapter.predict_structure(
        ...     PredictionInput(sequence="MGKLSTAA...")
        ... )
    """

    name = "boltz-2"
    supported_tasks = [
        TaskType.STRUCTURE_PREDICTION,
        TaskType.PROTEIN_LIGAND_DOCKING,
        TaskType.AFFINITY_PREDICTION,
    ]
    requires_gpu = False  # CPU works but slow

    paper_url = "https://www.biorxiv.org/content/10.1101/2024.11.19.624167"
    code_url = "https://github.com/jwohlwend/boltz"
    license = "MIT"

    def __init__(
        self,
        device: str = "auto",
        cache_dir: Path | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize Boltz-2 adapter."""
        self.device = self._resolve_device(device)
        self.cache_dir = cache_dir or Path.home() / ".cache" / "dynafold_hub" / "boltz2"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
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
                return "mps"
        except ImportError:
            pass
        return "cpu"

    def predict_structure(
        self,
        input_data: PredictionInput,
    ) -> StructurePrediction:
        """Run Boltz-2 structure prediction.

        Args:
            input_data: Input with sequence (required).

        Returns:
            StructurePrediction with coordinates and confidence.
        """
        input_data.validate()

        # TODO: Implement actual Boltz-2 call in Week 2
        raise NotImplementedError("Boltz-2 inference coming in Week 2 implementation")

    @classmethod
    def is_available(cls) -> bool:
        """Check if boltz is installed."""
        try:
            import boltz  # noqa: F401

            return True
        except ImportError:
            return False
