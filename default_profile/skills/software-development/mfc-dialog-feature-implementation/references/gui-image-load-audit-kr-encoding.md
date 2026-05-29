# GUI image-load audit in KR-encoded MFC projects

## Trigger
User reports intermittent `ERROR : Failed to load!\nFILE PATH:%s` popups while opening different dialogs/views.

## What worked
1. Enumerate all `m_BGImg.Load(...)` call sites and classify by asset literal style:
   - Safe: ASCII filename (`Debugbackimage.png`)
   - Risky: garbled Korean filename literals (`����...png`)
2. Cross-check actual files in `BIN/image` to confirm whether intended Korean assets exist.
3. Keep CWD anchoring patch in `InitInstance()` (`SetCurrentDirectory(exeDir)`) to stabilize relative paths.
4. For KR-fragile files, avoid broad text edits. Apply minimal edits only, and build after each edit.

## High-risk pattern
- Editing garbled `_T("...한글파일명...")` literals in CP949/ANSI files can trigger:
  - `C2001` newline in constant
  - `C1057` unexpected EOF in macro expansion
  - `C2059` syntax errors at unrelated lines

## Recovery pattern
- If compile breaks after literal patch in fragile files:
  1. `git checkout -- <fragile-file>.cpp`
  2. Rebuild to restore baseline.
  3. Re-apply using safer alternatives:
     - Sidecar `.cpp` for missing symbol implementations (linker fixes)
     - Very small targeted path edits only when necessary

## Verification checklist
- Build Debug/Win32 after EACH non-trivial patch.
- Runtime check: launch `Debug/LAND8116.exe`, confirm process starts, then cleanly terminate.
- For each dialog/view with `m_BGImg.Load`, confirm no fail popup on open.

## Note
When full UI visual parity is not required immediately, converging all background loads to one known-good ASCII image (`Debugbackimage.png`) is a practical stabilization step before a later encoding cleanup.