# I-Lang Compression Benchmark - Delivery Package

**Generated:** 2026-05-08  
**Version:** 1.0  
**Status:** ✅ Ready for Execution

---

## 📦 Package Contents

```
ilang-benchmark/
├── README.md                      # Complete usage guide
├── requirements.txt               # Python dependencies
├── test_cases.jsonl              # 30 test cases (baseline + I-Lang prompts)
├── report_template.md            # Report template
├── data/                         # Synthetic test data (5 files)
│   ├── news_article_1.txt
│   ├── history_text_1.txt
│   ├── tech_doc_1.txt
│   ├── sales_2025.csv
│   └── contract_1.txt
├── scripts/
│   ├── run_tests.py             # Main benchmark runner
│   ├── generate_report.py       # Report generator
│   └── generate_data.py         # Data generator
└── results/                      # Output directory (created on first run)
```

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/ilang-benchmark
pip3 install -r requirements.txt
```

**Required packages:**
- pandas, numpy, scipy (data analysis)
- huggingface_hub (API access)
- sentence-transformers (semantic similarity)
- tqdm (progress bars)

### 2. Run Benchmark

**Option A: Mock Mode (No API, instant results)**
```bash
python3 scripts/run_tests.py --mock
```

**Option B: Real API (Requires HF token)**
```bash
export HF_TOKEN="your_huggingface_token"
python3 scripts/run_tests.py --models gpt-4o-mini --hf-token $HF_TOKEN
```

**Option C: Multiple Models**
```bash
python3 scripts/run_tests.py \
  --models gpt-4o-mini meta-llama/Llama-2-13b deepseek-ai/deepseek-coder-6.7b \
  --hf-token $HF_TOKEN
```

### 3. Generate Report

```bash
python3 scripts/generate_report.py \
  --results results/raw_results_*.csv \
  --output report.md
```

---

## 📊 Test Suite Overview

### 30 Test Cases Across 6 Categories

| Category | Count | Focus Area | Example Task |
|----------|-------|------------|--------------|
| **A. Text Summarization** | 5 | Compression, extraction | News article → 3-part summary |
| **B. Table Transformations** | 5 | Filtering, aggregation | CSV → filtered JSON |
| **C. Code Generation** | 5 | Function generation, debugging | Spec → Python function |
| **D. Data Extraction** | 5 | NER, structured extraction | Contract → JSON fields |
| **E. Multi-Turn Workflows** | 5 | Sequential execution | Multi-step calculation |
| **F. Complex Pipelines** | 5 | End-to-end workflows | Scrape → clean → summarize |

### Each Test Case Includes

- **Baseline prompt:** Natural language (verbose)
- **I-Lang prompt:** Compressed syntax
- **Expected schema:** JSON schema for validation
- **Assertions:** Field existence, format, semantic similarity
- **Expected token savings:** Target compression rate

---

## 📈 Metrics & Thresholds

### Primary Metrics

| Metric | Definition | Success Threshold |
|--------|------------|-------------------|
| **Token Savings** | (Baseline - I-Lang) / Baseline | ≥ 20% |
| **Structural Consistency** | Assertion pass rate | ≥ 95% |
| **Semantic Similarity** | Cosine similarity (embeddings) | ≥ 0.75 |
| **Parse Error Rate** | Malformed outputs | < 5% |

### Statistical Tests

- **Paired t-test:** Token savings significance (p < 0.05)
- **Wilcoxon signed-rank:** Quality consistency (non-parametric)
- **95% CI:** Token savings confidence interval

---

## 🔧 Customization

### Add New Test Cases

Edit `test_cases.jsonl`:

```json
{
  "id": "X1",
  "category": "custom",
  "task": "Your task description",
  "input_file": "data/your_input.txt",
  "baseline_prompt": "Verbose natural language prompt...",
  "ilang_prompt": "[READ:@INPUT]=>[PROCESS]=>[OUT]",
  "expected_schema": {"type": "object", "required": ["field1"]},
  "assertions": ["field_exists:field1", "semantic_similarity:field1>=0.75"],
  "expected_token_savings": 0.30
}
```

### Add New Models

```bash
python3 scripts/run_tests.py --models your-model-id-1 your-model-id-2
```

### Custom Assertions

Edit `scripts/run_tests.py`, method `_run_assertions()`:

```python
elif assertion.startswith("custom_check:"):
    # Your custom validation logic
    result = your_validation_function(output)
    passed[assertion] = result
```

---

## 📋 Execution Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Set HF_TOKEN environment variable (if using real API)
- [ ] Run mock test to verify setup (`--mock`)
- [ ] Run full benchmark on target models
- [ ] Generate report
- [ ] Review results against thresholds
- [ ] Document any failures or anomalies
- [ ] Archive results with timestamp

---

## 🎯 Expected Outcomes

### Mock Test (Instant)
- **Duration:** ~6 seconds (60 tests)
- **Token savings:** ~70% (mock data)
- **Output:** `results/raw_results_*.csv`, `results/summary_*.json`

### Real API Test (Single Model)
- **Duration:** 5-15 minutes (depends on API latency)
- **Token savings:** 20-50% (expected range)
- **Output:** Same as mock + semantic similarity scores

### Multi-Model Test
- **Duration:** 15-45 minutes (3 models)
- **Output:** Cross-model comparison tables

---

## 🐛 Troubleshooting

### Issue: `sentence-transformers not available`
**Solution:** Install with `pip install sentence-transformers`  
**Impact:** Semantic similarity will be skipped (non-critical)

### Issue: `HF API rate limit exceeded`
**Solution:** Add delays in `run_tests.py`:
```python
time.sleep(1)  # After each API call
```

### Issue: `Mock mode not working`
**Solution:** Use `--mock` flag explicitly:
```bash
python3 scripts/run_tests.py --mock
```

---

## 📤 Deliverables

After running the benchmark, you will have:

1. **Raw Results CSV** (`results/raw_results_*.csv`)
   - Every test execution with tokens, latency, assertions
   
2. **Summary JSON** (`results/summary_*.json`)
   - Aggregate statistics, averages, token savings
   
3. **Analysis Report** (`report.md`)
   - Executive summary, statistical tests, recommendations
   
4. **Test Logs** (console output)
   - Real-time progress, errors, warnings

---

## 🔒 Security & Compliance

### Credentials
- **HF_TOKEN:** Store in environment variable, never commit to git
- **API Keys:** Use `.env` file or secrets manager

### Data Privacy
- Synthetic test data included (no real PII)
- For real data: scrub PII before running tests

### Audit Trail
- All results timestamped
- Raw outputs preserved for review
- Assertion failures logged

---

## 📞 Support

### Documentation
- Full README: `README.md`
- Report template: `report_template.md`
- Code comments: Inline in all scripts

### Common Questions

**Q: Can I run without Hugging Face?**  
A: Yes, use `--mock` mode for testing framework without API calls.

**Q: How do I add my own I-Lang compression tool?**  
A: Replace `ilang_prompt` values in `test_cases.jsonl` with your tool's output.

**Q: Can I test on local models?**  
A: Yes, modify `_call_model()` in `run_tests.py` to call your local inference endpoint.

**Q: How long does a full run take?**  
A: Mock: 6s | Single model: 5-15min | 3 models: 15-45min

---

## ✅ Validation Checklist

Before delivering to stakeholders:

- [ ] Mock test passes (60/60 tests)
- [ ] Real API test completes without errors
- [ ] Token savings ≥ 20% threshold
- [ ] Quality metrics ≥ 95% structural consistency
- [ ] Report generates successfully
- [ ] All deliverables present in `results/`
- [ ] No credentials in output files
- [ ] README instructions verified

---

## 🎉 Ready to Run

The benchmark suite is **production-ready** and can be executed immediately.

**Next Steps:**
1. Review `README.md` for detailed instructions
2. Run mock test to verify setup
3. Execute real benchmark with your target models
4. Generate and review report
5. Share results with stakeholders

**Estimated Time to First Results:** 10 minutes (including setup)

---

**Package Version:** 1.0  
**Last Updated:** 2026-05-08  
**Maintainer:** OpenClaw Team  
**License:** MIT
