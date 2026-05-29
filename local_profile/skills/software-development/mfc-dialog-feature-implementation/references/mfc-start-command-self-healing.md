# MFC Start command self-healing for GUI child-process launchers

## Context
In dialog-based maintenance runners, a visible command edit box may keep stale operator/debug text such as `z`. If Start builds the child process command directly from that edit box, `CreateProcessW` fails with `GetLastError=2` because Windows tries to execute the stale token as the program name.

## Durable pattern
When the GUI has a known canonical wrapper command, keep the canonical command in a helper such as `DefaultMaintenanceCommand()` and validate/repair the edit-box command before appending dynamic arguments like `--focus-log`.

Recommended flow:
1. Put the full default wrapper command in one function, not duplicated inline in `OnInitDialog` and log-selection code.
2. `OnInitDialog()` initializes the command edit with `DefaultMaintenanceCommand()`.
3. In the log-selection handler, read and trim the current command.
4. If it does not contain the expected wrapper token (for example `run_maintenance_with_review.py`), replace it with `DefaultMaintenanceCommand()` and append a visible transcript warning.
5. Only after that repair, call the helper that removes/re-adds `--focus-log`.
6. Verify the transcript `[START]` line shows the quoted absolute `python.exe` + wrapper script, not the stale token.

## Example checks
- Static test should assert the default-command helper exists.
- Static test should assert log selection repairs invalid commands before focus-log update.
- Runtime check: put `z` in the command box, select a log, then confirm the command is restored and Start no longer fails with `GetLastError=2`.

## Pitfall
Do not treat `CreateProcessW GetLastError=2` as a Python/reporting failure until the transcript `[START]` command line is inspected. If `[START]` begins with a short stale token, the bug is in GUI command ownership, not the analysis pipeline.