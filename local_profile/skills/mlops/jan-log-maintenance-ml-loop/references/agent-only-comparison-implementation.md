# Agent Only comparison implementation pattern

Use this reference when building or auditing the JAN comparison repository where the MFC GUI shell is preserved but all diagnostic/recommendation behavior is routed through an Agent Only pipeline.

## Repository role
- Local workspace: `C:\Users\yjs\Desktop\JAN\AGENT_Only`
- Remote comparison repo: `https://github.com/janny003/AGENT_Only.git`
- Purpose: provide the Agent Only baseline for comparison against:
  - Pipeline Only: deterministic pipeline without agent review
  - Hybrid: deterministic pipeline core with agent-assisted review/memory/recommendation

## Architecture expectation
The Agent Only implementation should keep the existing MFC GUI shell for operator continuity, but the default Start command should call an Agent Only runner instead of the hybrid review wrapper.

Expected 5-agent chain:
1. Context & Field Interview Agent
   - structures request/focus context
   - creates and records 4 separate Yes/No field questions
2. Persistent Memory Retrieval Agent
   - retrieves previous diagnostic/interview/inspection history
3. Diagnostic Reasoning Agent
   - reasons over logs, focus item, risk, and history
4. Procedure & Priority Agent
   - creates exclusion procedure and inspection priority
5. Verification & Feedback Agent
   - handles final confirmation, verification payload, and report persistence

## Output contract
The GUI default command should write both DOCX and JSON artifacts so later comparison/evaluation can consume structured outputs.

Recommended default output names:
- `out\JAN_agent_only_report_ui.docx`
- `out\JAN_agent_only_report_ui.json`

Smoke-test output names may use:
- `out\JAN_agent_only_smoke.docx`
- `out\JAN_agent_only_smoke.json`

JSON should include at minimum:
- `mode: agent_only`
- all 5 agent names/steps
- total log count
- fail candidate count
- high-risk count
- interview answers/final confirmation when provided

## Implementation notes
- Keep the MFC shell small: it should launch the runner and surface transcript/output paths, not contain diagnostic logic.
- The runner can be deterministic at first; the important baseline distinction is that reasoning/procedure/verification are expressed as explicit agent stages rather than pipeline-only postprocessing.
- Preserve Korean text carefully in runner output, JSON, and DOCX. Verify the generated JSON and Word report display Korean correctly.
- Keep Yes/No questions as 4 separate prompts/dialogs, not a combined paragraph.

## Verification checklist
1. Static/unit tests for the Agent Only runner pass.
2. Runner smoke execution succeeds with 4 Yes/No answers and final confirmation input.
3. JSON output confirms `mode=agent_only` and all 5 agents are present.
4. DOCX and JSON files are created at the expected output paths.
5. MFC Debug x64 rebuild succeeds with 0 errors.
6. The generated exe launches; if it is manually terminated after launch, distinguish that from a build/runtime startup failure.

## Common pitfall
Do not report only the Python runner result. For this user, code changes must be followed by immediate build verification and a concise report of build success/failure plus key errors, especially for MFC GUI projects.
