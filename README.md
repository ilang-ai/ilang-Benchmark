# I-Lang Compression Benchmark

Comprehensive testing framework for evaluating I-Lang prompt compression against baseline natural language prompts.

## Sub-benchmarks

- **[judgment/](judgment/)** — I-Lang v5.0 judgment-layer learnability. Tests whether the PATCH-1 reference mapping f_v5 (11-dim vector to decision mode) is a learnable decision surface. Result: a plain GBDT recovers it at 0.965 vs 0.353 baseline, official JCS 0.986, L2 PASS. Isolates the judgment layer from the extraction layer by design.

## Overview

This benchmark suite tests I-Lang compression across 30 representative tasks in 6 categories:
- **A. Text Summarization** (5 tasks)
- **B. Table Transformations** (5 tasks)
- **C. Code Generation** (5 tasks)
- **D. Data Extraction** (5 tasks)
- **E. Multi-Turn Workflows** (5 tasks)
- **F. Complex Pipelines** (5 tasks)

## Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/ilang-benchmark
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Credentials

```bash
export HF_TOKEN="your_huggingface_token"
```

### 3. Run Tests

```bash
# Run with mock responses (no API calls)
python scripts/run_tests.py --mock

# Run with real API
python scripts/run_tests.py --models gpt-4o-mini --hf-token $HF_TOKEN

# Run multiple models
python scripts/run_tests.py --models gpt-4o-mini meta-llama/Llama-2-13b deepseek-ai/deepseek-coder-6.7b
```

### 4. Generate Report

```bash
python scripts/generate_report.py --results results/raw_results_*.csv --output report.md
```

## Test Suite Structure

```
ilang-benchmark/
├── test_cases.jsonl          # 30 test cases (baseline + I-Lang prompts)
├── data/                      # Test input files (generated on first run)
├── scripts/
│   ├── run_tests.py          # Main test runner
│   ├── generate_report.py    # Report generator
│   └── generate_data.py      # Synthetic data generator
├── results/                   # Test outputs
│   ├── raw_results_*.csv     # Detailed results
│   └── summary_*.json        # Summary statistics
├── report_template.md         # Report template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Test Case Format

Each test case in `test_cases.jsonl` contains:

```json
{
  "id": "A1",
  "category": "text_summary",
  "task": "Summarize news article into 3-part structure",
  "input_file": "data/news_article_1.txt",
  "baseline_prompt": "Read the following news article and provide...",
  "ilang_prompt": "[READ:@INPUT]=>[SUM|fields=summary,impact,next_steps|format=json]=>[OUT]",
  "expected_schema": {"type": "object", "required": ["summary", "impact", "next_steps"]},
  "assertions": ["field_exists:summary", "semantic_similarity:summary>=0.75"],
  "expected_token_savings": 0.35
}
```

## Metrics

### Token Savings
- **Input tokens:** Prompt length
- **Output tokens:** Response length
- **Total tokens:** Input + Output
- **Savings rate:** (Baseline - I-Lang) / Baseline

### Quality Metrics
- **Structural consistency:** Field-level assertion pass rate
- **Semantic similarity:** Cosine similarity of embeddings (baseline vs I-Lang outputs)
- **Parse error rate:** Percentage of malformed outputs

### Performance
- **Latency:** Time from request to complete response
- **Throughput:** Tests per second

## Statistical Analysis

The benchmark performs:
- **Paired t-test:** Token savings significance
- **Wilcoxon signed-rank test:** Quality consistency (non-parametric)
- **Cohen's kappa:** Cross-model agreement
- **95% confidence intervals:** Token savings estimates

## Thresholds

### Success Criteria
- ✅ Token savings ≥ 20% (average)
- ✅ Structural consistency ≥ 95%
- ✅ Semantic similarity ≥ 0.75
- ✅ Parse error rate < 5%

### Warning Thresholds
- ⚠️ Token savings < 20%
- ⚠️ Structural consistency < 90%
- ⚠️ Semantic similarity drop > 0.05 (p < 0.05)
- ⚠️ Parse error rate > 5%

## Customization

### Add New Test Cases

Edit `test_cases.jsonl`:

```json
{"id":"X1","category":"custom","task":"Your task","baseline_prompt":"...","ilang_prompt":"...","expected_schema":{...},"assertions":[...]}
```

### Add New Models

```bash
python scripts/run_tests.py --models your-model-id-1 your-model-id-2
```

### Custom Assertions

Edit `scripts/run_tests.py` and add to `_run_assertions()` method.

## CI Integration

### GitHub Actions Example

```yaml
name: I-Lang Benchmark

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python scripts/run_tests.py --models gpt-4o-mini --hf-token ${{ secrets.HF_TOKEN }}
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
      - run: python scripts/generate_report.py --results results/raw_results_*.csv
      - uses: actions/upload-artifact@v3
        with:
          name: benchmark-report
          path: report.md
```

## Troubleshooting

### Mock Mode Not Working
```bash
# Force mock mode
python scripts/run_tests.py --mock
```

### API Rate Limits
```bash
# Add delays between requests (edit run_tests.py)
time.sleep(1)  # Add after each API call
```

### Missing Dependencies
```bash
pip install sentence-transformers huggingface_hub pandas numpy scipy
```

## License

MIT License - See LICENSE file

## Contact

For questions or issues, contact the OpenClaw team or open an issue on GitHub.

---

**Version:** 1.0  
**Last Updated:** 2026-05-08  
**Maintainer:** OpenClaw
