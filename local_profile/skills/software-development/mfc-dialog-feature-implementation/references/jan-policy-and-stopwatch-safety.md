# JAN policy + modeless stopwatch safety notes

## Trigger
Use this when implementing utility dialogs/buttons in JAN MFC apps where the user explicitly asks to honor `C:/Users/<user>/Desktop/JAN/Policy/*.md` subagent policies.

## Practical sequence
1. Read relevant policy markdowns under `JAN/Policy` (planner/developer/qa/designer as needed).
2. Implement minimal feature change.
3. Run subagent review focused on policy compliance + regression risks.
4. Apply concrete fixes from review before final handoff.

## Critical stability fix discovered
When using a modeless stopwatch dialog kept by parent pointer:
- Risk: user closes dialog with [X] -> window destroyed, parent pointer non-null -> crash on reopen.

### Mandatory guards
- On open:
```cpp
if (m_pStopwatchDlg != NULL && !::IsWindow(m_pStopwatchDlg->GetSafeHwnd())) {
    delete m_pStopwatchDlg;
    m_pStopwatchDlg = NULL;
}
```
- In dialog class, handle WM_CLOSE as hide:
```cpp
void CStopwatchDialog::OnClose() { ShowWindow(SW_HIDE); }
```
- Keep parent `OnDestroy` cleanup (`DestroyWindow`/`delete`/`NULL`).

## Why this matters
This pattern preserves single-instance behavior and prevents dangling-pointer crashes while matching low-risk policy expectations in legacy MFC maintenance.