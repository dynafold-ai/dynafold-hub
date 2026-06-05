"""Load structures from PDB/CIF files into StructurePrediction objects.

This allows users to bring their own predictions (e.g., downloaded from
AlphaFold Server, Chai-1 online, or computed locally) and use DYNAFOLD Hub
for cross-model consensus analysis.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from dynafold_hub.adapters.base import StructurePrediction


def load_prediction_from_file(
    path: Path,
    model_name: str | None = None,
) -> StructurePrediction:
    """Load a structure prediction from PDB or CIF file.

    Args:
        path: Path to .pdb or .cif file.
        model_name: Override model name (default: derived from filename).

    Returns:
        StructurePrediction with all atoms.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If format unsupported or file invalid.

    Example:
        >>> pred = load_prediction_from_file(
        ...     Path("af3_prediction.pdb"),
        ...     model_name="alphafold-3"
        ... )
        >>> print(f"Loaded {pred.n_atoms} atoms")
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Structure file not found: {path}")

    if model_name is None:
        model_name = path.stem

    from dynafold_hub.utils.parsers import load_structure

    structure = load_structure(path)

    # Extract data from biotite AtomArray
    coordinates = np.array(structure.coord, dtype=np.float64)
    atom_names = list(structure.atom_name)
    residue_ids = [int(r) for r in structure.res_id]
    residue_names = list(structure.res_name)

    # Try to extract chain IDs
    chain_ids = None
    if hasattr(structure, "chain_id"):
        chain_ids = list(structure.chain_id)

    # Try to extract B-factor as confidence (AlphaFold convention: B-factor = plDDT)
    confidence = None
    if hasattr(structure, "b_factor"):
        # Compute per-residue mean B-factor
        unique_residues: dict[tuple, list[float]] = {}
        for i, (rid, cid) in enumerate(zip(residue_ids, chain_ids or [""] * len(residue_ids))):
            key = (rid, cid)
            if key not in unique_residues:
                unique_residues[key] = []
            unique_residues[key].append(float(structure.b_factor[i]))

        confidence = np.array(
            [np.mean(vals) for vals in unique_residues.values()],
            dtype=np.float64,
        )

    return StructurePrediction(
        model_name=model_name,
        coordinates=coordinates,
        atom_names=atom_names,
        residue_ids=residue_ids,
        residue_names=residue_names,
        chain_ids=chain_ids,
        confidence_per_residue=confidence,
        metadata={"source_file": str(path)},
    )


def load_multiple_predictions(
    paths: list[Path],
    model_names: list[str] | None = None,
) -> list[StructurePrediction]:
    """Load multiple predictions for consensus comparison.

    Args:
        paths: List of PDB/CIF file paths.
        model_names: Optional override for model names (default: from filenames).

    Returns:
        List of StructurePrediction objects ready for ConsensusEngine.

    Example:
        >>> predictions = load_multiple_predictions(
        ...     [Path("af3.pdb"), Path("chai1.pdb"), Path("boltz2.pdb")]
        ... )
        >>> from dynafold_hub.orchestration import ConsensusEngine
        >>> result = ConsensusEngine().compare(predictions)
    """
    if model_names and len(model_names) != len(paths):
        raise ValueError(
            f"Number of model names ({len(model_names)}) " f"must match paths ({len(paths)})"
        )

    predictions = []
    for i, path in enumerate(paths):
        name = model_names[i] if model_names else None
        pred = load_prediction_from_file(path, model_name=name)
        predictions.append(pred)

    return predictions
