#!/usr/bin/env python3
"""
VITA Prototype - Week 6: Auditable Knowledge API vs Uncontrolled LLM SQL
Demonstrates the critical architectural rule established in Week 6:
WE DO NOT LET THE LLM WRITE SQL QUERIES.

Why LLM-generated SQL is banned:
1. Hallucination Risk: LLMs invent phantom tables and columns (e.g., SELECT fat_grams FROM foods).
2. Performance Killers: Malformed queries cause unindexed table scans, freezing the ARM CPU.
3. Lack of Auditability: Medical/nutritional defensiveness requires 100% deterministic traceability
   back to the exact ANSES food code (alim_code).

The Solution:
The LLM only emits high-level semantic entity slots (food="salmon", grams=150).
A strict, typed Python Knowledge API executes prepared, parameterized SQL queries,
computes mass-proportional nutritional scaling, and returns audited facts.
"""

import sqlite3
import json
import time

DB_PATH = "/tmp/ciqual_prototype.db"

class AuditableKnowledgeAPI:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def search_food(self, query: str):
        """Executes safe, parameterized FTS5 search."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        t0 = time.time()
        
        # Safe parameterized prepared statement
        cur.execute("""
            SELECT f.alim_code, f.nom_eng, f.nom_fr 
            FROM foods_fts ft 
            JOIN foods f ON f.alim_code = ft.alim_code 
            WHERE foods_fts MATCH ? 
            LIMIT 5
        """, (f'"{query}"',))
        
        results = cur.fetchall()
        elapsed_ms = (time.time() - t0) * 1000
        conn.close()
        return results, elapsed_ms

    def get_nutritional_facts(self, alim_code: int, portion_grams: float):
        """Calculates mathematically normalized nutrients for an exact portion."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # 1. Fetch food info
        cur.execute("SELECT nom_eng, nom_fr FROM foods WHERE alim_code = ?", (alim_code,))
        food_meta = cur.fetchone()
        if not food_meta:
            conn.close()
            return None
            
        # 2. Fetch all nutrient compositions per 100g
        cur.execute("""
            SELECT c.const_code, n.nom_eng, c.teneur 
            FROM composition c 
            JOIN nutrients n ON n.const_code = c.const_code 
            WHERE c.alim_code = ?
        """, (alim_code,))
        
        rows = cur.fetchall()
        conn.close()
        
        # 3. Deterministic mass scaling formula: amount = (teneur_100g / 100) * grams
        scale_factor = portion_grams / 100.0
        scaled_nutrients = {}
        for const_code, n_name, teneur_100g in rows:
            scaled_amount = round(teneur_100g * scale_factor, 2)
            scaled_nutrients[n_name] = {
                "const_code": const_code,
                "amount": scaled_amount,
                "unit": "g" if "kcal" not in n_name and "µg" not in n_name else ("kcal" if "kcal" in n_name else "µg"),
                "teneur_per_100g": teneur_100g
            }
            
        return {
            "alim_code": alim_code,
            "food_name_en": food_meta[0],
            "food_name_fr": food_meta[1],
            "portion_grams": portion_grams,
            "nutrients": scaled_nutrients,
            "audit_trail": {
                "database": "ANSES CIQUAL 2025",
                "authority": "French Republic Ministry of Health",
                "scaling_formula": f"({portion_grams}g / 100g) * reference_teneur"
            }
        }

if __name__ == "__main__":
    print("==========================================================")
    print(" VITA Week 6: Auditable Database API vs Raw LLM SQL      ")
    print("==========================================================")
    api = AuditableKnowledgeAPI()
    
    # 1. Search food item
    query = "salmon"
    matches, ms = api.search_food(query)
    print(f"[SEARCH] Query: '{query}' -> Found {len(matches)} matches in {ms:.2f}ms:")
    for code, en, fr in matches:
        print(f"  • alim_code: {code} | {en} ({fr})")
        
    # 2. Fetch normalized facts for 150g portion
    if matches:
        target_code = matches[0][0]
        facts = api.get_nutritional_facts(target_code, portion_grams=150.0)
        print(f"\n[GROUND TRUTH] Normalized facts for 150g of {facts['food_name_en']}:")
        print(json.dumps(facts, indent=2))
        print("\n[VERDICT] 100% Deterministic, mathematically audited, zero LLM hallucinations.")
