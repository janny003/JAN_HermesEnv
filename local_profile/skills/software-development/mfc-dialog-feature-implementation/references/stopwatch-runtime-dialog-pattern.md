# Stopwatch feature pattern for legacy MFC dialogs

Session-derived pattern from LAND8R-24HS4:

## Trigger
Need to add stopwatch functionality (start/stop/reset + stopped-time history list) into existing main GUI, while resource file visibility is inconsistent.

## Applied approach
1. Added a main-screen button in `OnInitDialog` via runtime `Create(...)`.
2. Added control ID in `resource.h` and incremented `_APS_NEXT_CONTROL_VALUE`.
3. Implemented a modeless runtime window class (`CWnd`-based) for stopwatch.
4. Wired click handler in message map (`ON_BN_CLICKED`).
5. Used `SetTimer/KillTimer` and `GetTickCount64` for elapsed timing.
6. Appended stop-time snapshots to `CListBox` at each stop event.
7. Added safe teardown in parent `OnDestroy`.
8. Registered new `.h/.cpp` in `.vcxproj`.

## Key snippets to preserve
- elapsed accumulation model:
  - `elapsedBeforeStart += now - startTick` on stop
- display update on timer tick:
  - `elapsed = elapsedBeforeStart + (running ? now - startTick : 0)`
- one-instance dialog behavior:
  - create if null, else show/foreground existing

## Risks observed
- `.vcxproj` can reference `LAND8116.rc` even when file discovery in workspace is inconsistent.
- In such cases, runtime-created controls avoid hard dependency on RC editing.

## Validation targets
- Start updates display continuously.
- Stop appends exactly one list row with formatted timestamp.
- Reset clears both display and list.
- Closing main dialog frees stopwatch window without leak/crash.
