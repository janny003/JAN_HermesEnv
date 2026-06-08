# MSBuild in Git-Bash + Dual-Solution Verification (JAN/ATESWLIB)

## Why this exists
In JAN Windows environments where Hermes terminal runs via Git-Bash/MSYS, MSBuild property switches can be mangled unless argument conversion is disabled. Also, `ATESWLIB` has at least two practical build targets that can diverge in status:
- `K2/K2.sln` (test programs/resources)
- `AteMgr/AteMgr_K2.sln` (manager UI)

## Stable verification pattern
1) Use Git-Bash-safe invocation:
- `export MSYS2_ARG_CONV_EXCL='*'`
- Then call MSBuild with explicit `/p:` switches.

2) Build BOTH solutions and report separately:
- `K2.sln` with `Debug|x86`
- `AteMgr_K2.sln` with `Debug|x86`

3) Always return:
- success/failure per solution
- error count / warning count (if visible)
- first blocking error (file path + error code)

## Example command shape
`export MSYS2_ARG_CONV_EXCL='*'; "/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe" "C:/.../K2.sln" /m /p:Configuration=Debug /p:Platform=x86`

## Session note (example)
- `K2.sln` can fail while `AteMgr_K2.sln` succeeds.
- Treat them as independent status lines in user reports.
