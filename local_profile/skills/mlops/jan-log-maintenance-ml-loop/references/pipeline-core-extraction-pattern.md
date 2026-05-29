# Pipeline Core Extraction Pattern

Use this when refactoring JAN maintenance-report generation from a script-oriented flow into an Agent Orchestrator-friendly core.

## Goal

Separate deterministic analysis payload construction from side-effecting wrapper behavior.

The core should be callable by an orchestrator repeatedly without writing files or mutating inspection memory.

## Recommended module boundary

Create or maintain `tools/pipeline_core.py` with a single orchestrator-facing entry point:

```python
build_maintenance_analysis_payload(
    log_root,
    project_root,
    focus_log=None,
    fault_exclusion_csv=None,
    memory=None,
    memory_path=None,
    generated_at=None,
) -> dict
```

The returned payload should preserve the existing report JSON schema:

- `generated_at`
- `log_root`
- `model_paths`
- `summary`
- `top_causes`
- `fail_candidates`
- `focus`
- `memory_json`

## Core responsibilities

Keep these in `pipeline_core.py`:

1. Model path discovery and model loading.
2. TXT log discovery.
3. Log decoding with Korean-safe fallback order: `utf-8`, `cp949`, `euc-kr`, `latin-1`.
4. Metric extraction and feature vector construction.
5. anomaly/cause/risk calculation.
6. `summary`, `top_causes`, and `fail_candidates` payload construction.
7. Focus-log matching, including filename fallback when paths differ.
8. Similar-case calculation.
9. Fault-exclusion recommendation generation.
10. `recommendation_policy.apply_recommendation_policy(...)` integration.
11. Focus `summary_text` generation, preserving Korean report phrases such as `우선점검권고` and `고장배제 점검 권고`.

## Wrapper responsibilities

Keep these in `tools/generate_maintenance_report.py` or another wrapper:

1. CLI argument parsing.
2. DOCX rendering and saving.
3. JSON report saving with `ensure_ascii=False` and UTF-8.
4. stdout path printing used by GUI wrappers.
5. `operator_feedback` parsing and memory update.
6. `inspection_memory.json` write-back.

Do not move memory write-back into the core. Repeated orchestrator calls would otherwise duplicate history entries or mutate user memory during read-only analysis.

## TDD checks to add/keep

Use `tests/test_pipeline_core.py` or equivalent to lock these behaviors:

1. Core returns the legacy report JSON schema.
2. Core does not write DOCX, JSON, or memory files.
3. Focus payload preserves expected fields and Korean text.
4. Focus-log matching works by filename fallback when the supplied path differs.
5. CLI-generated JSON is backward-compatible with direct core output after normalizing time-dependent fields.

Suggested verification:

```bash
python -m pytest tests/test_pipeline_core.py -q
python -m pytest tests -q
```

For smoke verification, generate DOCX+JSON through the CLI and inspect both the JSON payload and DOCX XML for Korean phrases. This catches regressions where JSON is correct but Word output loses the expected Korean text.

## Mirrored JAN roots

When working in the JAN OrobrosTest project, keep both roots synchronized when applicable:

- `C:\Users\yjs\Desktop\JAN\OrobrosTest`
- `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest`

If the mirror root lacks recently introduced support modules such as `recommendation_policy.py` or `agent_memory.py`, copy those dependencies too before running mirror tests.

## Pitfalls

- Avoid import cycles: `generate_maintenance_report.py` should import `pipeline_core`, not the reverse.
- Preserve payload key names because `ouroboros_review_loop.py` and GUI wrappers consume them.
- Inject or pass a single `generated_at` value when comparing CLI and core output.
- Do not treat path mismatch as focus-log missing until filename fallback has been attempted.
