# VITA CIQUAL Database & Knowledge Grounding Suite (Week 6)

This directory contains the Python benchmark and ETL ingestion scripts from **Week 6**, documenting our integration of the French national **CIQUAL** food composition database, our SQLite FTS5 importer, and our strict architectural rule prohibiting LLMs from writing raw SQL queries.

## Scripts Included

1. **`01_ciqual_importer_etl.py`**:
   - Parses raw ANSES CIQUAL XML records.
   - Cleans French numerical formatting (commas to decimal points, `< traces`, bounds).
   - Normalizes relational tables (`foods`, `nutrients`, `composition`) and creates unicode61 `foods_fts` Full-Text Search virtual tables.

2. **`02_auditable_database_api.py`**:
   - The core defensive abstraction: A typed Python Knowledge API that executes parameterized SQL statements.
   - Computes mass-proportional nutritional scaling:
     $$\text{Nutrient Amount} = \left(\frac{\text{Teneur}_{100\text{g}}}{100}\right) \times \text{Portion Grams}$$
   - Generates an immutable clinical audit trail with exact `alim_code` and laboratory citations.

3. **`03_two_stage_llm_grounding_pipeline.py`**:
   - The complete 2-stage interaction loop:
     1. Local Qwen 2.5 1.5B extracts structured intent and slot parameters.
     2. The Orchestrator queries `AuditableKnowledgeAPI` (no LLM-generated SQL).
     3. Ground-truth nutritional values are retrieved and injected into spoken response templates.

## Running the Suite

```bash
python3 01_ciqual_importer_etl.py
python3 02_auditable_database_api.py
python3 03_two_stage_llm_grounding_pipeline.py
```
