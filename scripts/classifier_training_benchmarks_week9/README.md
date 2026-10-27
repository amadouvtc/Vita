# VITA Week 9: Classifier Training & MLOps Pipeline Verification Suite

This test suite chronicles and verifies the training pipeline, dataset synthesis, loss formulation, and hardware acceleration implemented in Week 9 of the VITA project.

## Scripts

1. **`01_dataset_concept_and_template_generator.py`**:
   - Demonstrates concept-driven synthetic dataset generation using `taxonomy.json` and concept YAMLs.
   - Synthesizes single-sentence single-intent queries alongside multi-sentence single-intent queries (e.g., conversational preamble preceding the target question).

2. **`02_loss_and_calibration_demo.py`**:
   - Demonstrates `SymmetricBCELoss` with label smoothing ($\epsilon = 0.05$) and sub-intent loss masking.
   - Executes deterministic coordinate threshold calibration, proving how optimizing per-label thresholds lifts Macro F1.

3. **`03_gpu_vs_cpu_training_benchmark.py`**:
   - Benchmarks training throughput: CPU (240s) vs GPU (11s) on 25 epochs.
   - Explains the post-mortem fix for the NVIDIA Driver 535 vs CUDA 12.0 container mismatch.

## Running the Suite

```bash
python3 scripts/classifier_training_benchmarks_week9/01_dataset_concept_and_template_generator.py
python3 scripts/classifier_training_benchmarks_week9/02_loss_and_calibration_demo.py
python3 scripts/classifier_training_benchmarks_week9/03_gpu_vs_cpu_training_benchmark.py
```
