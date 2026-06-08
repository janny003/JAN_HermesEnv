# LAND8R BIN runtime baseline comparison

Use this when a LAND8R/LAND8116 MFC build succeeds but the program does not launch from `BIN`, or when the user asks to compare against a known-good deployed `BIN` folder.

## Durable pattern
1. Compare the active `BIN` folder against the known-good `BIN` recursively by relative path, size, and hash.
2. Separate findings into:
   - missing from active `BIN`
   - extra in active `BIN`
   - same hash
   - changed hash
3. Treat `BIN\LAND8116.exe` presence as a first-class runtime prerequisite. A successful Debug build may only create `Debug\LAND8116.exe`; it does not prove the deployed `BIN` launch target exists.
4. For text configs such as `Config\Program.ini` and `Config\ipset.ini`, normalize line endings before concluding semantic differences. CRLF vs LF alone is not a functional configuration delta.
5. For `Program.ini`, report new `[UI]` keys separately from runtime dependency differences because UI font/spacing settings are expected user-facing changes, not necessarily launch blockers.
6. If `BIN\LAND8116.exe` is missing, prefer restoring the intended Release post-build/copy path or explicitly copying the current verified build output into `BIN` before attempting another `BIN` launch.

## Reporting shape
- State the two compared paths.
- Give counts: active file count, reference file count, same, changed, only-active, only-reference.
- Highlight `LAND8116.exe` first if missing or changed.
- Then list config semantic differences, explicitly saying when a file differs only by line endings.

## Pitfall
Do not infer that the application binary is present just because the solution built successfully. For this project, Debug output and deployed `BIN` output can diverge, and the user may be asking about the deployed runtime folder specifically.