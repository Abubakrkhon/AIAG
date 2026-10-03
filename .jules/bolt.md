## 2026-04-09 - Database Aggregations and Dict Caching

**Learning:** When retrieving summary stats across multiple rows or listing static models in Python FastAPI apps, avoiding loading large ORM objects (with large JSON/Text columns like interview transcripts and answers) by using SQL aggregates (`func.count`, `func.avg`, `case`) and pre-computing static lookup dictionaries improves speed and memory efficiency significantly.
**Action:** Use SQL aggregates for stats endpoints and cache static model listings at module load time.
