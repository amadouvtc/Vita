#!/usr/bin/env python3
"""
VITA Edge Architecture - Week 10 Benchmark Suite
Script 03: End-to-End Repeated Intent Pipeline & Edge Execution Demo

Simulates the complete VITA multi-instance edge execution pipeline:
Audio transcript -> Communicative Clause Segmentation -> Per-Clause Classification & Entity Grounding
-> Strict Merge & Adjudication -> CIQUAL Database Execution -> Unified Auditable Synthesis.
"""

import time
import json
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any

# Mock CIQUAL database table
CIQUAL_MOCK_DB = {
    25000: {
        "name": "Atlantic salmon, raw",
        "energy_kcal_100g": 208.0,
        "protein_g_100g": 20.4,
        "fat_g_100g": 13.4,
        "carbs_g_100g": 0.0,
    },
    20005: {
        "name": "Chicken breast, skinless, raw",
        "energy_kcal_100g": 110.0,
        "protein_g_100g": 31.0,
        "fat_g_100g": 1.2,
        "carbs_g_100g": 0.0,
    },
    19023: {
        "name": "Whole milk, pasteurized",
        "energy_kcal_100g": 65.0,
        "protein_g_100g": 3.3,
        "fat_g_100g": 3.6,
        "calcium_mg_100g": 120.0,
    },
}

@dataclass(frozen=True)
class ClauseSpan:
    start: int
    end: int
    text: str

@dataclass
class IntentInstanceExecution:
    rank: int
    span: ClauseSpan
    sub_intent: str
    target_nutrient: str
    entity_text: str
    alim_code: int
    quantity_g: float
    db_result: Dict[str, Any] = field(default_factory=dict)
    dispatch_plan: str = ""

def run_pipeline_demo():
    print("=" * 78)
    print("🔬 VITA BENCHMARK 03: END-TO-END REPEATED SAME-INTENT PIPELINE DEMO")
    print("=" * 78)

    user_query = "Tell me the calories in 100g of salmon, and also check the protein in 200g of chicken breast"
    print(f"\n🎙️ Incoming User Utterance:\n   \"{user_query}\"\n")

    t_start = time.perf_counter()

    # Stage 1: Communicative Clause Segmentation
    t0 = time.perf_counter()
    span1 = ClauseSpan(0, 39, "Tell me the calories in 100g of salmon")
    span2 = ClauseSpan(50, 99, "check the protein in 200g of chicken breast")
    spans = [span1, span2]
    t_seg = (time.perf_counter() - t0) * 1000

    print("Step 1: Communicative Clause Span Segmentation")
    print(f"  ⚡ Latency: {t_seg:.3f} ms")
    for idx, s in enumerate(spans, 1):
        print(f"  ├─ Clause {idx} [{s.start:02d}:{s.end:02d}]: \"{s.text}\"")

    # Stage 2: Dual Clause Classification & Entity Extraction
    t0 = time.perf_counter()
    instance1 = IntentInstanceExecution(
        rank=1,
        span=span1,
        sub_intent="food_composition_lookup",
        target_nutrient="energy_kcal_100g",
        entity_text="salmon",
        alim_code=25000,
        quantity_g=100.0,
    )
    instance2 = IntentInstanceExecution(
        rank=2,
        span=span2,
        sub_intent="food_composition_lookup",
        target_nutrient="protein_g_100g",
        entity_text="chicken breast",
        alim_code=20005,
        quantity_g=200.0,
    )
    instances = [instance1, instance2]
    # Simulate dual BERT inference on RK3588 NPU/CPU
    time.sleep(0.004)  # 4ms simulated inference
    t_cls = (time.perf_counter() - t0) * 1000

    print("\nStep 2: Dual Clause Classification & Canonical Entity Grounding")
    print(f"  ⚡ Latency: {t_cls:.3f} ms")
    for inst in instances:
        print(f"  ├─ Rank {inst.rank}: sub_intent='{inst.sub_intent}' | entity='{inst.entity_text}' (alim_code={inst.alim_code}) | target='{inst.target_nutrient}'")

    # Stage 3: Merge & Adjudication Gate (Rule 4 & Rule 6)
    print("\nStep 3: Merge & Adjudication Gate Verification")
    if instance1.alim_code == instance2.alim_code and instance1.sub_intent == instance2.sub_intent:
        print("  ⚠️ Rule 4 Triggered: Same food -> Merging into K=1 multi-attribute instance.")
    else:
        print("  ✅ Rule 6 Triggered: Distinct entities (salmon alim_code:25000 != chicken alim_code:20005).")
        print("     Both instances preserved under independent execution plan.")

    # Stage 4: CIQUAL Database Execution
    t0 = time.perf_counter()
    for inst in instances:
        food_record = CIQUAL_MOCK_DB[inst.alim_code]
        base_val = food_record[inst.target_nutrient]
        factor = inst.quantity_g / 100.0
        calculated_val = round(base_val * factor, 1)

        inst.db_result = {
            "food_name": food_record["name"],
            "base_val_100g": base_val,
            "quantity_g": inst.quantity_g,
            "calculated_val": calculated_val,
        }
        inst.dispatch_plan = f"SELECT {inst.target_nutrient} FROM foods WHERE alim_code = {inst.alim_code}"

    t_db = (time.perf_counter() - t0) * 1000

    print("\nStep 4: Deterministic Database Dispatch")
    print(f"  ⚡ Latency: {t_db:.3f} ms")
    for inst in instances:
        res = inst.db_result
        unit = "kcal" if "kcal" in inst.target_nutrient else "g"
        print(f"  ├─ [Query #{inst.rank}] SQL: `{inst.dispatch_plan}`")
        print(f"     Result: {res['quantity_g']}g of {res['food_name']} -> {res['calculated_val']} {unit}")

    # Stage 5: Unified Auditable Synthesis
    t0 = time.perf_counter()
    synth_output = (
        f"100g of {instances[0].db_result['food_name'].split(',')[0]} contains "
        f"{instances[0].db_result['calculated_val']} kcal, and "
        f"200g of {instances[1].db_result['food_name'].split(',')[0]} provides "
        f"{instances[1].db_result['calculated_val']}g of protein."
    )
    t_synth = (time.perf_counter() - t0) * 1000

    total_latency = (time.perf_counter() - t_start) * 1000

    print("\nStep 5: Synthesized Auditable Output")
    print(f"  💬 Spoken Output: \"{synth_output}\"")
    print("\n" + "-" * 78)
    print(f"⏱️ TOTAL PIPELINE LATENCY: {total_latency:.2f} ms (Target: < 20 ms on Orange Pi 5)")
    print("-" * 78)

    print("\n" + "=" * 78)
    print("✅ Benchmark 03 Complete: Successfully routed repeated same-intent query.")
    print("=" * 78)

if __name__ == "__main__":
    run_pipeline_demo()
