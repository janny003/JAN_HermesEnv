# LAND8116: IDC_Timer symbol drift + macro cascade (2026-05)

## Trigger
Timer dialog wiring was added in `LANDTestView.cpp` with:
- `ON_BN_CLICKED(IDC_Timer, &CLANDTestView::OnBnClickedTimer)`

Build then showed cascades including:
- `IDC_Timer: undeclared identifier`
- `_messageEntries: const object must be initialized`
- `macro invocation improperly terminated`
- `unexpected EOF in macro expansion`
- `newline in constant`

## Root causes observed
1. Resource-symbol drift:
   - `.rc` contained `PUSHBUTTON "Manual TIMER",IDC_Timer,...`
   - `resource.h` lacked `#define IDC_Timer ...`
2. Literal corruption risk in parallel edits:
   - accidental real newline inserted inside `_T("...")` can produce the same macro/parse cascade.

## Durable fix sequence
1. Use `.rc` symbol as source-of-truth (`IDC_Timer`).
2. Recreate missing symbol in `resource.h` (alias to existing numeric ID if needed during migration).
3. Keep canonical handler on `OnBnClickedTimer`; let legacy handler delegate.
4. Confirm string literals use escaped `\n` not raw line breaks.
5. Rebuild immediately after each micro-change.

## Fast verification queries
- `resource.h`: `#define IDC_Timer`
- `.rc`: `IDC_Timer` on target dialog control
- `.cpp`: `ON_BN_CLICKED(IDC_Timer, &CLANDTestView::OnBnClickedTimer)`
- `.cpp`: no `_T("...` split across lines

## Notes
This pattern is especially common in legacy MFC trees where `.rc`, `resource.h`, and message-map edits are done in separate passes or restored selectively.