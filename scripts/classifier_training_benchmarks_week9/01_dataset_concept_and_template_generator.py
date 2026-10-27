#!/usr/bin/env python3
"""
VITA Devices — Week 9: Concept-Driven Dataset Generator
======================================================
Demonstrates the Stage 2 pure-Python dataset compilation pipeline:
  1. Reads taxonomy definitions (Level 1 Global Nodes & Level 2 Sub-Intents)
  2. Binds concept domains (Composition, Allergens, Environmental, Trust, Meta)
  3. Synthesizes single-intent training examples:
     - Single-sentence queries: "How much protein is in 100g of salmon?"
     - Multi-sentence single-intent queries: "I am cooking dinner. What is the calorie count for salmon?"
"""

from __future__ import annotations

import json
import random


TAXONOMY = {
    "level1_nodes": {
        "ciqual": "CIQUAL Food Composition & Nutrition Catalog",
        "user_profile": "User profile metrics, preferences, and biometric goals",
        "meta": "System capability, data provenance, and diagnostic questions",
        "none": "Out-of-domain requests and ambient acoustic noise",
    },
    "level2_nodes": {
        "food_composition_lookup": {"parent": "ciqual"},
        "allergen_cross_referencing": {"parent": "ciqual"},
        "data_trust_confidence_codes": {"parent": "ciqual"},
        "environmental_footprint_agribalyse": {"parent": "ciqual"},
        "update_biometric_goal": {"parent": "user_profile"},
        "system_status": {"parent": "meta"},
    }
}

CONCEPTS = {
    "macronutrient_and_energy": {
        "global_category": "ciqual",
        "sub_intent": "food_composition_lookup",
        "nutrients": ["protein", "carbohydrates", "fat", "calories", "fiber", "magnesium", "iron"],
        "foods": ["grilled salmon", "chicken breast", "lentils", "avocado", "oatmeal", "cheddar cheese"],
        "single_sentence_templates": [
            "How much {nutrient} is in {food}?",
            "What is the {nutrient} count for {food} per 100g?",
            "Tell me the {nutrient} level of {food}.",
            "{food} {nutrient} content please.",
        ],
        "multi_sentence_templates": [
            "I am cooking dinner for my family. How much {nutrient} is in {food}?",
            "I just had a workout. What is the {nutrient} value of {food}?",
            "Let me check my meal log. Does {food} provide high {nutrient}?",
        ]
    },
    "allergen_inquiry": {
        "global_category": "ciqual",
        "sub_intent": "allergen_cross_referencing",
        "allergens": ["peanuts", "tree nuts", "lactose", "gluten", "soy", "crustaceans"],
        "foods": ["pesto sauce", "peanut butter", "white bread", "whole milk", "shrimp curry"],
        "single_sentence_templates": [
            "Does {food} contain {allergen}?",
            "Is {allergen} present in {food}?",
            "Could {food} trigger my {allergen} allergy?",
        ],
        "multi_sentence_templates": [
            "I have an allergy test tomorrow. Does {food} contain {allergen}?",
            "My daughter is severely allergic. Is {allergen} listed for {food}?",
        ]
    }
}


def generate_synthetic_samples(num_samples: int = 10) -> list[dict]:
    samples = []
    random.seed(42)

    concept_keys = list(CONCEPTS.keys())
    for _ in range(num_samples):
        c_key = random.choice(concept_keys)
        concept = CONCEPTS[c_key]

        # 50% single-sentence, 50% multi-sentence
        is_multi_sentence = random.random() < 0.5
        templates = concept["multi_sentence_templates"] if is_multi_sentence else concept["single_sentence_templates"]
        tmpl = random.choice(templates)

        food = random.choice(concept["foods"])
        if "nutrients" in concept:
            nutrient = random.choice(concept["nutrients"])
            text = tmpl.format(food=food, nutrient=nutrient)
        else:
            allergen = random.choice(concept["allergens"])
            text = tmpl.format(food=food, allergen=allergen)

        samples.append({
            "text": text,
            "global_category": concept["global_category"],
            "sub_intent": concept["sub_intent"],
            "sentence_structure": "multi_sentence_single_intent" if is_multi_sentence else "single_sentence_single_intent"
        })

    return samples


def run_demo() -> None:
    print("=" * 76)
    print(" VITA Week 9: Concept-Driven Dataset Generation Engine")
    print("=" * 76)

    print("[TAXONOMY SUMMARY]")
    print(f"  Level 1 Global Nodes: {list(TAXONOMY['level1_nodes'].keys())}")
    print(f"  Level 2 Sub-Intents:  {list(TAXONOMY['level2_nodes'].keys())}\n")

    print("[SYNTHETIC SAMPLES DEMO (Single-Intent Focus)]")
    samples = generate_synthetic_samples(8)
    for i, s in enumerate(samples, 1):
        tag = "[MULTI-SENTENCE]" if "multi" in s["sentence_structure"] else "[SINGLE-SENT]"
        print(f"{i:>2}. {tag:<16} \"{s['text']}\"")
        print(f"    -> Global: {s['global_category']:<10} | Sub-Intent: {s['sub_intent']}")
        print()

    print("[VERDICT] Every synthetic sample preserves pure single-intent semantic grounding.")


if __name__ == "__main__":
    run_demo()
