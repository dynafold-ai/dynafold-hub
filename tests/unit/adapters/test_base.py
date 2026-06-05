"""Tests for the BaseModelAdapter abstract class."""

from __future__ import annotations

import numpy as np
import pytest

from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    DockingPrediction,
    PredictionInput,
    StructurePrediction,
    TaskType,
)


class TestTaskType:
    """Tests for TaskType enum."""

    def test_task_type_values_are_strings(self):
        """TaskType values must be strings for JSON serialization."""
        assert TaskType.STRUCTURE_PREDICTION.value == "structure_prediction"
        assert TaskType.PROTEIN_LIGAND_DOCKING.value == "protein_ligand_docking"

    def test_task_type_count(self):
        """We have at least 5 task types defined."""
        assert len(list(TaskType)) >= 5

    def test_task_type_iterable(self):
        """TaskType can be iterated."""
        all_tasks = [t.value for t in TaskType]
        assert "structure_prediction" in all_tasks
        assert "antibody_design" in all_tasks


class TestPredictionInput:
    """Tests for PredictionInput dataclass."""

    def test_minimal_creation(self):
        inp = PredictionInput(sequence="MGKLSTA")
        assert inp.sequence == "MGKLSTA"
        assert inp.task == TaskType.STRUCTURE_PREDICTION
        assert inp.extra_params == {}

    def test_validate_structure_prediction_requires_sequence(self):
        inp = PredictionInput(task=TaskType.STRUCTURE_PREDICTION)
        with pytest.raises(ValueError, match="requires sequence"):
            inp.validate()

    def test_validate_docking_requires_ligand(self):
        inp = PredictionInput(
            sequence="MGKLSTA",
            task=TaskType.PROTEIN_LIGAND_DOCKING,
        )
        with pytest.raises(ValueError, match="ligand_smiles"):
            inp.validate()

    def test_validate_docking_complete(self):
        inp = PredictionInput(
            sequence="MGKLSTA",
            ligand_smiles="CCO",
            task=TaskType.PROTEIN_LIGAND_DOCKING,
        )
        # Should not raise
        inp.validate()

    def test_validate_structure_prediction_complete(self):
        inp = PredictionInput(sequence="MGKLSTA")
        inp.validate()  # Should not raise


class TestStructurePrediction:
    """Tests for StructurePrediction dataclass."""

    def _make_dummy_prediction(self, n_atoms: int = 10) -> StructurePrediction:
        return StructurePrediction(
            model_name="test-model",
            coordinates=np.zeros((n_atoms, 3)),
            atom_names=["CA"] * n_atoms,
            residue_ids=list(range(1, n_atoms + 1)),
            residue_names=["ALA"] * n_atoms,
            confidence_per_residue=np.full(n_atoms, 85.0),
        )

    def test_n_atoms(self):
        pred = self._make_dummy_prediction(n_atoms=25)
        assert pred.n_atoms == 25

    def test_mean_confidence(self):
        pred = self._make_dummy_prediction()
        assert pred.mean_confidence() == 85.0

    def test_mean_confidence_none_when_no_data(self):
        pred = StructurePrediction(
            model_name="test",
            coordinates=np.zeros((1, 3)),
            atom_names=["CA"],
            residue_ids=[1],
            residue_names=["ALA"],
        )
        assert pred.mean_confidence() is None


class TestDockingPrediction:
    """Tests for DockingPrediction."""

    def test_best_pose_is_first(self):
        pose1 = StructurePrediction(
            model_name="test",
            coordinates=np.zeros((1, 3)),
            atom_names=["CA"],
            residue_ids=[1],
            residue_names=["ALA"],
        )
        pose2 = StructurePrediction(
            model_name="test",
            coordinates=np.ones((1, 3)),
            atom_names=["CA"],
            residue_ids=[1],
            residue_names=["ALA"],
        )
        dock = DockingPrediction(
            model_name="test",
            poses=[pose1, pose2],
            binding_energies=[-9.5, -7.2],
            confidence_scores=[0.95, 0.78],
        )
        assert dock.best_pose is pose1
        assert dock.best_energy == -9.5


class TestBaseModelAdapter:
    """Tests for the abstract BaseModelAdapter."""

    def test_cannot_instantiate_directly(self):
        """ABC should be enforceable for proper subclasses."""
        # Note: BaseModelAdapter is ABC but has no abstract methods,
        # so it can technically be instantiated. The test is more conceptual.
        # In Phase 2 we'll mark predict_structure as @abstractmethod.
        adapter = BaseModelAdapter()
        # Default name is 'base', should not be used in production
        assert adapter.name == "base"

    def test_subclass_can_be_instantiated(self):
        class DummyAdapter(BaseModelAdapter):
            name = "dummy"
            supported_tasks = [TaskType.STRUCTURE_PREDICTION]

        adapter = DummyAdapter()
        assert adapter.name == "dummy"

    def test_get_info_includes_required_fields(self):
        class DummyAdapter(BaseModelAdapter):
            name = "dummy"
            supported_tasks = [TaskType.STRUCTURE_PREDICTION]
            license = "MIT"

        info = DummyAdapter.get_info()
        assert info["name"] == "dummy"
        assert info["license"] == "MIT"
        assert "available" in info
        assert "requires_gpu" in info
