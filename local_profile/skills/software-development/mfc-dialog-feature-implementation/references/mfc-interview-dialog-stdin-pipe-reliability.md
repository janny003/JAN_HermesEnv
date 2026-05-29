# MFC Interview Dialog stdin Pipe Reliability (Ouroboros-style Q&A)

## Problem pattern
- UI reads child stdout and opens modal Yes/No dialogs on `[INTERVIEW_Qn]` lines.
- User clicks Yes/No, app writes `예/아니요` to child stdin.
- Intermittent failure appears as pipe write error because child process already exited or closed stdin between popup display and click.

## Durable fix pattern
1. Upgrade write helper to return `lastError` (`WriteAnswer(answer, &err)`).
2. Before writing, probe process state:
   - `WaitForSingleObject(m_pi.hProcess, 0) != WAIT_TIMEOUT` => process already exited.
   - Treat as `ERROR_BROKEN_PIPE` class failure.
3. On `WriteFile` failure, capture `GetLastError()` and log with `FormatWin32Error`.
4. UX policy:
   - `ERROR_BROKEN_PIPE`: warn in transcript, suppress hard error modal.
   - other errors: show warning modal + instruct manual Send fallback.
5. Keep dialog flow non-fatal so test transcript remains usable.

## Practical guardrails
- Do not assume popup implies process is still alive.
- Keep Yes/No automation and manual Send path consistent through the same `WriteAnswer` function.
- If a "final manual input" dialog exists after Q4, apply identical error handling there.

## Verification
- Build success after signature changes in `.h/.cpp`.
- Runtime: trigger Q1~Q4 flow and confirm:
  - normal case: answers auto-written,
  - child-exit race: transcript logs warning without crash/hard-stop,
  - manual Send still works when process alive.
