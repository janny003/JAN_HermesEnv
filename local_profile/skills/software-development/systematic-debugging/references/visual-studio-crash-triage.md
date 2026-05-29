# Visual Studio 2022 crash triage notes

Use this reference when Visual Studio itself exits/crashes while opening a solution or even a newly created project.

## Durable pattern

If MSBuild builds the solution successfully but `devenv.exe` crashes, treat the IDE/runtime/profile as the failing component before editing project code.

Typical Windows Event Log evidence:
- Faulting application: `devenv.exe`
- Faulting module: `VCRUNTIME140.dll` or another VS runtime DLL
- Exception code: `0xc0000005`
- Related `PerfWatson2.exe` / `PerfWatsonVS12Data` entries

## Investigation sequence

1. Check whether the project builds outside Visual Studio.
   - In Git Bash/MSYS, prevent `/p:` and `/m` arguments being path-converted:
     `MSYS2_ARG_CONV_EXCL='*' MSBuild.exe OrobrosTest.sln /p:Configuration=Debug /p:Platform=x64 /m`
2. Check recent Application event logs for `devenv.exe`, `PerfWatson`, `.NET Runtime`, `VCRUNTIME140`, `KERNELBASE`.
3. Inspect Visual Studio ActivityLog and MEF cache errors:
   - `%APPDATA%\Microsoft\VisualStudio\<instance>\ActivityLog.xml`
   - `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache\Microsoft.VisualStudio.Default.err`
4. If one solution crashes but others do not, back up and remove the solution-local `.vs` folder.
5. If all projects/new projects crash, test:
   - `devenv.exe /SafeMode`
6. Interpret Safe Mode:
   - Safe Mode stable + normal mode crashes: user profile, extensions, MEF cache, or VS installed component composition is likely.
   - Safe Mode also crashes: VS installation/runtime repair is more likely.
7. Prefer non-destructive repairs in order:
   - Back up and clear `ComponentModelCache`.
   - Back up and clear solution-local `.vs`.
   - Consider `devenv /ResetUserData` only after user consent, because it resets layouts/recent projects/settings.
   - Use Visual Studio Installer > More > Repair when the user prefers repair or when crashes persist across projects.

## Pitfalls

- Do not conclude the C++ source or `.sln` is broken if command-line MSBuild succeeds.
- Do not leave `.vs` backup folders inside the repository; move them to a temp path so git status stays clean.
- In Git Bash, raw `/p:Configuration=...` can be converted incorrectly by MSYS. Use `MSYS2_ARG_CONV_EXCL='*'` for MSBuild invocations.
- Safe Mode may keep running beyond a short timeout; a timeout exit from the probe is not itself a crash. Cross-check event logs.
