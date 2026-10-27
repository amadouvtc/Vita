# Week 10 Benchmarks: Same-Intent Clause Repetition & Adjudication

This directory provides standalone, reproducible Python test harnesses demonstrating how VITA solves the **repeated same-intent problem in compound utterances**:

1. **`01_same_intent_span_segmenter.py`**:
   - Tests communicative clause span segmentation on compound sentences containing two instances of `food_composition_lookup`.
   - Verifies exact start and end offsets and asserts **Rule 11 Character Slicing Integrity** (`text[start:end] == span.text`).
   - Contrasts independent multi-entity requests against multi-attribute single-food requests and comparative queries.

2. **`02_dataset_merge_vs_split_validator.py`**:
   - Implements the 12-rule semantic validation engine from VITA's production codebase (`classifier/dataset/multi_intent_validator.py`).
   - Audits 4 critical scenarios:
     - Test 1: Valid repeated same-intent query (distinct entities, passes all gates).
     - Test 2: Unmerged repeated query on the *same food* (violates Rule 3 duplicate detection and Rule 4 merge consistency).
     - Test 3: Fragmented comparative query (violates Rule 5 comparative adjudication).
     - Test 4: Character offset drift (violates Rule 11 character slicing integrity).

3. **`03_repeated_intent_pipeline_demo.py`**:
   - End-to-end execution simulation on RK3588 / Orange Pi 5:
     - Splits `"Tell me the calories in 100g of salmon, and also check the protein in 200g of chicken breast"`.
     - Extracts dual `IntentInstance`s with grounded `alim_code`s (25000 and 20005).
     - Dispatches two deterministic SQL queries to CIQUAL.
     - Synthesizes auditable response in **4.33 ms total latency**.

### Running the Benchmarks:
```bash
python3 01_same_intent_span_segmenter.py
python3 02_dataset_merge_vs_split_validator.py
python3 03_repeated_intent_pipeline_demo.py
```
