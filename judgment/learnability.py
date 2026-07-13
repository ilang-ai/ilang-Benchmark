#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I-Lang v5.0 Judgment Layer — Learnability Benchmark
====================================================

Scientific claim under test
---------------------------
SPEC-v5.0-PRE defines judgment as vector composition over an 11-dimensional
behavioral manifold, and PATCH-1 makes the reference mapping f_v5 (11-dim
vector -> decision mode) mechanically defined. If that mapping is real and
consistent, a standard supervised learner must be able to recover it from
(vector, mode) pairs. This script tests exactly that, end to end, with every
number reproducible from one command.

What it proves (and does not)
-----------------------------
PROVES:  the PATCH-1 reference function f_v5 is a well-formed, learnable
         decision surface — a learner recovers it far above the majority
         baseline, and its predictions pass the official JCS conformance gate.
DOES NOT PROVE: that a language model can extract accurate 11-dim vectors
         from free text (that is the extraction-layer question, benchmarked
         separately once a base model is chosen). Here the vectors are the
         validator's own synthetic samples, so this isolates the judgment
         layer from the extraction layer on purpose.

Pipeline
--------
1. Emit N synthetic (vector, mode) pairs from the frozen official validator.
2. Train two students: LogisticRegression (linear separability probe) and
   HistGradientBoosting (the real recoverability result).
3. Report accuracy vs the majority-class baseline.
4. Re-score the GBDT predictions through the official JCS eval and assert L2.
5. Write a machine-readable results JSON + a human-readable summary.

Usage
-----
  python3 learnability.py                 # default N=24000, seed=42
  python3 learnability.py --n 40000 --seed 7
  python3 learnability.py --quick         # N=6000 for a fast smoke run

Dependencies: numpy, scikit-learn (see judgment/requirements.txt).
The validator itself is stdlib-only and version-locked in this folder.
"""

import argparse
import json
import subprocess
import sys
import os
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(HERE, "ilang_judge_validator.py")
DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]


def emit_pairs(n, seed):
    """Call the frozen official validator to emit N synthetic (vector, mode) pairs."""
    out = subprocess.run(
        [sys.executable, VALIDATOR, "--sample", str(n)],
        capture_output=True, text=True, check=True,
    ).stdout
    X, y = [], []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        v = d["v"]
        X.append([v[k] for k in DIMS])
        y.append(d["mode"])
    return np.array(X, dtype=float), np.array(y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=24000, help="number of synthetic pairs")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--quick", action="store_true", help="fast run, N=6000")
    ap.add_argument("--out", default=os.path.join(HERE, "results", "learnability_result.json"))
    args = ap.parse_args()
    if args.quick:
        args.n = 6000

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import HistGradientBoostingClassifier

    print(f"[1/5] emitting {args.n} synthetic (vector, mode) pairs from official validator...")
    X, y = emit_pairs(args.n, args.seed)
    modes, counts = np.unique(y, return_counts=True)
    dist = {m: int(c) for m, c in zip(modes, counts)}
    print(f"      got {len(X)} pairs across {len(modes)} modes: {dist}")

    print("[2/5] splitting 75/25 stratified...")
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=args.seed, stratify=y
    )

    maj = max(set(list(ytr)), key=list(ytr).count)
    base_acc = float((yte == maj).mean())
    print(f"      majority-class baseline ({maj}): {base_acc:.4f}")

    print("[3/5] training LogisticRegression (linear separability probe)...")
    lr = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
    lr_acc = float(lr.score(Xte, yte))
    print(f"      logistic accuracy: {lr_acc:.4f}")

    print("[4/5] training HistGradientBoosting (recoverability result)...")
    gb = HistGradientBoostingClassifier(random_state=args.seed).fit(Xtr, ytr)
    gb_acc = float(gb.score(Xte, yte))
    print(f"      gbdt accuracy:     {gb_acc:.4f}")

    # Write GBDT predictions in the official eval JSONL format, then score via validator.
    preds = gb.predict(Xte)
    eval_path = os.path.join(HERE, "results", "eval_gbdt.jsonl")
    with open(eval_path, "w", encoding="utf-8") as f:
        for xe, yg, yp in zip(Xte, yte, preds):
            v = {k: round(float(val), 2) for k, val in zip(DIMS, xe)}
            f.write(json.dumps(
                {"gold_v": v, "pred_v": v, "gold_mode": yg, "pred_mode": yp, "boundary": False}
            ) + "\n")

    print("[5/5] scoring GBDT predictions through official JCS eval...")
    jcs_out = subprocess.run(
        [sys.executable, VALIDATOR, "--eval", eval_path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    print(f"      {jcs_out}")

    jcs = None
    l2_pass = None
    for tok in jcs_out.replace("(", " ").replace(")", " ").split():
        if tok.startswith("JCS="):
            jcs = float(tok.split("=")[1])
        if tok.startswith("L2_pass="):
            l2_pass = tok.split("=")[1]

    result = {
        "claim": "PATCH-1 reference function f_v5 (11-dim vector -> decision mode) is a learnable decision surface",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_pairs": int(len(X)),
        "seed": args.seed,
        "mode_distribution": dist,
        "majority_baseline_acc": round(base_acc, 4),
        "logistic_acc": round(lr_acc, 4),
        "gbdt_acc": round(gb_acc, 4),
        "gbdt_lift_over_baseline": round(gb_acc - base_acc, 4),
        "official_jcs": jcs,
        "official_l2_pass": l2_pass,
        "validator_source": "ilang-ai/ilang-spec :: ilang_judge_validator.py (version-locked copy)",
        "interpretation": {
            "isolates": "judgment layer only; vectors are the validator's synthetic samples, not model-extracted",
            "proves": "f_v5 is a well-formed learnable mapping; a plain GBDT recovers it and passes the JCS gate",
            "does_not_prove": "that a language model can extract accurate 11-dim vectors from free text",
            "next": "extraction-layer benchmark once a base model is selected (see two-layer architecture)",
        },
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print(f"  f_v5 learnability: gbdt {gb_acc:.3f} vs baseline {base_acc:.3f}"
          f"  (+{gb_acc - base_acc:.3f})")
    print(f"  official JCS: {jcs}   L2_pass: {l2_pass}")
    print(f"  result written: {os.path.relpath(args.out, HERE)}")
    print("=" * 60)
    # Non-zero exit if the mapping failed to be recovered or JCS gate failed.
    if gb_acc < base_acc + 0.10 or l2_pass != "YES":
        print("WARN: recoverability weak or JCS gate not passed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
