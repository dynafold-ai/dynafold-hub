"""Base abstract class for all model adapters.

This module defines the unified interface that all model adapters must implement.
It standardizes inputs and outputs across different SOTA models (AlphaFold 3,
Chai-1, Boltz-2, etc.) so that they can be used interchangeably and compared.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import numpy as np


class TaskType(str, Enum):
    """Types of tasks supported by adapters.

    Using str-based enum for easy serialization (JSON, configs).
    """

    STRUCTURE_PREDICTION = "structure_prediction"
    """Predict 3D structure of a protein/biomolecule from sequence."""

    PROTEIN_LIGAND_DOCKING = "protein_ligand_docking"
    """Predict binding pose of a small molecule to a protein."""

    PROTEIN_DESIGN = "protein_design"
    """De novo design of a new protein structure."""

    SEQUENCE_DESIGN = "sequence_design"
    """Design amino acid sequence given a structure (inverse folding)."""

    ANTIBODY_DESIGN = "antibody_design"
    """De novo design of antibodies for a given target."""

    AFFINITY_PREDICTION = "affinity_prediction"
    """Predict binding affinity (Kd, IC50, etc.) for a complex."""

    EMBEDDING = "embedding"
    """Generate latent representations of sequences/structures."""


@dataclass
class PredictionInput:
    """Standardized input for any model adapter.

    Not all fields are required for all tasks. Each adapter validates
    that the required fields are present.

    Attributes:
        sequence: Single-letter amino acid sequence (for proteins).
        ligand_smiles: SMILES string of the ligand (for docking).
        receptor_pdb: Path to receptor PDB file (for docking/design).
        epitope_residues: Residue IDs of the epitope (for antibody design).
        task: Type of prediction task.
        extra_params: Adapter-specific parameters (random seed, recycles, etc.).
    """

    sequence: str | None = None
    ligand_smiles: str | None = None
    receptor_pdb: Path | None = None
    epitope_residues: list[int] | None = None
    task: TaskType = TaskType.STRUCTURE_PREDICTION
    extra_params: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate that input is complete for the requested task.

        Raises:
            ValueError: If required fields are missing.
        """
        if self.task == TaskType.STRUCTURE_PREDICTION:
            if not self.sequence:
                raise ValueError("Structure prediction requires sequence")

        elif self.task == TaskType.PROTEIN_LIGAND_DOCKING:
            if not (self.sequence or self.receptor_pdb):
                raise ValueError("Docking requires either sequence or receptor_pdb")
            if not self.ligand_smiles:
                raise ValueError("Docking requires ligand_smiles")

        elif self.task == TaskType.ANTIBODY_DESIGN:
            if not self.receptor_pdb:
                raise ValueError("Antibody design requires target receptor_pdb")


@dataclass
class StructurePrediction:
    """Standardized structure prediction output.

    Attributes:
        model_name: Name of the model that produced this prediction.
        coordinates: Atom coordinates, shape (N_atoms, 3) in Angstroms.
        atom_names: Atom names (e.g., 'CA', 'N', 'C', 'O').
        residue_ids: Residue numbering (1-based).
        residue_names: 3-letter residue codes (e.g., 'ALA', 'GLY').
        chain_ids: Chain identifiers (e.g., 'A', 'B').
        confidence_per_residue: Per-residue confidence (plDDT-like, 0-100).
        pae_matrix: Predicted Aligned Error matrix, shape (N_res, N_res).
        ptm_score: Predicted TM-score (global confidence, 0-1).
        metadata: Adapter-specific extra info.
    """

    model_name: str
    coordinates: np.ndarray  # (N_atoms, 3)
    atom_names: list[str]
    residue_ids: list[int]
    residue_names: list[str]
    chain_ids: list[str] | None = None
    confidence_per_residue: np.ndarray | None = None
    pae_matrix: np.ndarray | None = None
    ptm_score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the structure."""
        return len(self.coordinates)

    @property
    def n_residues(self) -> int:
        """Number of unique residues."""
        return len(set(zip(self.residue_ids, self.chain_ids or [""] * len(self.residue_ids))))

    def mean_confidence(self) -> float | None:
        """Mean per-residue confidence (e.g., mean plDDT)."""
        if self.confidence_per_residue is None:
            return None
        return float(np.mean(self.confidence_per_residue))


@dataclass
class DockingPrediction:
    """Standardized protein-ligand docking output.

    Attributes:
        model_name: Name of the model.
        poses: List of predicted poses (sorted by score, best first).
        binding_energies: Binding scores per pose (kcal/mol; more negative = better).
        confidence_scores: Per-pose confidence (0-1).
        metadata: Adapter-specific extra info.
    """

    model_name: str
    poses: list[StructurePrediction]
    binding_energies: list[float]
    confidence_scores: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def best_pose(self) -> StructurePrediction:
        """Return the best-scoring pose."""
        return self.poses[0]

    @property
    def best_energy(self) -> float:
        """Best (most negative) binding energy."""
        return self.binding_energies[0]


@dataclass
class DesignedSequence:
    """Standardized output for sequence design tasks.

    Attributes:
        model_name: Name of the model.
        sequence: Designed amino acid sequence.
        score: Design score (model-specific).
        confidence: Per-residue confidence in design.
        metadata: Adapter-specific info.
    """

    model_name: str
    sequence: str
    score: float
    confidence: np.ndarray | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelNotAvailableError(Exception):
    """Raised when a model adapter cannot be used in the current environment."""

    pass


class BaseModelAdapter(ABC):
    """Abstract base class for all model adapters.

    Each concrete adapter (Chai1Adapter, AlphaFold3Adapter, etc.) must:
    1. Set class attributes (name, supported_tasks, requires_gpu)
    2. Implement predict_structure() if it supports structure prediction
    3. Override is_available() to check installation

    Example:
        class MyAdapter(BaseModelAdapter):
            name = "my-model"
            supported_tasks = [TaskType.STRUCTURE_PREDICTION]

            def predict_structure(self, input_data):
                input_data.validate()
                # ... model-specific logic ...
                return StructurePrediction(...)
    """

    name: str = "base"
    """Unique identifier for this adapter (lowercase, hyphenated)."""

    supported_tasks: list[TaskType] = []
    """List of TaskType this adapter can handle."""

    requires_gpu: bool = False
    """Whether GPU is required (vs nice-to-have)."""

    paper_url: str | None = None
    """URL to the paper describing this model."""

    code_url: str | None = None
    """URL to the model's source code."""

    license: str = "Unknown"
    """License of the underlying model (e.g., 'Apache 2.0', 'MIT')."""

    # --------- Lifecycle ---------

    def __init__(self, **kwargs: Any) -> None:
        """Initialize adapter with optional configuration."""
        self._check_availability()

    def _check_availability(self) -> None:
        """Raise ModelNotAvailableError if adapter can't be used."""
        if not self.__class__.is_available():
            raise ModelNotAvailableError(
                f"{self.name} is not available. " f"Check installation: {self.code_url}"
            )

    # --------- Prediction methods (override in subclasses) ---------

    def predict_structure(self, input_data: PredictionInput) -> StructurePrediction:
        """Predict 3D structure for given input.

        Args:
            input_data: Validated input with sequence and parameters.

        Returns:
            StructurePrediction with coordinates and confidence.

        Raises:
            NotImplementedError: If this adapter doesn't support structure prediction.
        """
        raise NotImplementedError(f"{self.name} does not support structure prediction")

    def predict_docking(self, input_data: PredictionInput) -> DockingPrediction:
        """Predict protein-ligand docking poses.

        Args:
            input_data: Validated input with receptor + ligand.

        Returns:
            DockingPrediction with ranked poses.

        Raises:
            NotImplementedError: If this adapter doesn't support docking.
        """
        raise NotImplementedError(f"{self.name} does not support docking")

    def design_sequence(self, structure: StructurePrediction) -> DesignedSequence:
        """Design amino acid sequence for a given structure (inverse folding).

        Args:
            structure: Target structure to design sequence for.

        Returns:
            DesignedSequence with proposed sequence.

        Raises:
            NotImplementedError: If this adapter doesn't support sequence design.
        """
        raise NotImplementedError(f"{self.name} does not support sequence design")

    # --------- Class methods (no instance needed) ---------

    @classmethod
    def is_available(cls) -> bool:
        """Check if this adapter can be used in current environment.

        Override in subclasses to check for installed packages, API keys, etc.

        Returns:
            True if adapter is ready to use, False otherwise.
        """
        return True

    @classmethod
    def get_info(cls) -> dict[str, Any]:
        """Return metadata about this adapter.

        Returns:
            Dict with name, supported_tasks, requires_gpu, license, etc.
        """
        return {
            "name": cls.name,
            "supported_tasks": [t.value for t in cls.supported_tasks],
            "requires_gpu": cls.requires_gpu,
            "available": cls.is_available(),
            "paper_url": cls.paper_url,
            "code_url": cls.code_url,
            "license": cls.license,
        }

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"{self.__class__.__name__}(name='{self.name}')"
