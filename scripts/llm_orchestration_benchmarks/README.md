# VITA LLM Orchestration & Container Benchmarks (Week 4)

This directory contains benchmark and diagnostic scripts from **Week 4**, documenting our evolution from monolithic cloud prompt bloat to containerized local intent orchestration on the Raspberry Pi 4.

## Scripts Included

1. **`01_bloated_cloud_prompt_test.py`**:
   - Demonstrates the early monolithic approach: sending full user transcripts to OpenAI with a massive 1,600-token system prompt containing clinical rules, formatting directives, and conversational tone guards.
   - Shows token explosion, latency lag, and conversational fluff.

2. **`02_structured_intent_template_router.py`**:
   - Demonstrates the architectural pivot: demoting the LLM from a free-form chatbot to a strict **Orchestration Layer**.
   - Extracts structured intent (`LOG_FOOD`, `QUERY_NUTRITION`) and entity slots into JSON, then injects them into verified deterministic templates.

3. **`03_local_qwen_container_benchmark.py`**:
   - Documents why we moved from bare-metal to Docker containers to prevent library dependency collisions.
   - Benchmarks micro-models (TinyLlama vs SmolLM vs Qwen2.5) for JSON schema compliance.
   - Measures Qwen2.5-0.5B token throughput on the Raspberry Pi 4's 4 Cortex-A72 CPU cores (~3.6 tok/s), proving the architecture is rock-solid even while highlighting the CPU latency bottleneck.

## Running Benchmarks

```bash
python3 01_bloated_cloud_prompt_test.py
python3 02_structured_intent_template_router.py
python3 03_local_qwen_container_benchmark.py
```
