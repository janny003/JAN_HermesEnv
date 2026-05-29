# Agent Only GUI interview dialog gating

## Symptom
In the AGENT_Only MFC GUI, Start runs `tools/agent_only_runner.py` and the transcript reaches `[INTERVIEW_Q1]`, but no Yes/No dialog appears. The transcript remains at an `실행 중 - 5-agent workflow...` or input-wait-looking state and no `[DONE]` completion message appears.

## Root cause
The child process is not complete; it is blocked waiting for stdin for Q1. The GUI's `MaybeShowQuestionDialog()` can detect `[INTERVIEW_Qn]`, but it may return early if the command gating only allows legacy `ouroboros` / `run_maintenance_with_review.py` command strings. For Agent Only, the command string contains `agent_only_runner.py`, so that token must also be accepted.

## Durable fix
Patch `OrobrosTestDlg.cpp` in `MaybeShowQuestionDialog()` so the guard allows all supported interactive runners:

```cpp
if (currentCommand.Find(L"ouroboros") < 0 &&
    currentCommand.Find(L"run_maintenance_with_review.py") < 0 &&
    currentCommand.Find(L"agent_only_runner.py") < 0) {
    return;
}
```

## Regression test
Add/keep a static GUI test that asserts the Agent Only dialog path is allowed, for example:

```python
def test_gui_question_dialog_allows_agent_only_runner():
    cpp = (ROOT / "OrobrosTestDlg.cpp").read_text(encoding="utf-8-sig")
    assert "currentCommand.Find(L\"agent_only_runner.py\") < 0" in cpp
    assert "currentCommand.Find(L\"run_maintenance_with_review.py\") < 0" in cpp
```

## Verification checklist
1. Run full pytest for the AGENT_Only repo.
2. Rebuild MFC Debug x64 so the latest exe contains the dialog-gating change.
3. Launch the GUI, select a focus log, and press Start.
4. Confirm Q1 shows as an actual Yes/No popup, then Q2-Q4 and final confirmation follow.
5. Confirm `[OUTPUT]` and `[DONE]` appear and `JAN_agent_only_report_ui.docx/json` are created with Korean text intact.

## Important interpretation
Absence of a completion message after `[INTERVIEW_Q1]` is not automatically a runner failure. First check whether the GUI popped the Q1 dialog and whether the child process is waiting for stdin.