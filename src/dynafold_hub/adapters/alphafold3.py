"""AlphaFold 3 adapter.

Wraps the AlphaFold Server API (https://alphafoldserver.com) for protein
structure prediction. AlphaFold 3 is DeepMind's latest model that predicts
biomolecular complexes including proteins, ligands, DNA, RNA, and ions.

Reference: Abramson et al., Nature 2024
URL: https://www.nature.com/articles/s41586-024-07487-w
License: Free for non-commercial research, paid commercial use
"""

from __future__ import annotations

import os
from typing import Any

from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    PredictionInput,
    StructurePrediction,
    TaskType,
)


class AlphaFold3Adapter(BaseModelAdapter):
    """Adapter for AlphaFold 3 (via AlphaFold Server API).

    AlphaFold 3 is DeepMind's state-of-the-art structure prediction model.
    This adapter uses the official AlphaFold Server REST API rather than
    running the model locally (which is not feasible for most users).

    Authentication:
        Set ALPHAFOLD_SERVER_API_KEY environment variable, or pass api_key.

    Limitations:
        - Free tier has rate limits (varies)
        - Commercial use requires paid subscription
        - Some advanced features may require API upgrades

    Example:
        >>> adapter = AlphaFold3Adapter(api_key="your-key")
        >>> result = adapter.predict_structure(
        ...     PredictionInput(sequence="MGKLSTAAGSALA")
        ... )
    """

    name = "alphafold-3"
    supported_tasks = [
        TaskType.STRUCTURE_PREDICTION,
        TaskType.PROTEIN_LIGAND_DOCKING,
    ]
    requires_gpu = False  # Runs server-side

    paper_url = "https://www.nature.com/articles/s41586-024-07487-w"
    code_url = "https://github.com/google-deepmind/alphafold3"
    license = "Free non-commercial / Paid commercial"

    SERVER_URL = "https://alphafoldserver.com/api"

    def __init__(
        self,
        api_key: str | None = None,
        timeout: int = 600,
        **kwargs: Any,
    ) -> None:
        """Initialize AlphaFold 3 adapter.

        Args:
            api_key: AlphaFold Server API key. Falls back to env var.
            timeout: Max seconds to wait for prediction (default 10 min).
        """
        self.api_key = api_key or os.environ.get("ALPHAFOLD_SERVER_API_KEY")
        self.timeout = timeout
        super().__init__(**kwargs)

    def _check_availability(self) -> None:
        """Override: also check for API key."""
        super()._check_availability()
        # API key check happens at request time, not init
        # (allows showing in CLI list without key)

    def predict_structure(
        self,
        input_data: PredictionInput,
    ) -> StructurePrediction:
        """Predict structure via AlphaFold Server API.

        Args:
            input_data: Input with sequence (required).

        Returns:
            StructurePrediction with plDDT confidence.

        Raises:
            ValueError: If sequence is missing.
            RuntimeError: If API call fails.
        """
        input_data.validate()

        if not self.api_key:
            raise RuntimeError(
                "AlphaFold Server API key required. "
                "Set ALPHAFOLD_SERVER_API_KEY environment variable."
            )

        # TODO: Implement actual API call in Week 1 Day 6-7
        # The AlphaFold Server has a job submission + polling API
        # For now this is a stub showing the interface
        raise NotImplementedError("AlphaFold 3 API integration coming in Week 1 implementation")

    @classmethod
    def is_available(cls) -> bool:
        """Check if requests library is installed (for API calls)."""
        try:
            import requests  # noqa: F401

            return True
        except ImportError:
            return False

    @classmethod
    def get_info(cls) -> dict[str, Any]:
        """Override to indicate API key requirement."""
        info = super().get_info()
        info["requires_api_key"] = True
        info["api_key_env_var"] = "ALPHAFOLD_SERVER_API_KEY"
        return info
