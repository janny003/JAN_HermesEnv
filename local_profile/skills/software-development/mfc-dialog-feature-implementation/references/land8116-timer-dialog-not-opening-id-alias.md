# LAND8116 Timer dialog not opening: control-ID alias trap (2026-05)

## Symptom
- User reports: timer dialog does not open when clicking `Manual TIMER` button.
- Existing code had `OnBnClickedButtonFailstop()` empty, and no message-map route for `IDC_Timer`.

## Root cause
- In `resource.h`, both IDs mapped to the same numeric value (`1129`):
  - `IDC_BUTTON_FAILSTOP`
  - `IDC_Timer`
- UI in `.rc` used `IDC_Timer` on `IDD_ERUTESTVIEW`.
- Code assumptions focused on legacy fail-stop handler name, but actual click path was not mapped to the canonical timer handler.

## Durable fix pattern
1. Confirm real control ID from `.rc` dialog block (not only `resource.h` aliases).
2. Map visible timer button directly:
   - `ON_BN_CLICKED(IDC_Timer, &CLANDTestView::OnBnClickedTimer)`
3. Keep timer logic in canonical handler `OnBnClickedTimer`.
4. If legacy handler must remain, delegate only:
   - `OnBnClickedButtonFailstop() { OnBnClickedTimer(); }`
5. Implement safe modeless lifecycle:
   - open via `CDialogTimer::ShowModeless(...)`
   - close via `CloseTimerDialog()` (`CloseNow` + `delete` + null)

## Verification
- Click `Manual TIMER` once -> dialog opens.
- Click again -> dialog closes (toggle behavior).
- Build verification should run immediately after wiring change.

## Why this matters
- Numeric ID aliases can hide wiring mistakes in brownfield MFC screens.
- `.rc` is source-of-truth for what user can actually click on that dialog.
