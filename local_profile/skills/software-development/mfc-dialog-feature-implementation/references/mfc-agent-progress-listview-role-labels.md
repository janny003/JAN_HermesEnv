# MFC agent progress ListView with role labels

Use this when an MFC dialog launches a single child process but the user needs to see which logical agent/phase is currently active.

## Pattern
- Add a `SysListView32` / `CListCtrl` progress area between the status panel and transcript.
- Prefer columns:
  - `No`
  - `Agent`
  - `State`
  - `Detail`
- Keep a current logical role name such as `m_currentAgentName`.
- Add rows only on distinct status transitions, reusing the same last-status guard used for transcript status logs.
- Initialize ListView common controls with `ICC_LISTVIEW_CLASSES` in app startup.

## Role-label mapping
For JAN maintenance GUI work, a useful split was:
- `JAN Maintenance Report Agent`: default report generation / log analysis wrapper flow.
- `Ouroboros Review Interview Agent`: review interview and final-confirmation phase detected from protocol markers like `[INTERVIEW_Qn]` and `[FINAL_CONFIRM_Q]`.

## Important distinction
If the GUI launches one child process, do not describe these rows as multiple OS-level agents unless the implementation actually spawns multiple processes. The `Agent` column can be a logical role/phase label inside one child-process flow.

## Verification
- Static test asserts `IDC_LIST_AGENT_PROGRESS`, `SysListView32`, `CListCtrl`, `ICC_LISTVIEW_CLASSES`, and expected column captions.
- Static test asserts role names and marker-based role switching logic.
- Build with MSBuild after resource/header/cpp edits.
- Runtime check: launch the exe, send Start, find the `SysListView32` child window, and verify item count increases.