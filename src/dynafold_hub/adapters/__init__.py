"""Model adapters for DYNAFOLD Hub.

Each adapter wraps a specific SOTA model behind a unified interface.
"""

from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    DesignedSequence,
    DockingPrediction,
    ModelNotAvailableError,
    PredictionInput,
    StructurePrediction,
    TaskType,
)

# Concrete adapters (imported lazily to avoid heavy dependencies)
# Each adapter is imported only when needed.

__all__ = [
    "BaseModelAdapter",
    "DesignedSequence",
    "DockingPrediction",
    "ModelNotAvailableError",
    "PredictionInput",
    "StructurePrediction",
    "TaskType",
    # Adapters added via get_adapter() function below
    "get_adapter",
    "list_available_adapters",
]


def get_adapter(name: str, **kwargs) -> BaseModelAdapter:
    """Get an adapter instance by name.

    This is the recommended way to instantiate adapters as it handles
    lazy imports of heavy dependencies (e.g., chai_lab only loaded when
    Chai1Adapter is requested).

    Args:
        name: Adapter name (e.g., 'chai-1', 'alphafold-3', 'boltz-2').
        **kwargs: Adapter-specific initialization parameters.

    Returns:
        Instantiated adapter.

    Raises:
        ValueError: If adapter name is unknown.
        ModelNotAvailableError: If adapter dependencies are missing.

    Example:
        >>> adapter = get_adapter('chai-1', device='cpu')
        >>> result = adapter.predict_structure(input_data)
    """
    name = name.lower()

    if name in ("alphafold-3", "alphafold3", "af3"):
        from dynafold_hub.adapters.alphafold3 import AlphaFold3Adapter

        return AlphaFold3Adapter(**kwargs)

    if name in ("chai-1", "chai1"):
        from dynafold_hub.adapters.chai1 import Chai1Adapter

        return Chai1Adapter(**kwargs)

    if name in ("boltz-2", "boltz2"):
        from dynafold_hub.adapters.boltz2 import Boltz2Adapter

        return Boltz2Adapter(**kwargs)

    raise ValueError(f"Unknown adapter: {name}. " f"Available: alphafold-3, chai-1, boltz-2")


def list_available_adapters() -> list[dict]:
    """List all adapters with their availability status.

    Returns:
        List of dicts with adapter info (name, available, requires_gpu, etc.).
    """
    adapters_to_check = []

    # Lazy import to avoid loading all dependencies
    try:
        from dynafold_hub.adapters.alphafold3 import AlphaFold3Adapter

        adapters_to_check.append(AlphaFold3Adapter)
    except ImportError:
        pass

    try:
        from dynafold_hub.adapters.chai1 import Chai1Adapter

        adapters_to_check.append(Chai1Adapter)
    except ImportError:
        pass

    try:
        from dynafold_hub.adapters.boltz2 import Boltz2Adapter

        adapters_to_check.append(Boltz2Adapter)
    except ImportError:
        pass

    return [adapter.get_info() for adapter in adapters_to_check]
