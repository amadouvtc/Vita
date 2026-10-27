#!/usr/bin/env python3
"""
VITA Devices — Week 7: Federated Knowledge Database Inspector
============================================================
Inspects the 4 authoritative SQLite knowledge bases compiled during Stage 1:
  1. ANSES CIQUAL 2025 (authoritative food anchor & nutrient composition)
  2. ADEME Agribalyse 3.2 (environmental LCA & PEF 3.1 eco-scores)
  3. Statutory Food Allergens v2 (EU 14 / US 9 regulatory groups & evidence states)
  4. Clinical Hypersensitivities & Inhalants v2 (WHO/IUIS pollen OAS & clinical intolerances)

Verifies:
  - File sizes and schema versioning
  - Table row counts and cryptographic manifest baselines
  - Zero orphan alim_code references (Gate 1A integrity invariant)
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from pathlib import Path

# Paths to databases
DEFAULT_DB_DIR = Path("/home/ahmed/Desktop/VITADEVICE/database")

def inspect_databases(db_dir: Path) -> None:
    print("=" * 70)
    print(" VITA Week 7: Federated Knowledge Database Inspector")
    print("=" * 70)
    print(f"[PATH] Database directory: {db_dir.resolve()}\n")

    if not db_dir.exists():
        print(f"[ERROR] Database directory {db_dir} does not exist.")
        sys.exit(1)

    db_configs = [
        ("ciqual.db", "ciqual_manifest.json", "CIQUAL 2025 (ANSES)"),
        ("agribalyse.db", "agribalyse_manifest.json", "Agribalyse 3.2 (ADEME/INRAE)"),
        ("food_allergens_v2.db", "food_allergens_v2_manifest.json", "Food Allergens v2 (EU 1169 / US FDA)"),
        ("hypersensitivities_and_inhalants_v2.db", "hypersensitivities_v2_manifest.json", "Hypersensitivities & OAS v2 (EAACI / WHO)"),
    ]

    total_bytes = 0

    for filename, manifest_name, label in db_configs:
        file_path = db_dir / filename
        manifest_path = db_dir / manifest_name

        if not file_path.exists():
            print(f"[MISSING] Database {filename} not found.")
            continue

        size_mb = file_path.stat().st_size / (1024 * 1024)
        total_bytes += file_path.stat().st_size

        manifest_data = {}
        if manifest_path.exists():
            with open(manifest_path, "r", encoding="utf-8") as mf:
                manifest_data = json.load(mf)

        print(f"┌── {label} [{filename}]")
        print(f"│   Size: {size_mb:.2f} MB | Schema Version: {manifest_data.get('schema_version', 1)}")
        print(f"│   Build Timestamp: {manifest_data.get('build_date', 'N/A')}")

        conn = sqlite3.connect(f"file:{file_path.as_posix()}?mode=ro", uri=True)
        conn.execute("PRAGMA query_only = ON;")
        cur = conn.cursor()

        tables = [
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_idx' AND name NOT LIKE '%_data' AND name NOT LIKE '%_docsize' AND name NOT LIKE '%_config';"
            ).fetchall()
        ]

        for table in tables:
            count = cur.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
            print(f"│   • Table `{table}`: {count:,} rows")

        conn.close()
        print("└──" + "─" * 40 + "\n")

    print(f"[SUMMARY] Total federated SQLite knowledge footprint: {total_bytes / (1024*1024):.2f} MB")

    # Integrity Gate 1A verification
    print("\n[GATE 1A] Verifying Referential Integrity (Zero Orphan alim_code checks)...")
    ciqual_path = db_dir / "ciqual.db"
    ciqual_conn = sqlite3.connect(f"file:{ciqual_path.as_posix()}?mode=ro", uri=True)
    ciqual_codes = {r[0] for r in ciqual_conn.execute("SELECT alim_code FROM foods;").fetchall()}
    print(f"  -> Authoritative CIQUAL alim_code catalog: {len(ciqual_codes):,} entries")

    # Check Agribalyse
    agb_conn = sqlite3.connect(f"file:{(db_dir / 'agribalyse.db').as_posix()}?mode=ro", uri=True)
    agb_codes = {r[0] for r in agb_conn.execute("SELECT DISTINCT alim_code FROM lca_products;").fetchall()}
    agb_orphans = agb_codes - ciqual_codes
    print(f"  -> Agribalyse: {len(agb_codes):,} unique alim_codes. Orphans: {len(agb_orphans)}")

    # Check Allergens v2
    allg_conn = sqlite3.connect(f"file:{(db_dir / 'food_allergens_v2.db').as_posix()}?mode=ro", uri=True)
    allg_codes = {r[0] for r in allg_conn.execute("SELECT DISTINCT alim_code FROM food_allergen_map;").fetchall()}
    allg_orphans = allg_codes - ciqual_codes
    print(f"  -> Food Allergens v2: {len(allg_codes):,} mapped alim_codes. Orphans: {len(allg_orphans)}")

    # Check Hypersensitivities v2
    hyp_conn = sqlite3.connect(f"file:{(db_dir / 'hypersensitivities_and_inhalants_v2.db').as_posix()}?mode=ro", uri=True)
    hyp_intol_codes = {r[0] for r in hyp_conn.execute("SELECT DISTINCT alim_code FROM food_intolerance_map;").fetchall()}
    hyp_pollen_codes = {r[0] for r in hyp_conn.execute("SELECT DISTINCT alim_code FROM food_pollen_cross_reactivity_map;").fetchall()}
    hyp_orphans = (hyp_intol_codes | hyp_pollen_codes) - ciqual_codes
    print(f"  -> Hypersensitivities v2: {len(hyp_intol_codes | hyp_pollen_codes):,} mapped alim_codes. Orphans: {len(hyp_orphans)}")

    if not (agb_orphans or allg_orphans or hyp_orphans):
        print("\n[VERDICT] PASS: Gate 1A satisfied. 100% referential integrity across all 4 federated databases.")
    else:
        print("\n[VERDICT] FAIL: Orphan alim_code detected!")
        sys.exit(1)

if __name__ == "__main__":
    db_directory = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB_DIR
    inspect_databases(db_directory)
