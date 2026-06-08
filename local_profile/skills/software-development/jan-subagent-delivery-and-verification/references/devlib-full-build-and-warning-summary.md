# DevLib full-build and warning-summary verification

## When to use
Use this when the user asks whether DevLib "전체적으로 빌드 되는지" or requests a broad build health check after DevLib common-library changes.

## Verified pattern
Run both build paths from `C:\Users\yjs\Desktop\JAN\DevLib` when possible:

```bash
set -o pipefail; MSYS2_ARG_CONV_EXCL='*' dotnet build DevLib.sln -c Debug --no-restore /v:minimal 2>&1 | tee /tmp/devlib_sln_dotnet_build.log | tail -n 80
```

```bash
set -o pipefail; MSYS2_ARG_CONV_EXCL='*' 'C:/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe' DevLib.sln /p:Configuration=Debug /m /v:minimal 2>&1 | tee /tmp/devlib_sln_vs_msbuild.log | tail -n 100
```

## Summary extraction
After the build, summarize in terms the user can act on:

```bash
printf 'dotnet summary:\n'
grep -E '경고 [0-9]+개|오류 [0-9]+개|warning [0-9]+|error [0-9]+' /tmp/devlib_sln_dotnet_build.log | tail -n 5 || true
printf '\nmsbuild summary:\n'
grep -E '경고 [0-9]+개|오류 [0-9]+개|warning [0-9]+|error [0-9]+' /tmp/devlib_sln_vs_msbuild.log | tail -n 5 || true
printf '\nwarning code top dotnet:\n'
grep -Eo 'warning (CS|CA)[0-9]+' /tmp/devlib_sln_dotnet_build.log | sort | uniq -c | sort -nr | head -10
printf '\nwarning code top msbuild:\n'
grep -Eo 'warning (CS|CA)[0-9]+' /tmp/devlib_sln_vs_msbuild.log | sort | uniq -c | sort -nr | head -10
```

## Reporting standard
Report in the user's preferred concise JAN format:

- `Jangli : 전체 빌드 결과: 성공/실패`
- Include exact target solution and configuration.
- State both command paths and their exit status.
- If errors are zero but warnings remain, say "전체적으로 빌드 됩니다" and then list warning classes separately.
- Do not over-treat warnings as build failure. Nullable warnings (`CS8618`, `CS8625`, `CS8600`, `CS8602`) and Windows-only API warnings (`CA1416`) are follow-up stabilization items unless the user asks to clean warnings.
- Include dirty working-tree note only as context, not as a blocker, unless the user asked for commit/release readiness.
