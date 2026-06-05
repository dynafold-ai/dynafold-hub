"""Parsers for structural biology file formats (PDB, mmCIF, FASTA)."""

from __future__ import annotations

from pathlib import Path


def load_structure(path: Path):
    """Auto-detect format and load structure.

    Args:
        path: Path to .pdb, .cif, or .mmcif file.

    Returns:
        Biotite AtomArray of the first model.

    Raises:
        ValueError: If file format is not supported.
        FileNotFoundError: If file doesn't exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Structure file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".pdb":
        return _load_pdb(path)
    if suffix in (".cif", ".mmcif"):
        return _load_cif(path)
    raise ValueError(f"Unsupported format: {suffix}. Use .pdb, .cif, or .mmcif")


def _load_pdb(path: Path):
    """Load PDB file."""
    import biotite.structure.io.pdb as pdb_io

    pdb_file = pdb_io.PDBFile.read(str(path))
    return pdb_io.get_structure(pdb_file, model=1)


def _load_cif(path: Path):
    """Load mmCIF file."""
    import biotite.structure.io.pdbx as pdbx_io

    cif_file = pdbx_io.CIFFile.read(str(path))
    return pdbx_io.get_structure(cif_file, model=1)


def parse_fasta(content: str) -> list[tuple[str, str]]:
    """Parse FASTA-format string into list of (header, sequence) tuples.

    Args:
        content: FASTA-formatted string.

    Returns:
        List of (header, sequence) pairs.

    Example:
        >>> parse_fasta(">seq1\\nMGKLSTA\\n>seq2\\nGGGAA")
        [('seq1', 'MGKLSTA'), ('seq2', 'GGGAA')]
    """
    records = []
    current_header: str | None = None
    current_seq: list[str] = []

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_header is not None:
                records.append((current_header, "".join(current_seq)))
            current_header = line[1:].strip()
            current_seq = []
        else:
            current_seq.append(line)

    if current_header is not None:
        records.append((current_header, "".join(current_seq)))

    return records


def write_fasta(sequence: str, header: str = "query") -> str:
    """Format sequence as FASTA string.

    Args:
        sequence: Amino acid sequence.
        header: FASTA header (without '>').

    Returns:
        FASTA-formatted string.
    """
    return f">{header}\n{sequence}\n"


def validate_protein_sequence(sequence: str) -> str:
    """Validate that a string is a valid protein sequence.

    Args:
        sequence: Single-letter amino acid sequence.

    Returns:
        Cleaned uppercase sequence.

    Raises:
        ValueError: If sequence contains invalid characters.
    """
    seq = sequence.strip().upper().replace(" ", "").replace("\n", "")
    valid_aa = set("ACDEFGHIKLMNPQRSTVWYX*-")
    invalid = set(seq) - valid_aa
    if invalid:
        raise ValueError(
            f"Invalid amino acid codes: {invalid}. "
            f"Use standard one-letter codes (X for unknown, - for gap)."
        )
    return seq
