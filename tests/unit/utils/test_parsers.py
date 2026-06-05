"""Tests for parser utilities."""

from __future__ import annotations

import pytest

from dynafold_hub.utils.parsers import (
    parse_fasta,
    validate_protein_sequence,
    write_fasta,
)


class TestParseFasta:
    """Tests for parse_fasta function."""

    def test_single_record(self):
        content = ">seq1\nMGKLSTA"
        records = parse_fasta(content)
        assert len(records) == 1
        assert records[0] == ("seq1", "MGKLSTA")

    def test_multiple_records(self):
        content = ">seq1\nMGKLSTA\n>seq2\nGGGAA"
        records = parse_fasta(content)
        assert len(records) == 2
        assert records[0] == ("seq1", "MGKLSTA")
        assert records[1] == ("seq2", "GGGAA")

    def test_multiline_sequence(self):
        content = ">seq1\nMGKL\nSTAA\nGGG"
        records = parse_fasta(content)
        assert records[0] == ("seq1", "MGKLSTAAGGG")

    def test_empty_content(self):
        records = parse_fasta("")
        assert records == []

    def test_whitespace_handling(self):
        content = ">seq1\n  MGKLSTA  \n"
        records = parse_fasta(content)
        assert records[0][1] == "MGKLSTA"


class TestWriteFasta:
    """Tests for write_fasta function."""

    def test_basic_write(self):
        result = write_fasta("MGKLSTA")
        assert result == ">query\nMGKLSTA\n"

    def test_custom_header(self):
        result = write_fasta("MGKLSTA", header="my_protein")
        assert result == ">my_protein\nMGKLSTA\n"


class TestValidateProteinSequence:
    """Tests for validate_protein_sequence."""

    def test_valid_sequence(self):
        result = validate_protein_sequence("MGKLSTA")
        assert result == "MGKLSTA"

    def test_lowercase_normalized(self):
        result = validate_protein_sequence("mgklsta")
        assert result == "MGKLSTA"

    def test_whitespace_stripped(self):
        result = validate_protein_sequence("MG KL\nSTA")
        assert result == "MGKLSTA"

    def test_invalid_characters_rejected(self):
        with pytest.raises(ValueError, match="Invalid amino acid"):
            validate_protein_sequence("MGKLZ1")

    def test_unknown_aa_allowed(self):
        # X = unknown amino acid (standard)
        result = validate_protein_sequence("MGKXLSTA")
        assert result == "MGKXLSTA"

    def test_gap_allowed(self):
        result = validate_protein_sequence("MGK-LSTA")
        assert result == "MGK-LSTA"
