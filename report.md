# I-Lang Compression Benchmark — Status

**Current state:** harness complete and open. Headline numbers pending real-model runs.

The report previously published here was generated with `mock-model-1`, a pipeline
smoke test that validated the harness (30 cases, 6 categories, scoring, statistics),
not the protocol. Citing its numbers as evidence was wrong. It is archived, clearly
labeled, at [`archive/2026-05-08-mock-smoke-test.md`](archive/2026-05-08-mock-smoke-test.md),
raw outputs in `archive/results-mock-20260508/`.

## Next

Real-model runs (July 2026) across at least one Claude model, one GPT model, and one
open-weights model. Results publish here unmodified, whatever the numbers are.

## Reproduce

See README Quick Start. `scripts/run_tests.py` executes the 30-case suite against a
configured model; `scripts/generate_report.py` renders this report from `results/`.
