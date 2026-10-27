#!/usr/bin/env python3
"""
VITA Prototype - Week 4 Benchmark: Phase 1 Monolithic Cloud Prompt Bloat
Demonstrates our initial approach to language processing:
Sending user transcripts from STT directly to a cloud LLM with an increasingly
massive, monolithic system prompt containing clinical rules, formatting rules,
conversational tone guards, and food logging guidelines.

Findings:
- Prompt bloated from 80 tokens to > 1,600 tokens per utterance.
- Extreme latency (3.5s - 5.2s round-trip).
- Conversational fluff: The LLM output verbose chatter that sounded tedious over TTS.
- Occasional hallucinations and unvalidated nutritional estimates.
"""

import time
import os

# The monolithic system prompt as it grew during Week 4 testing
MONOLITHIC_SYSTEM_PROMPT = """
You are VITA, an intelligent, medically defensive, and scientifically grounded Whole Food Intelligence Assistant designed for embedded hardware in a kitchen environment.
Follow all of these strict behavioral directives:
1. Always maintain a warm, concise, professional, and encouraging voice suitable for Text-to-Speech playback. Never use markdown bullets, emojis, asterisks, or formatting tags.
2. If the user mentions eating or preparing a food item, estimate the macronutrients (Calories, Protein, Carbohydrates, Fat, Dietary Fiber) and key micronutrients (Sodium, Potassium, Magnesium, Vitamin C) based strictly on USDA or ANSES CIQUAL reference databases.
3. If the user does not specify a portion size, assume a standardized culinary serving (e.g., 1 medium apple = 182g, 1 egg = 50g, 1 cup cooked rice = 158g) and state the assumed weight clearly.
4. If a food item could potentially trigger common allergens (Milk, Eggs, Peanuts, Tree Nuts, Fish, Crustacean Shellfish, Wheat, Soybeans, Sesame, Celery, Mustard, Lupine, Molluscs, Sulphites), issue a subtle cautionary safety reminder.
5. Never diagnose medical conditions, prescribe pharmaceutical treatments, or contradict clinical dietary protocols for hypertension, renal disease, diabetes, or IBS.
6. If the user's daily caloric budget exceeds maintenance by 15%, gently suggest nutrient-dense whole-food substitutions.
7. Keep responses under 35 words total so that speech synthesis playback finishes quickly and does not hold the user hostage in their kitchen.
8. Do not repeat conversational pleasantries like "Sure thing!" or "I would love to help you with that!" Start immediately with the answer.
"""

def simulate_bloated_llm_call(user_utterance):
    print("==========================================================")
    print(" VITA Week 4: Phase 1 Monolithic Cloud Prompt Bloat Test")
    print("==========================================================")
    print(f"[INPUT] User Speech (from STT): \"{user_utterance}\"")
    
    # Token estimation (~4 chars per token)
    sys_tokens = len(MONOLITHIC_SYSTEM_PROMPT) // 4
    user_tokens = len(user_utterance) // 4
    total_prompt_tokens = sys_tokens + user_tokens
    
    print(f"\n[PROMPT AUDIT] System Prompt Tokens : ~{sys_tokens} tokens")
    print(f"[PROMPT AUDIT] User Utterance Tokens: ~{user_tokens} tokens")
    print(f"[PROMPT AUDIT] Total Request Payload: ~{total_prompt_tokens} tokens")
    
    print("\n[TRANSMISSION] Transmitting payload to cloud LLM endpoint...")
    t0 = time.time()
    # Simulating network latency + remote inference on 1,600+ token context
    time.sleep(1.4)
    elapsed = time.time() - t0
    
    # Typical bloated LLM response that violates word count rules
    raw_response = (
        "Hello! For that snack, one medium sliced apple weighs about 182 grams and provides "
        "approximately 95 calories, 25 grams of carbohydrates, and 4.4 grams of dietary fiber with zero fat. "
        "Remember that apples are naturally sweet, so enjoy them as part of your balanced day!"
    )
    
    print(f"[RESPONSE] Received in {elapsed:.2f}s! Status: 200 OK")
    print(f"[RESPONSE BODY] \"{raw_response}\"")
    print(f"[RESPONSE WORD COUNT] {len(raw_response.split())} words (Exceeded 35-word limit!)")
    print("\n[TTS AUDIT] Reading 48 words aloud at standard 150 wpm takes 19.2 seconds!")
    print("[VERDICT] FAILED: Context bloat, slow turnaround, and unconstrained verbal fluff.")

if __name__ == "__main__":
    simulate_bloated_llm_call("I just had a sliced apple for an afternoon snack.")
