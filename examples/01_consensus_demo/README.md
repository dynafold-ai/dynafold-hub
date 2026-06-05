# Consensus Demo — Cross-Model Agreement Analysis

This example shows DYNAFOLD Hub's unique value: comparing predictions from
multiple AI models to identify agreement and divergence.

## Scenario

You have predicted the structure of a 20-residue peptide using three different
state-of-the-art models:
- AlphaFold 3 (DeepMind)
- Chai-1 (Chai Discovery)
- Boltz-2 (MIT Wohlwend Lab)

Each gives you a structure with confidence scores. But:
- Do they agree?
- Which regions can you trust?
- Which regions need experimental validation?

DYNAFOLD Hub answers all of this **automatically**.

## Run the demo

```bash
# 1. Generate example PDB files (run once)
python generate_example_data.py

# 2. Run consensus analysis
dynafold compare af3.pdb chai1.pdb boltz2.pdb \
    --names "alphafold-3,chai-1,boltz-2"
```

## What you'll see

The output shows:

1. **Trust Score (0-100)** — overall confidence in the consensus
2. **Agreement fraction** — what % of residues all models agree on
3. **Divergent regions** — where models disagree (sorted by severity)
4. **Experimental recommendations** — specific wet-lab experiments to validate

## Expected output for this demo

Looking at the synthetic data:
- Most residues agree (low RMSD between models)
- Residues 8-13 show divergence (artificial "loop" region)
- AF3 and Chai-1 disagree moderately
- Boltz-2 shows critical divergence in this region

DYNAFOLD Hub flags this region as needing HDX-MS or cryo-EM validation.

## Why this matters

In real drug discovery:
- A "critical" divergent region near a binding site = **STOP, validate before designing drugs**
- Models agreeing = **PROCEED with confidence**
- Without DYNAFOLD Hub, researchers do this comparison **manually**, taking hours

DYNAFOLD Hub automates this in seconds.

## Real usage

In production, you'd use REAL predictions:
- AlphaFold 3 from [AlphaFold Server](https://alphafoldserver.com)
- Chai-1 from [Chai Discovery](https://www.chaidiscovery.com)
- Boltz-2 from [GitHub](https://github.com/jwohlwend/boltz)

Just download/run them, save as PDB files, and run `dynafold compare`.
