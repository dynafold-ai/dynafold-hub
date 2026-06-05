"""Tests for the ConsensusEngine — the unique value-add of DYNAFOLD Hub."""

from __future__ import annotations

import numpy as np
import pytest

from dynafold_hub.adapters.base import StructurePrediction
from dynafold_hub.orchestration.consensus import (
    ConsensusEngine,
)


def make_prediction(
    name: str,
    n_residues: int = 10,
    confidence: float = 90.0,
    offset: float = 0.0,
) -> StructurePrediction:
    """Helper to create mock predictions with controlled differences."""
    # One Cα per residue, evenly spaced
    coords = np.zeros((n_residues, 3))
    for i in range(n_residues):
        coords[i] = [i * 3.8, 0.0 + offset, 0.0]  # 3.8 Å Cα-Cα distance

    return StructurePrediction(
        model_name=name,
        coordinates=coords,
        atom_names=["CA"] * n_residues,
        residue_ids=list(range(1, n_residues + 1)),
        residue_names=["ALA"] * n_residues,
        confidence_per_residue=np.full(n_residues, confidence),
    )


class TestConsensusEngineBasics:
    """Basic tests for ConsensusEngine."""

    def test_requires_at_least_two_predictions(self):
        engine = ConsensusEngine()
        pred = make_prediction("af3")
        with pytest.raises(ValueError, match="at least 2"):
            engine.compare([pred])

    def test_compare_two_identical_predictions(self):
        """Identical predictions should have perfect agreement."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3")
        pred2 = make_prediction("chai-1")
        result = engine.compare([pred1, pred2])

        assert result.global_rmsd == 0.0
        assert result.agreement_fraction == 1.0
        assert result.trust_score > 90  # Should be very high
        assert len(result.divergent_regions) == 0

    def test_compare_divergent_predictions(self):
        """Predictions with large offset should show divergence."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", offset=0.0)
        pred2 = make_prediction("chai-1", offset=10.0)  # 10 Å shift
        result = engine.compare([pred1, pred2])

        assert result.global_rmsd > 5  # Significant displacement
        assert result.agreement_fraction == 0  # No residue agrees
        assert result.trust_score < 50  # Low trust
        assert len(result.divergent_regions) > 0


class TestDivergentRegions:
    """Tests for divergent region detection."""

    def test_critical_region_detected(self):
        """Large displacements should be flagged as critical."""
        engine = ConsensusEngine()

        # Create two predictions with one region of critical divergence
        pred1 = make_prediction("af3", n_residues=20)
        pred2 = make_prediction("chai-1", n_residues=20)

        # Move residues 5-10 in pred2 by 8 Å (critical)
        for i in range(4, 10):
            pred2.coordinates[i] += [0, 8.0, 0]

        result = engine.compare([pred1, pred2])

        # Should find one critical region
        critical = [r for r in result.divergent_regions if r.severity == "critical"]
        assert len(critical) >= 1
        # First critical region should be around residues 5-10
        assert critical[0].max_displacement_angstroms >= 6.0

    def test_no_divergence_when_models_agree(self):
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", n_residues=20)
        pred2 = make_prediction("chai-1", n_residues=20)
        result = engine.compare([pred1, pred2])
        assert len(result.divergent_regions) == 0


class TestRecommendations:
    """Tests for experimental recommendations."""

    def test_recommendations_for_consensus(self):
        """When models agree, recommendation says no validation needed."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3")
        pred2 = make_prediction("chai-1")
        result = engine.compare([pred1, pred2])
        # Should have a "no validation needed" message
        assert any("agree" in r.lower() for r in result.recommendations)

    def test_recommendations_for_critical_divergence(self):
        """Critical divergence should recommend specific experiments."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", n_residues=20)
        pred2 = make_prediction("chai-1", n_residues=20)

        # Create critical divergence
        for i in range(5, 12):
            pred2.coordinates[i] += [0, 10.0, 0]

        result = engine.compare([pred1, pred2])
        # Should recommend HDX-MS or cryo-EM for critical regions
        recs_text = " ".join(result.recommendations).lower()
        assert any(method in recs_text for method in ["hdx", "cryo-em", "mutagenesis"])


class TestTrustScore:
    """Tests for the Trust Score computation."""

    def test_trust_score_high_when_models_agree_and_confident(self):
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", confidence=95.0)
        pred2 = make_prediction("chai-1", confidence=92.0)
        result = engine.compare([pred1, pred2])
        # Perfect agreement + high confidence = trust > 90
        assert result.trust_score > 90

    def test_trust_score_low_when_models_disagree(self):
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", offset=0.0, confidence=80.0)
        pred2 = make_prediction("chai-1", offset=15.0, confidence=80.0)
        result = engine.compare([pred1, pred2])
        # Large disagreement = low trust
        assert result.trust_score < 60

    def test_trust_score_works_without_confidence(self):
        """Trust score should still work when models don't provide plDDT."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3")
        pred1.confidence_per_residue = None
        pred2 = make_prediction("chai-1")
        pred2.confidence_per_residue = None
        result = engine.compare([pred1, pred2])
        # Should compute score based on agreement only
        assert 0 <= result.trust_score <= 100


class TestMultipleModels:
    """Tests with 3+ models."""

    def test_compare_three_models(self):
        engine = ConsensusEngine()
        pred1 = make_prediction("af3")
        pred2 = make_prediction("chai-1")
        pred3 = make_prediction("boltz-2")
        result = engine.compare([pred1, pred2, pred3])

        assert len(result.models_compared) == 3
        assert "af3" in result.models_compared
        assert "chai-1" in result.models_compared
        assert "boltz-2" in result.models_compared

    def test_validation_residue_count_mismatch(self):
        """Predictions with different residue counts should fail."""
        engine = ConsensusEngine()
        pred1 = make_prediction("af3", n_residues=10)
        pred2 = make_prediction("chai-1", n_residues=20)
        with pytest.raises(ValueError, match="different residue counts"):
            engine.compare([pred1, pred2])
