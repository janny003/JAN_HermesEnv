# Agent Only repo-copy QA regression pattern

When validating the JAN `AGENT_Only` comparison repository after copying or adapting code from `PipeLineOnly`, do not rely only on the narrow Agent Only tests. Run the full pytest suite because copied Pipeline Only tests may still assert the old GUI default command.

Observed durable pattern:
- `python -m pytest -q` can fail even when the Agent Only runner itself works.
- A common failure is a stale test expecting `OrobrosTestDlg.cpp` to point to `C:\\Users\\yjs\\Desktop\\JAN\\PipeLineOnly`, `pipeline_only_runner.py`, or `JAN_pipeline_only_report_ui.docx`.
- In `AGENT_Only`, the correct GUI default command should point to `AGENT_Only`, `agent_only_runner.py`, and `JAN_agent_only_report_ui.docx`.

Recommended verification sequence:
1. Confirm clean repo and executable presence if GUI validation is in scope.
2. Run full regression: `python -m pytest -q`.
3. If stale Pipeline Only assertions fail, update the test expectation to assert the Agent Only command path and output names instead of weakening/removing the test.
4. Run the Agent Only runner smoke path with four Yes/No answers plus final `approved`.
5. Verify JSON fields: `mode == agent_only`, five agents, four questions, four answers, `approval_status == approved`.
6. Verify DOCX and JSON contain Korean text to catch encoding regressions.
7. If code/tests changed, commit and push, then confirm local HEAD equals `origin/main`.

This is a regression-test hygiene rule for comparison repos, not a one-off failure: after cloning/specializing a comparison variant, update tests so they enforce the variant’s intended default command.