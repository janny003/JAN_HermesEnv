# MFC multi-agent progress ListView pattern

Use this when an MFC dialog launches one child workflow but the user needs to see which logical agent/role is active at each stage.

## Problem signal
- A single child process performs several conceptual roles, but the GUI only shows generic states like running/waiting/done.
- The user asks to show “what agent” is working, not just that an agent is working.
- The workflow emits stdout protocol markers such as `[RUN]`, `[REVIEW]`, `[INTERVIEW_Qn]`, `[FINAL_CONFIRM_Q]`, `[DONE]`, or can be extended to emit explicit `[AGENT] Name | detail` markers.

## Recommended UI
Add a `SysListView32` above the transcript with columns:
- `No`
- `Agent`
- `State`
- `Detail`

Keep the status panel as the current-state summary, and use the ListView as the audit trail. On each Start, clear the ListView and reset sequence/last-status state so the new run is readable.

## Implementation pattern
1. Add a list control resource and bind it with `CListCtrl`.
2. Initialize common controls with `ICC_LISTVIEW_CLASSES`.
3. Initialize columns once in `OnInitDialog`.
4. Centralize status updates through `SetAgentStatus(state, detail)`.
5. When the state changes, append both:
   - transcript line: `[AGENT STATUS] state - detail`
   - ListView row: `No / currentAgentName / state / detail`
6. Maintain `m_currentAgentName` separately from status.
7. Prefer explicit child stdout markers:
   - `[AGENT] Context & Field Interview Agent | ...`
   - `[AGENT] Persistent Memory Retrieval Agent | ...`
   - `[AGENT] Diagnostic Reasoning Agent | ...`
   - `[AGENT] Procedure & Priority Agent | ...`
   - `[AGENT] Trust Gate Agent | ...`
   - `[AGENT] Feedback Learning Agent | ...`
8. Keep fallback parsing for older outputs:
   - `[INTERVIEW_Qn]` -> `Context & Field Interview Agent`
   - `[FINAL_CONFIRM_Q]`, `[FINAL_CONFIRM_A]`, `[REVIEW]` -> `Trust Gate Agent`
   - review script launch -> `Procedure & Priority Agent`
   - report generation launch / `[RUN]` -> `Diagnostic Reasoning Agent`
   - `[FINAL_CONFIRM]`, `[DONE]` -> `Feedback Learning Agent`

## Verification
- Static test checks resource ID, `SysListView32`, `CListCtrl`, columns, `[AGENT]` parser, and all intended agent names.
- Run targeted Python tests for GUI/status and workflow wrapper.
- Run full Python test suite.
- Build Debug x64 with MSBuild and require 0 errors.
- Launch built exe and confirm the ListView handle exists and row count increases after Start.

## Pitfalls
- Do not imply there are multiple OS child processes if there is only one process. Describe them as logical workflow agents/roles unless the implementation truly spawns multiple processes.
- Do not rely only on fallback string inference when the Python wrapper can emit explicit `[AGENT]` markers; explicit markers are more stable.
- Keep user-visible agent names stable and human-readable; avoid internal script names in the ListView.
