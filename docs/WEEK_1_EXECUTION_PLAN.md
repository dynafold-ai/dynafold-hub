# Semana 1 — Plan de Ejecución Detallado

> **Para Claude**: este es el plan paso-a-paso para la primera semana de desarrollo. Sigue las tareas en orden. Cada tarea tiene definición clara de "done".

**Inicio estimado**: cuando Sergio confirme
**Duración**: 7 días (40-50 horas de trabajo)
**Objetivo**: Tener `Chai1Adapter` funcionando + repo GitHub público

---

## Pre-requisitos antes de empezar

Sergio debe confirmar:

- [ ] Instancia Verda destruida (no más facturación)
- [ ] Cuenta GitHub activa con SSH keys configuradas
- [ ] Dominio dynafold.io comprado (opcional pero recomendado, ~$12/año)
- [ ] HuggingFace account creada (gratis)
- [ ] OpenAI API key (opcional, para futuras integraciones)
- [ ] Decisión: ¿queremos `dynafold-ai/dynafold-hub` o `SergioNotionHQ/dynafold-hub`?

Claude debe verificar:

- [ ] Python 3.11+ instalado localmente: `python3 --version`
- [ ] Poetry instalado: `poetry --version`
- [ ] Docker Desktop instalado (opcional): `docker --version`
- [ ] GitHub CLI instalado: `gh --version`

---

## Día 1-2: Setup del proyecto

### Tarea 1.1: Inicializar repositorio Python

```bash
cd ~/Desktop/git/Navas_Bio_Century/dynafold_hub

# Inicializar Poetry
poetry init --no-interaction \
    --name "dynafold-hub" \
    --description "Unified platform for open-source AI drug discovery models" \
    --author "Sergio León <sergio@dynafold.io>" \
    --license "MIT" \
    --python "^3.11"

# Dependencias base
poetry add streamlit pydantic fastapi
poetry add biotite gemmi mdanalysis
poetry add py3Dmol numpy pandas
poetry add typer rich  # CLI bonito

# Dev dependencies
poetry add --group dev pytest pytest-cov pytest-asyncio
poetry add --group dev black ruff mypy pre-commit
poetry add --group dev ipykernel jupyter

# Crear estructura
mkdir -p src/dynafold_hub/{adapters,orchestration,ui,api,utils,data}
mkdir -p tests/{unit,integration,fixtures}
touch src/dynafold_hub/__init__.py
touch src/dynafold_hub/adapters/__init__.py
touch src/dynafold_hub/orchestration/__init__.py
```

**Done cuando**: `poetry run python -c "import dynafold_hub"` funciona

### Tarea 1.2: Configurar pre-commit hooks

```bash
# Crear .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix]
EOF

poetry run pre-commit install
poetry run pre-commit autoupdate
```

**Done cuando**: `git commit -m "test"` ejecuta los hooks sin errores

### Tarea 1.3: Crear README + LICENSE + estructura base

```bash
# README.md ya existe (creado en sesión planificación)
# Verificar contenido y ajustar si necesario

# LICENSE
curl -o LICENSE https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt
# Editar año y nombre

# .github/workflows/ci.yml
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install Poetry
        run: pipx install poetry
      - name: Install dependencies
        run: poetry install
      - name: Lint with ruff
        run: poetry run ruff check src/ tests/
      - name: Format check with black
        run: poetry run black --check src/ tests/
      - name: Type check with mypy
        run: poetry run mypy src/
      - name: Test with pytest
        run: poetry run pytest tests/ --cov=src/dynafold_hub
EOF

# .env.example
cat > .env.example << 'EOF'
# AlphaFold Server API
ALPHAFOLD_SERVER_API_KEY=

# Chai-1 settings
CHAI1_DEVICE=cpu  # or cuda
CHAI1_CACHE_DIR=./cache/chai1

# Boltz-2 settings
BOLTZ2_DEVICE=cpu

# Database (Phase 2)
DATABASE_URL=

# Storage (Phase 2)
S3_BUCKET=
EOF
```

**Done cuando**: Estructura mínima existe + CI corre en GitHub Actions

### Tarea 1.4: Crear repo en GitHub

```bash
# Asumiendo username de Sergio en GitHub
# Confirmar primero con él

gh repo create SergioNotionHQ/dynafold-hub \
    --public \
    --description "Unified platform for open-source AI drug discovery models" \
    --source=. \
    --remote=origin \
    --push

# Configurar topics
gh api repos/SergioNotionHQ/dynafold-hub \
    --method PATCH \
    --field topics='["drug-discovery","ai","alphafold","protein-structure","chai-discovery","bioinformatics","machine-learning","python"]'
```

**Done cuando**: Repo público accesible en https://github.com/SergioNotionHQ/dynafold-hub

---

## Día 3-4: Architecture skeleton

### Tarea 2.1: Implementar `BaseModelAdapter` (ABC)

Archivo: `src/dynafold_hub/adapters/base.py`

```python
"""Base abstract class for all model adapters."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path

import numpy as np


class TaskType(Enum):
    """Types of tasks supported by adapters."""
    STRUCTURE_PREDICTION = "structure_prediction"
    PROTEIN_LIGAND_DOCKING = "protein_ligand_docking"
    PROTEIN_DESIGN = "protein_design"
    ANTIBODY_DESIGN = "antibody_design"
    SEQUENCE_DESIGN = "sequence_design"


@dataclass
class PredictionInput:
    """Standardized input for any model."""
    sequence: Optional[str] = None
    ligand_smiles: Optional[str] = None
    receptor_pdb: Optional[Path] = None
    task: TaskType = TaskType.STRUCTURE_PREDICTION
    extra_params: dict = field(default_factory=dict)


@dataclass
class StructurePrediction:
    """Standardized structure prediction output."""
    model_name: str
    coordinates: np.ndarray  # (N_atoms, 3)
    atom_names: list[str]
    residue_ids: list[int]
    residue_names: list[str]
    confidence_per_residue: Optional[np.ndarray] = None  # plDDT-like
    pae_matrix: Optional[np.ndarray] = None  # Predicted Aligned Error
    metadata: dict = field(default_factory=dict)

    def to_pdb(self, output_path: Path) -> None:
        """Write to PDB file."""
        # Implementation using biotite
        raise NotImplementedError


@dataclass
class DockingPrediction:
    """Standardized docking output."""
    model_name: str
    poses: list[StructurePrediction]
    binding_energies: list[float]  # kcal/mol
    confidence_scores: list[float]
    metadata: dict = field(default_factory=dict)


class BaseModelAdapter(ABC):
    """Abstract base class for all model adapters."""

    name: str = "base"
    supported_tasks: list[TaskType] = []
    requires_gpu: bool = False

    @abstractmethod
    def predict_structure(
        self,
        input_data: PredictionInput,
    ) -> StructurePrediction:
        """Predict structure for given input."""
        raise NotImplementedError

    def predict_docking(
        self,
        input_data: PredictionInput,
    ) -> DockingPrediction:
        """Predict protein-ligand docking. Override if supported."""
        raise NotImplementedError(
            f"{self.name} does not support docking prediction"
        )

    @classmethod
    def is_available(cls) -> bool:
        """Check if this adapter can be used in current environment."""
        return True  # Override in subclasses

    @classmethod
    def get_info(cls) -> dict:
        """Return adapter metadata."""
        return {
            "name": cls.name,
            "supported_tasks": [t.value for t in cls.supported_tasks],
            "requires_gpu": cls.requires_gpu,
            "available": cls.is_available(),
        }
```

**Tests**: `tests/unit/adapters/test_base.py`

```python
import pytest
from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    TaskType,
    PredictionInput,
)


def test_base_adapter_cant_be_instantiated():
    with pytest.raises(TypeError):
        BaseModelAdapter()


def test_prediction_input_minimal():
    inp = PredictionInput(sequence="MGKLST")
    assert inp.sequence == "MGKLST"
    assert inp.task == TaskType.STRUCTURE_PREDICTION


def test_task_type_enum():
    assert TaskType.STRUCTURE_PREDICTION.value == "structure_prediction"
    assert len(TaskType) >= 5
```

**Done cuando**: tests pasan + base class importable

### Tarea 2.2: Crear utilities básicas

Archivo: `src/dynafold_hub/utils/parsers.py`

```python
"""Parsers for structural biology formats."""
from pathlib import Path
import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx


def load_structure_pdb(path: Path):
    """Load PDB file into biotite AtomArray."""
    pdb_file = pdb.PDBFile.read(str(path))
    return pdb.get_structure(pdb_file, model=1)


def load_structure_cif(path: Path):
    """Load CIF/mmCIF file."""
    cif_file = pdbx.CIFFile.read(str(path))
    return pdbx.get_structure(cif_file, model=1)


def auto_load(path: Path):
    """Auto-detect format and load."""
    suffix = path.suffix.lower()
    if suffix == ".pdb":
        return load_structure_pdb(path)
    elif suffix in [".cif", ".mmcif"]:
        return load_structure_cif(path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")
```

**Done cuando**: parsea correctamente un PDB de ejemplo (usar 6LU7 que ya tenemos)

---

## Día 5-7: Primer adapter (Chai-1)

### Tarea 3.1: Instalar Chai-1

```bash
# Chai-1 puede ser pesado. Verificar primero:
poetry add chai_lab

# Si falla por GPU, instalar versión CPU:
poetry run pip install chai-lab[cpu] --extra-index-url https://download.pytorch.org/whl/cpu

# Test básico de instalación
poetry run python -c "
from chai_lab.chai1 import run_inference
print('Chai-1 importable')
"
```

**Posibles problemas**:
- Chai-1 puede requerir CUDA → tener fallback documentado
- Pesos del modelo se descargan en primer uso (varios GB)
- En Mac M1/M2, posible incompatibilidad con algunos componentes

**Done cuando**: import funciona + descarga inicial de pesos completa

### Tarea 3.2: Implementar `Chai1Adapter`

Archivo: `src/dynafold_hub/adapters/chai1.py`

```python
"""Chai-1 model adapter.

Chai-1 is an open-source structure prediction model from Chai Discovery,
matching AlphaFold 3 performance on PoseBusters.

Reference: https://github.com/chaidiscovery/chai-lab
License: Apache 2.0
"""
import tempfile
from pathlib import Path
from typing import Optional

import numpy as np

from dynafold_hub.adapters.base import (
    BaseModelAdapter,
    PredictionInput,
    StructurePrediction,
    TaskType,
)


class Chai1Adapter(BaseModelAdapter):
    """Adapter for Chai-1 structure prediction model."""

    name = "chai-1"
    supported_tasks = [
        TaskType.STRUCTURE_PREDICTION,
        TaskType.PROTEIN_LIGAND_DOCKING,
    ]
    requires_gpu = False  # Works on CPU but slow

    def __init__(self, device: str = "auto", cache_dir: Optional[Path] = None):
        self.device = self._resolve_device(device)
        self.cache_dir = cache_dir or Path.home() / ".cache" / "dynafold_hub" / "chai1"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_device(self, device: str) -> str:
        """Resolve device string to actual device."""
        if device == "auto":
            try:
                import torch
                return "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                return "cpu"
        return device

    def predict_structure(
        self,
        input_data: PredictionInput,
    ) -> StructurePrediction:
        """Run Chai-1 inference."""
        if not input_data.sequence:
            raise ValueError("Chai-1 requires a sequence input")

        # Implementation:
        # 1. Write FASTA from input
        # 2. Call chai_lab.run_inference
        # 3. Parse output CIF
        # 4. Return StructurePrediction

        from chai_lab.chai1 import run_inference

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            fasta_path = tmp_path / "input.fasta"
            fasta_path.write_text(f">query\n{input_data.sequence}\n")

            # Run inference
            output_path = tmp_path / "output"
            output_path.mkdir()

            result = run_inference(
                fasta_file=fasta_path,
                output_dir=output_path,
                num_diffn_timesteps=200,
                seed=42,
                device=self.device,
                use_esm_embeddings=True,
            )

            # Parse first model
            cif_files = sorted(output_path.glob("*.cif"))
            if not cif_files:
                raise RuntimeError("Chai-1 produced no output")

            from dynafold_hub.utils.parsers import load_structure_cif
            structure = load_structure_cif(cif_files[0])

            return StructurePrediction(
                model_name="chai-1",
                coordinates=structure.coord,
                atom_names=list(structure.atom_name),
                residue_ids=list(structure.res_id),
                residue_names=list(structure.res_name),
                confidence_per_residue=None,  # TODO: extract from result
                metadata={"n_models_generated": len(cif_files)},
            )

    @classmethod
    def is_available(cls) -> bool:
        """Check if Chai-1 is importable."""
        try:
            import chai_lab
            return True
        except ImportError:
            return False
```

**Tests**: `tests/unit/adapters/test_chai1.py`

```python
import pytest
from dynafold_hub.adapters.chai1 import Chai1Adapter
from dynafold_hub.adapters.base import PredictionInput


@pytest.mark.skipif(not Chai1Adapter.is_available(), reason="Chai-1 not installed")
def test_chai1_availability():
    assert Chai1Adapter.is_available() is True


@pytest.mark.slow  # Mark slow tests
@pytest.mark.skipif(not Chai1Adapter.is_available(), reason="Chai-1 not installed")
def test_chai1_predict_small_protein():
    adapter = Chai1Adapter(device="cpu")
    # Small test sequence (avoid full proteins in tests)
    input_data = PredictionInput(sequence="MGKLSTAAGSALA")  # Test peptide
    result = adapter.predict_structure(input_data)
    assert result.model_name == "chai-1"
    assert len(result.coordinates) > 0
```

**Done cuando**:
- Test unit pasa
- Test slow (con Chai-1 real) pasa al menos una vez
- Documentación inline completa

### Tarea 3.3: CLI básica

Archivo: `src/dynafold_hub/cli.py`

```python
"""DYNAFOLD Hub CLI."""
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from dynafold_hub.adapters.chai1 import Chai1Adapter
from dynafold_hub.adapters.base import PredictionInput

app = typer.Typer(name="dynafold")
console = Console()


@app.command()
def info():
    """Show information about available adapters."""
    table = Table(title="DYNAFOLD Hub - Available Adapters")
    table.add_column("Model")
    table.add_column("Tasks")
    table.add_column("GPU Required")
    table.add_column("Available")

    for adapter_class in [Chai1Adapter]:
        info = adapter_class.get_info()
        table.add_row(
            info["name"],
            ", ".join(info["supported_tasks"]),
            "Yes" if info["requires_gpu"] else "No",
            "✅" if info["available"] else "❌",
        )

    console.print(table)


@app.command()
def predict(
    sequence: str = typer.Argument(..., help="Protein sequence"),
    model: str = typer.Option("chai-1", help="Model to use"),
    output: Path = typer.Option("output.pdb", help="Output file"),
):
    """Predict structure for a given sequence."""
    adapters = {"chai-1": Chai1Adapter}
    if model not in adapters:
        console.print(f"[red]Unknown model: {model}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Running {model} on sequence of length {len(sequence)}...[/cyan]")
    adapter = adapters[model]()
    input_data = PredictionInput(sequence=sequence)

    with console.status("Running inference..."):
        result = adapter.predict_structure(input_data)

    console.print(f"[green]✓ Predicted {len(result.coordinates)} atoms[/green]")
    # TODO: save to PDB
    console.print(f"Output: {output}")


if __name__ == "__main__":
    app()
```

Añadir al `pyproject.toml`:
```toml
[tool.poetry.scripts]
dynafold = "dynafold_hub.cli:app"
```

**Done cuando**:
- `poetry run dynafold info` muestra tabla
- `poetry run dynafold predict MGKLST --model chai-1` corre y produce output

---

## Resumen "Definition of Done" Semana 1

Al final de la semana 1 debemos tener:

- [ ] **Repositorio GitHub público** en https://github.com/SergioNotionHQ/dynafold-hub
- [ ] **CI funcionando**: lint + tests pasan en GitHub Actions
- [ ] **`BaseModelAdapter`** implementado con tests
- [ ] **`Chai1Adapter`** funcionando end-to-end
- [ ] **CLI `dynafold info` y `dynafold predict`** operativos
- [ ] **README + LICENSE** publicados
- [ ] **`.gitignore`** completo
- [ ] **Pre-commit hooks** instalados
- [ ] **70%+ test coverage** en código nuevo
- [ ] **Documentación inicial** en `docs/`

## Riesgos identificados Semana 1

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|------------|
| Chai-1 no instala en Mac | 40% | Fallback: usar Modal o Colab para tests |
| GPU requirements bloquean development | 30% | Empezar con CPU, GPU solo para benchmarks |
| Poetry/dependency conflicts | 30% | Usar pipx para Poetry, environments aislados |
| Tiempo subestimado | 60% | Cortar features no críticos antes que extender plazo |

## Siguiente: Semana 2

Una vez completada Semana 1, ver `docs/WEEK_2_EXECUTION_PLAN.md` (a crear).

Hitos de Semana 2:
- Añadir `AlphaFold3Adapter` (vía API)
- Añadir `Boltz2Adapter`
- Crear `ConsensusEngine`
- Primera versión Streamlit UI

---

**Última actualización**: 2026-05-24 por Claude + Sergio
