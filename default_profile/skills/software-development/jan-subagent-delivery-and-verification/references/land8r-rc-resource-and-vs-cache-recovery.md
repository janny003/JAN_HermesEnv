# LAND8R/LAND8116 RC resource restore + Visual Studio cache crash recovery

Use this when `LAND.sln`/LAND8116 builds or launches inconsistently, `BIN\LAND8116.exe` is missing/stale, or Visual Studio closes/crashes while opening the solution.

## Durable pattern
1. Separate project health from IDE health first.
   - Build `LAND.sln` outside Visual Studio with MSBuild.
   - In Git Bash/MSYS use path-conversion protection. The verified form in this repo is:
     - `MSYS_NO_PATHCONV=1 '/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe' LAND.sln /m /p:Configuration=Release /p:Platform=Win32 /t:Build /nologo`
   - If MSBuild succeeds but `devenv.exe` crashes, treat the first issue as Visual Studio cache/profile/install health, not source failure.

2. Check the `.sln` header before assuming the file is otherwise healthy.
   - A repeated LAND8R failure mode is a UTF-8 BOM followed by a blank first line, then `Microsoft Visual Studio Solution File...` on line 2.
   - Verify with `xxd -g1 -l 64 LAND.sln`; problematic bytes start `ef bb bf 0d 0a 4d...`, while healthy bytes start `ef bb bf 4d...`.
   - Back up first: `cp LAND.sln "LAND.sln.bak_$(date +%Y%m%d_%H%M%S)"`.
   - Restore with a small Python normalization: read `encoding='utf-8-sig'`, `lstrip('\r\n')`, normalize newlines, then write UTF-8 BOM + CRLF.
   - Commit the fixed `LAND.sln` and a local recovery note if the user wants future repetition to be quick; do not commit `LAND.sln.bak_*`.

3. Check whether the `.rc` file is truncated or ad-hoc minimal.
   - Healthy LAND8116 `.rc` is a full Visual C++ resource script with dialogs, menus, icons, bitmaps, `LANGUAGE LANG_KOREAN`, and `#pragma code_page(949)`.
   - A tiny file containing only icons/string table/timer dialog can still compile partially but breaks Visual Studio resource/project behavior and can produce an incomplete deployed runtime state.
   - Compare size/hash against a known-good sibling/baseline tree before editing.

3. Restore the full resource script before changing code.
   - Prefer copying the known-good `LAND8116\LAND8116.rc` from the verified baseline tree.
   - Rebuild immediately after restore.
   - Confirm Release build copies `LAND8116\LAND8116.exe` into `BIN\LAND8116.exe`.

4. Verify deployed runtime from `BIN`, not only Debug output.
   - Launch from `C:\Users\yjs\Desktop\JAN\LAND8R-24HS4\BIN` so relative asset/config paths match deployment.
   - Confirm `LAND8116.exe` remains running for several seconds via `tasklist.exe /FI "IMAGENAME eq LAND8116.exe"`.
   - Terminate the smoke-run process after verification.
   - Check `sha256sum BIN/LAND8116.exe LAND8116/LAND8116.exe` to confirm the deployed binary matches the Release output.

5. Triage Visual Studio closing/crashing.
   - Query Windows Application events for `devenv.exe` and capture fault module/exception code.
   - Evidence pattern seen here: `devenv.exe`, fault module `VCRUNTIME140.dll`, exception `0xc0000005`.
   - Back up and remove solution-local `.vs` outside the repo.
   - Back up and recreate `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache`.
   - Test `devenv.exe /SafeMode <solution> /log <file>` first.
   - If SafeMode stays open, close it, then retry normal mode. If normal mode stays open after cache reset, do not repair/reinstall Visual Studio.
   - If SafeMode also crashes, escalate to Visual Studio Installer Repair after reporting the evidence.

## Reporting expectations
- Report Release and Debug build results separately.
- State the exact deployed executable path and hash evidence.
- State whether the app was launched from `BIN` and remained alive.
- State whether Visual Studio was stable in SafeMode and normal mode after cache reset.
- Distinguish source changes (`LAND8116.rc`) from generated build/cache noise (`.vs`, `BIN\*.exe`, `LAND8116\Release`, `LAND8116\Debug`).

## Pitfalls
- Do not infer runtime readiness from `Debug\LAND8116.exe`; this project’s user-facing launch target is `BIN\LAND8116.exe`.
- Do not keep trying source edits for `devenv.exe` APPCRASH if MSBuild is already green.
- Do not leave Visual Studio running when rebuilding if the linker reports the output `.exe` is locked.
- Avoid editing Korean MFC resource/source files broadly; restore known-good CP949 resource content and rebuild before applying further feature changes.
