# I-Lang v5.0 Judgment Layer — Learnability Benchmark

A reproducible test of one specific scientific claim from **SPEC-v5.0-PRE + PATCH-1**:

> Judgment can be modeled as vector composition over an 11-dimensional behavioral
> manifold, and the reference mapping `f_v5` (11-dim vector → decision mode) is
> mechanically well-defined.

If that mapping is real and internally consistent, a plain supervised learner must
be able to recover it from `(vector, mode)` pairs. This benchmark tests exactly that,
end to end, with every number reproducible from a single command.

## Result

| metric | value |
|---|---|
| synthetic pairs | 24,000 |
| decision modes | 7 (M2–M8) |
| majority-class baseline | 0.353 |
| logistic regression (linearity probe) | 0.631 |
| **HistGradientBoosting (recoverability)** | **0.965** |
| lift over baseline | **+0.613** |
| **official JCS conformance** | **0.986** |
| **official L2 gate** | **PASS** |

Seed 42. Reproduce: `python3 learnability.py --n 24000 --seed 42`.

## What this proves — and what it does not

This benchmark deliberately **isolates the judgment layer from the extraction layer.**
The input vectors are the official validator's own synthetic samples, not vectors a
language model extracted from text. That separation is the point.

**It proves:** `f_v5` as frozen in PATCH-1 is a well-formed, learnable decision
surface. A commodity gradient-boosted tree recovers it far above the majority
baseline and its predictions pass the official JCS conformance gate. The v5.0 claim
that "judgment is vector composition" is, at the judgment-layer level, mechanically
true and reproducible — not just asserted.

**It does not prove:** that a language model can extract *accurate* 11-dim vectors
from free-form text. That is a different, harder question — the **extraction layer** —
and it is benchmarked separately once a base model is selected. A perfect judgment
layer fed noisy vectors still judges badly; this experiment says nothing about that
noise, on purpose.

This honesty is the design. The judgment engine and the language layer are two
decoupled components, and conflating them is how a benchmark ends up reporting a
number it did not actually measure.

## Two-layer architecture (context)

```
  free text ──► [ extraction layer ]  ──► 11-dim vector ──► [ judgment layer ] ──► decision mode
                 (a language base model,                      (this benchmark;
                  benchmarked separately)                      LimiX-class engine at inference)
```

- **Extraction layer** — a language model turning input into the 11 dimensions
  (`int, cap, csq, rel, cer, aut, rev, evd, sov, ine, ext`). Base-model choice and
  its extraction accuracy are a separate benchmark.
- **Judgment layer** — maps the vector to a decision mode and score. This is a
  small-sample tabular task, which is precisely what structured-data foundation
  models (e.g. LimiX, Apache-2.0) are built for. This benchmark shows the mapping
  is learnable even by a plain GBDT; a pretrained tabular model needs few or no
  training pairs.

## Files

- `learnability.py` — the experiment. Emits pairs from the frozen validator, trains
  two students, scores through the official JCS eval, writes a results JSON.
- `ilang_judge_validator.py` — version-locked copy of the official validator from
  `ilang-ai/ilang-spec`. Stdlib-only. Source of truth for `f_v5` and the JCS metric.
- `results/learnability_result.json` — machine-readable result with full provenance
  and an explicit `proves` / `does_not_prove` block.
- `requirements.txt` — numpy + scikit-learn.

## Run it yourself

```bash
cd judgment
pip install -r requirements.txt
python3 learnability.py                 # N=24000, seed=42
python3 learnability.py --quick         # N=6000 fast run
python3 learnability.py --n 40000 --seed 7
```

The script exits non-zero if recoverability is weak or the JCS gate fails, so it
doubles as a conformance check on any future edit to `f_v5`.
