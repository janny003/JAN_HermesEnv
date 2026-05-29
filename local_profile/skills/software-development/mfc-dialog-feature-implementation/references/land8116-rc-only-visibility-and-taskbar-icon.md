# LAND8116: RC-only safe fix for hidden TIMER button + missing taskbar icon

## When to use
- `LANDTestView.cpp` (or equivalent CP949-heavy file) is fragile and prior edits triggered `C2001/C1057/C2059`.
- User asks for a UI visibility fix (e.g., show TIMER button) and/or taskbar presence/icon behavior.

## Safe pattern
1. Avoid touching fragile `.cpp` for pure visibility/layout asks.
2. Edit `.rc` minimally:
   - Change hidden button to visible by removing `NOT WS_VISIBLE`.
   - Reposition/resize in dialog coordinates near requested UI group.
   - Example used in `IDD_ERUTESTVIEW`:
     - from: `"MANUAL TIMER",IDC_BUTTON_FAILSTOP,...,NOT WS_VISIBLE`
     - to: `"TIMER",IDC_BUTTON_FAILSTOP,392,175,92,28`
3. For taskbar presence on modeless dialog windows, add:
   - `EXSTYLE WS_EX_APPWINDOW` to the target dialog block.
4. Rebuild immediately after `.rc` change and verify runtime launch.

## Why this worked
- Preserved `.cpp` encoding stability.
- Delivered requested UI changes using resource-only deltas.
- Avoided re-triggering macro/string corruption in CP949-sensitive source.

## Verification checklist
- Build `Debug|Win32` succeeds.
- Process launches (`LAND8116.exe` alive) and can be terminated cleanly.
- TIMER button visible at expected location near test-progress controls.
- Dialog now appears as app-window style in taskbar context.
