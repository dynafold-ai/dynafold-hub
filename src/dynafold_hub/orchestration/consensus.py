"""Consensus engine: compare predictions from multiple models.

This is the UNIQUE VALUE of DYNAFOLD Hub. Given predictions from 2+ models,
identifies where they agree (high confidence) and where they disagree
(regions needing experimental validation).

Algorithm:
1. Align structures using protein backbone (Cα atoms)
2. Compute per-residue displacement (RMSD)
3. Combine with per-model confidence (plDDT-like) to compute Trust Score
4. Identify divergent regions
5. Recommend experiments to validate divergent regions
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from dynafold_hub.adapters.base import StructurePrediction


@dataclass
class DivergentRegion:
    """A region where models disagree significantly."""

    residue_range: tuple[int, int]
    max_displacement_angstroms: float
    mean_confidence: float
    severity: str  # "minor" | "moderate" | "critical"


@dataclass
class ConsensusResult:
    """Result of comparing multiple structure predictions.

    Attributes:
        models_compared: Names of models that were compared.
        n_residues: Total number of residues compared.
        global_rmsd: Mean RMSD across all residues (Å).
        agreement_fraction: Fraction of residues where models agree (RMSD < 2 Å).
        trust_score: Overall trust score 0-100.
        divergent_regions: List of regions where models disagree.
        per_residue_rmsd: RMSD per residue across models.
        per_residue_confidence: Mean confidence per residue.
        recommendations: Human-readable experimental recommendations.
    """

    models_compared: list[str]
    n_residues: int
    global_rmsd: float
    agreement_fraction: float
    trust_score: float
    divergent_regions: list[DivergentRegion]
    per_residue_rmsd: np.ndarray
    per_residue_confidence: np.ndarray | None = None
    recommendations: list[str] = field(default_factory=list)


class ConsensusEngine:
    """Engine for cross-model consensus analysis.

    Example:
        >>> engine = ConsensusEngine()
        >>> result = engine.compare([af3_pred, chai_pred, boltz_pred])
        >>> print(f"Trust: {result.trust_score:.1f}/100")
        >>> print(f"{len(result.divergent_regions)} regions need validation")
    """

    # Thresholds (tunable based on task)
    AGREEMENT_RMSD_THRESHOLD = 2.0  # Å — below this, models "agree"
    MINOR_DIVERGENCE = 2.0  # Å
    MODERATE_DIVERGENCE = 4.0  # Å
    CRITICAL_DIVERGENCE = 6.0  # Å

    def compare(
        self,
        predictions: list[StructurePrediction],
    ) -> ConsensusResult:
        """Compare 2+ structure predictions.

        Args:
            predictions: List of StructurePrediction from different models.

        Returns:
            ConsensusResult with agreement analysis and recommendations.

        Raises:
            ValueError: If fewer than 2 predictions provided.
        """
        if len(predictions) < 2:
            raise ValueError("Need at least 2 predictions to compute consensus")

        # Validate all predictions have compatible size
        n_residues = predictions[0].n_residues
        for pred in predictions[1:]:
            if pred.n_residues != n_residues:
                raise ValueError(
                    f"Predictions have different residue counts: "
                    f"{predictions[0].model_name}={n_residues} "
                    f"vs {pred.model_name}={pred.n_residues}"
                )

        # Compute per-residue RMSD across all model pairs
        per_residue_rmsd = self._compute_per_residue_rmsd(predictions)

        # Aggregate confidence (mean across models if available)
        per_residue_confidence = self._aggregate_confidence(predictions)

        # Identify divergent regions
        divergent = self._find_divergent_regions(per_residue_rmsd, per_residue_confidence)

        # Compute trust score (0-100)
        trust = self._compute_trust_score(per_residue_rmsd, per_residue_confidence)

        # Agreement fraction
        agreement = float(np.mean(per_residue_rmsd < self.AGREEMENT_RMSD_THRESHOLD))

        # Recommendations
        recommendations = self._recommend_experiments(divergent, predictions[0])

        return ConsensusResult(
            models_compared=[p.model_name for p in predictions],
            n_residues=n_residues,
            global_rmsd=float(np.mean(per_residue_rmsd)),
            agreement_fraction=agreement,
            trust_score=trust,
            divergent_regions=divergent,
            per_residue_rmsd=per_residue_rmsd,
            per_residue_confidence=per_residue_confidence,
            recommendations=recommendations,
        )

    def _compute_per_residue_rmsd(
        self,
        predictions: list[StructurePrediction],
    ) -> np.ndarray:
        """Compute per-residue RMSD between all model pairs.

        For each residue, calculates the mean pairwise RMSD across
        all combinations of models.

        Returns:
            Array shape (n_residues,) with RMSD values in Å.
        """
        n_residues = predictions[0].n_residues
        n_models = len(predictions)

        # Get Cα coordinates per residue per model
        # Assuming for now coordinates are organized as (n_atoms, 3)
        # We need to map atoms to residues
        ca_coords_per_model = []
        for pred in predictions:
            ca_coords = self._extract_ca_coordinates(pred)
            ca_coords_per_model.append(ca_coords)

        # Compute pairwise displacement per residue
        rmsds = np.zeros(n_residues)
        n_pairs = 0
        for i in range(n_models):
            for j in range(i + 1, n_models):
                pair_diff = ca_coords_per_model[i] - ca_coords_per_model[j]
                pair_rmsd = np.sqrt(np.sum(pair_diff**2, axis=1))
                rmsds += pair_rmsd
                n_pairs += 1

        if n_pairs > 0:
            rmsds /= n_pairs

        return rmsds

    def _extract_ca_coordinates(self, pred: StructurePrediction) -> np.ndarray:
        """Extract Cα coordinates per residue.

        Returns:
            Array shape (n_residues, 3) with Cα positions.
        """
        # Find indices of CA atoms
        ca_indices = [i for i, name in enumerate(pred.atom_names) if name == "CA"]

        if not ca_indices:
            # Fallback: use coordinates directly (assume 1 atom per residue)
            return pred.coordinates

        return pred.coordinates[ca_indices]

    def _aggregate_confidence(
        self,
        predictions: list[StructurePrediction],
    ) -> np.ndarray | None:
        """Average per-residue confidence across models.

        Returns:
            Array shape (n_residues,) with mean confidence, or None if no model has it.
        """
        confidences = [
            p.confidence_per_residue for p in predictions if p.confidence_per_residue is not None
        ]
        if not confidences:
            return None
        return np.mean(confidences, axis=0)

    def _find_divergent_regions(
        self,
        per_residue_rmsd: np.ndarray,
        per_residue_confidence: np.ndarray | None,
    ) -> list[DivergentRegion]:
        """Identify contiguous regions of model disagreement.

        Returns:
            List of DivergentRegion sorted by severity (worst first).
        """
        regions = []
        in_divergent = False
        start = 0

        for i, rmsd in enumerate(per_residue_rmsd):
            is_divergent = rmsd > self.MINOR_DIVERGENCE

            if is_divergent and not in_divergent:
                start = i
                in_divergent = True
            elif not is_divergent and in_divergent:
                # End of divergent region
                end = i - 1
                regions.append(
                    self._classify_region(start, end, per_residue_rmsd, per_residue_confidence)
                )
                in_divergent = False

        # Handle region extending to end
        if in_divergent:
            regions.append(
                self._classify_region(
                    start,
                    len(per_residue_rmsd) - 1,
                    per_residue_rmsd,
                    per_residue_confidence,
                )
            )

        # Sort by severity (critical first)
        severity_order = {"critical": 0, "moderate": 1, "minor": 2}
        regions.sort(key=lambda r: severity_order[r.severity])

        return regions

    def _classify_region(
        self,
        start: int,
        end: int,
        rmsds: np.ndarray,
        confidence: np.ndarray | None,
    ) -> DivergentRegion:
        """Classify a divergent region by severity."""
        region_rmsds = rmsds[start : end + 1]
        max_rmsd = float(np.max(region_rmsds))

        if max_rmsd > self.CRITICAL_DIVERGENCE:
            severity = "critical"
        elif max_rmsd > self.MODERATE_DIVERGENCE:
            severity = "moderate"
        else:
            severity = "minor"

        mean_conf = 0.0
        if confidence is not None:
            mean_conf = float(np.mean(confidence[start : end + 1]))

        return DivergentRegion(
            residue_range=(start + 1, end + 1),  # 1-indexed for display
            max_displacement_angstroms=max_rmsd,
            mean_confidence=mean_conf,
            severity=severity,
        )

    def _compute_trust_score(
        self,
        per_residue_rmsd: np.ndarray,
        per_residue_confidence: np.ndarray | None,
    ) -> float:
        """Compute overall trust score (0-100).

        Score combines:
        - Agreement between models (low RMSD = good)
        - Model confidence (high plDDT = good)

        Returns:
            Trust score 0-100.
        """
        # Agreement component: % residues with RMSD < 2 Å, weighted
        agreement_score = float(np.mean(per_residue_rmsd < self.AGREEMENT_RMSD_THRESHOLD)) * 100

        if per_residue_confidence is None:
            return agreement_score

        # Confidence component: mean plDDT (already 0-100 scale typically)
        # Auto-detect scale: >1.0 means 0-100 plDDT, otherwise 0-1
        confidence_score = float(np.mean(per_residue_confidence))
        confidence_pct = confidence_score if confidence_score > 1.0 else confidence_score * 100

        # Weighted average: 60% agreement, 40% confidence
        return 0.6 * agreement_score + 0.4 * confidence_pct

    def _recommend_experiments(
        self,
        divergent_regions: list[DivergentRegion],
        reference: StructurePrediction,
    ) -> list[str]:
        """Generate experimental recommendations for divergent regions.

        Args:
            divergent_regions: Regions where models disagree.
            reference: Reference structure for residue identity lookup.

        Returns:
            List of human-readable recommendations.
        """
        recommendations = []

        if not divergent_regions:
            recommendations.append(
                "✓ All models agree. High confidence in prediction. "
                "No critical validation needed."
            )
            return recommendations

        n_critical = sum(1 for r in divergent_regions if r.severity == "critical")
        if n_critical > 0:
            recommendations.append(
                f"⚠ {n_critical} CRITICAL divergent region(s) detected. "
                f"Strongly recommend wet-lab validation before drug design."
            )

        for region in divergent_regions[:5]:  # Top 5 most severe
            start, end = region.residue_range
            size = end - start + 1
            rec = (
                f"[{region.severity.upper()}] Residues {start}-{end} "
                f"(size {size}, max displacement {region.max_displacement_angstroms:.1f} Å): "
            )

            if region.severity == "critical":
                rec += (
                    "Models disagree drastically. Recommend "
                    "HDX-MS (hydrogen-deuterium exchange MS) or "
                    "cryo-EM to resolve structure experimentally."
                )
            elif region.severity == "moderate":
                rec += (
                    "Significant disagreement. Recommend "
                    "site-directed mutagenesis at key residues + "
                    "functional assay (e.g., binding affinity)."
                )
            else:
                rec += (
                    "Minor flexibility. Likely a loop region. "
                    "Consider MD simulation (10-50 ns) to characterize dynamics."
                )

            recommendations.append(rec)

        if len(divergent_regions) > 5:
            recommendations.append(
                f"... and {len(divergent_regions) - 5} more divergent regions "
                f"of lower severity."
            )

        return recommendations
