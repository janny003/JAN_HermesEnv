# Deterministic Agent Orchestrator for JAN Maintenance Pipeline

## When to use
Use this note when adding or reviewing the first Agent Orchestrator layer over the JAN deterministic maintenance pipeline.

## Durable pattern
Start with deterministic agents before adding LLM/ReAct behavior. The Agent Orchestrator should coordinate existing deterministic modules, not replace model inference.

Recommended stage order:
1. `MemoryAgent`
   - Loads separated memory bundle from `tools/agent_memory.py`.
   - No writes.
2. `PipelineAgent`
   - Calls `pipeline_core.build_maintenance_analysis_payload(...)`.
   - Produces the report payload.
   - No writes.
3. `RecommendationAgent`
   - Exposes recommendation fields from the focus payload as an agent-stage output.
   - Keeps recommendation policy effects visible without mutating raw pipeline data.
4. `VerificationAgent`
   - Checks payload schema, focus availability, Korean recommendation text, and summary count sanity.
   - Carries the GUI review contract as metadata: `[INTERVIEW_Q1]` through `[INTERVIEW_Q4]` Yes/No prompts must remain visible in wrappers.
5. `ReportAgent`
   - Performs handoff only.
   - Does not write DOCX/JSON; report writing remains in `generate_maintenance_report.py` until `report_writer.py` is split out.

## Step result contract
Each agent step should explicitly report:
- `agent`: stable agent name
- `mode`: currently `deterministic`
- `side_effect`: boolean, normally `False`
- `status`: `ok`, `needs_attention`, etc.
- `input`: a dict describing the inputs consumed by that stage
- `output`: a dict describing the produced stage result
- optionally `details` as a backward-compatible alias of `output`

This is important because “details” alone is too ambiguous for future LLM-agent replacement and stage-level testing.

## Purity rule
The orchestrator must not write report files or update memory. It can read separated memory and return a composed result. Memory updates remain in explicit wrappers or future write-capable agents with `side_effect=True`.

## TDD checks to add
- RED test for missing `tools.agent_orchestrator` import before implementation.
- Agent order is exactly Memory → Pipeline → Recommendation → Verification → Report.
- All stages expose `input` and `output` dicts.
- All initial stages are deterministic and `side_effect=False`.
- Split memory affects recommendation/interview notes.
- `focus_log` can match by filename fallback.
- Missing focus does not crash; verification returns `needs_attention` and `requires_operator_confirmation=False`.
- Repeated orchestrator runs do not modify memory files.

## Verification commands
From `C:\Users\yjs\Desktop\JAN\OrobrosTest`:

```bash
python -m pytest tests/test_agent_orchestrator.py -q
python -m pytest tests -q
```

Mirror the same files to `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest` and run the same full pytest there when working in the JAN policy project.

## Pitfalls
- Do not let `RecommendationAgent` silently become another writer; it should expose recommendation state, not persist it.
- Do not put DOCX/JSON save logic into `ReportAgent` before the dedicated `report_writer.py` split.
- Treat agent `input`/`output` as part of the public contract, not debug decoration.
- Keep Korean strings under UTF-8 and verify key phrases such as `우선점검권고` remain visible in returned payloads/tests.
