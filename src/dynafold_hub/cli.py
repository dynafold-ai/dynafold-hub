"""DYNAFOLD Hub CLI.

Command-line interface for using DYNAFOLD Hub from the terminal.

Examples:
    dynafold info                          # List available adapters
    dynafold predict MGKLSTAA              # Predict structure
    dynafold predict-file input.fasta      # Predict from FASTA file
    dynafold launch-ui                     # Launch Streamlit web app
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dynafold_hub import __version__
from dynafold_hub.adapters import (
    PredictionInput,
    TaskType,
    get_adapter,
    list_available_adapters,
)
from dynafold_hub.utils import parse_fasta, validate_protein_sequence

app = typer.Typer(
    name="dynafold",
    help="DYNAFOLD Hub — Unified platform for AI drug discovery models",
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def version() -> None:
    """Show DYNAFOLD Hub version."""
    console.print(f"[bold cyan]DYNAFOLD Hub[/] v{__version__}")


@app.command()
def info() -> None:
    """Show information about available model adapters."""
    console.print(
        Panel(
            "[bold cyan]DYNAFOLD Hub[/] — Available Model Adapters",
            border_style="cyan",
        )
    )

    adapters = list_available_adapters()

    if not adapters:
        console.print(
            "[yellow]No adapters configured yet. " "This is expected in early development.[/]"
        )
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan")
    table.add_column("Tasks", style="green")
    table.add_column("GPU?", justify="center")
    table.add_column("Available", justify="center")
    table.add_column("License")

    for adapter in adapters:
        gpu = "✓" if adapter["requires_gpu"] else "—"
        avail = "[green]✓[/]" if adapter["available"] else "[red]✗[/]"
        tasks_short = ", ".join(t.replace("_", " ") for t in adapter["supported_tasks"][:2])
        table.add_row(
            adapter["name"],
            tasks_short,
            gpu,
            avail,
            adapter.get("license", "Unknown"),
        )

    console.print(table)
    console.print(
        "\n[dim]Install adapters: " "[bold]poetry install --extras all[/] for full setup[/]"
    )


@app.command()
def predict(
    sequence: str = typer.Argument(..., help="Protein sequence (1-letter codes)"),
    model: str = typer.Option(
        "chai-1",
        "--model",
        "-m",
        help="Model to use (chai-1, alphafold-3, boltz-2)",
    ),
    output: Path = typer.Option(
        Path("prediction.json"),
        "--output",
        "-o",
        help="Output file path",
    ),
) -> None:
    """Predict 3D structure for a given amino acid sequence."""
    try:
        sequence = validate_protein_sequence(sequence)
    except ValueError as e:
        console.print(f"[red]Invalid sequence: {e}[/]")
        raise typer.Exit(1) from e

    console.print(
        f"[cyan]→[/] Running [bold]{model}[/] on sequence of " f"length [bold]{len(sequence)}[/]..."
    )

    try:
        adapter = get_adapter(model)
    except ValueError as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Failed to load adapter: {e}[/]")
        raise typer.Exit(1) from e

    input_data = PredictionInput(
        sequence=sequence,
        task=TaskType.STRUCTURE_PREDICTION,
    )

    try:
        with console.status(f"[bold green]Running {model} inference..."):
            result = adapter.predict_structure(input_data)
    except NotImplementedError as e:
        console.print(f"[yellow]⚠ {e}[/]")
        console.print("[dim]This adapter is being implemented in upcoming weeks.[/]")
        raise typer.Exit(2) from e
    except Exception as e:
        console.print(f"[red]Prediction failed: {e}[/]")
        raise typer.Exit(1) from e

    console.print(
        f"[green]✓[/] Predicted [bold]{result.n_atoms}[/] atoms, "
        f"[bold]{result.n_residues}[/] residues"
    )
    if result.mean_confidence() is not None:
        console.print(f"  Mean confidence: [bold]{result.mean_confidence():.2f}[/]")
    console.print(f"  Output: [cyan]{output}[/]")


@app.command(name="predict-file")
def predict_file(
    fasta: Path = typer.Argument(..., help="Path to FASTA file"),
    model: str = typer.Option("chai-1", "--model", "-m"),
) -> None:
    """Predict structures for all sequences in a FASTA file."""
    if not fasta.exists():
        console.print(f"[red]File not found: {fasta}[/]")
        raise typer.Exit(1)

    records = parse_fasta(fasta.read_text())
    console.print(f"[cyan]Loaded {len(records)} sequence(s) from {fasta}[/]")

    for header, seq in records:
        console.print(f"\n[bold]Predicting {header}...[/]")
        predict(sequence=seq, model=model, output=Path(f"{header}.json"))


@app.command(name="launch-ui")
def launch_ui(
    port: int = typer.Option(8501, help="Port for Streamlit"),
) -> None:
    """Launch the DYNAFOLD Hub web UI (Streamlit)."""
    try:
        import streamlit  # noqa: F401
    except ImportError as e:
        console.print("[red]Streamlit not installed.[/] Run: [bold]poetry install --extras ui[/]")
        raise typer.Exit(1) from e

    import subprocess

    app_path = Path(__file__).parent / "ui" / "app.py"
    if not app_path.exists():
        console.print(f"[yellow]UI not yet implemented at {app_path}[/]")
        console.print("[dim]Coming in Week 2-3 of development.[/]")
        raise typer.Exit(2)

    console.print(f"[green]Launching Streamlit on port {port}...[/]")
    subprocess.run(
        [
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(port),
        ]
    )


def main() -> int:
    """Entry point for CLI."""
    try:
        app()
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
