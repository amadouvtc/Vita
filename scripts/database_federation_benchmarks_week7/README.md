# VITA Week 7: Federated Knowledge Benchmarks & Verification Suite

This test suite chronicles and verifies the Stage 1 Knowledge Federation pipeline implemented in Week 7 of the VITA project.

## Scripts

1. **`01_federated_database_inspector.py`**:
   - Inspects the 4 compiled SQLite knowledge bases (`ciqual.db`, `agribalyse.db`, `food_allergens_v2.db`, `hypersensitivities_and_inhalants_v2.db`).
   - Asserts schema versions, table row counts, and verifies Gate 1A referential integrity (zero orphan `alim_code` references).

2. **`02_knowledge_facade_benchmarks.py`**:
   - Implements the read-only `KnowledgeFacade` with `PRAGMA query_only = ON`.
   - Runs 100 benchmark iterations measuring FTS5 search latency (avg ~0.4ms) and 4-way federated profile retrieval (avg ~1.8ms).

3. **`03_clinical_and_environmental_query_scenarios.py`**:
   - Executes 3 real-world multi-database queries:
     1. Carbon footprint comparison (Beef steak vs Lentil patty).
     2. Birch pollen-food cross-reactivity / OAS (Raw apple vs Cooked apple).
     3. Lactose intolerance thresholds (Whole milk vs Aged cheddar).

## Running the Suite

```bash
python3 scripts/database_federation_benchmarks_week7/01_federated_database_inspector.py
python3 scripts/database_federation_benchmarks_week7/02_knowledge_facade_benchmarks.py
python3 scripts/database_federation_benchmarks_week7/03_clinical_and_environmental_query_scenarios.py
```
