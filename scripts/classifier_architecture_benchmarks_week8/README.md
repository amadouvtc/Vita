# VITA Week 8: Intent Classifier Evaluation & Pipeline Verification Suite

This test suite chronicles and verifies the architecture pivot from LLM-based intent routing to a dedicated BERT intent classifier in Week 8 of the VITA project.

## Scripts

1. **`01_llm_vs_classifier_determinism_test.py`**:
   - Executes 1,000 consecutive invocations on the exact same utterance.
   - Demonstrates how LLM prompt routing exhibits probabilistic drift and misclassifications, whereas the frozen BERT classifier achieves 100.00% deterministic consistency.

2. **`02_classifier_architectures_benchmark.py`**:
   - Compares the 4 evaluated classifier architectures:
     1. Rule-Based / RegEx Heuristics
     2. TF-IDF + Logistic Regression / SVM
     3. Transformer [CLS] Pooling + Softmax
     4. BERT Token Mean Pooling + Sigmoid Multi-Head
   - Evaluates latency, handling of subtle negations, mutual exclusivity flaws, and edge deployment suitability.

3. **`03_end_to_end_auditable_pipeline_demo.py`**:
   - Demonstrates the complete 6-stage decoupled voice architecture:
     `Audio -> STT -> BERT Classifier -> LLM Slot Extractor -> Auditable DB API -> LLM Formulator -> TTS Audio`
   - Logs an end-to-end audit trail verifying sub-5ms intent routing and zero LLM arithmetic hallucination.

## Running the Suite

```bash
python3 scripts/classifier_architecture_benchmarks_week8/01_llm_vs_classifier_determinism_test.py
python3 scripts/classifier_architecture_benchmarks_week8/02_classifier_architectures_benchmark.py
python3 scripts/classifier_architecture_benchmarks_week8/03_end_to_end_auditable_pipeline_demo.py
```
