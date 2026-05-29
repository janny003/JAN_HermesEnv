# Visual Studio Crash + ComponentModelCache Reset Pattern

Use when Visual Studio itself exits/crashes while opening or using a C++/MFC solution, especially after the project still builds from command line.

## Evidence pattern

Windows Application event log may show:

- Faulting application: `devenv.exe`
- Fault module: `VCRUNTIME140.dll`
- Exception code: `0xc0000005`
- Related `PerfWatson2.exe` or `PerfWatsonVS12Data` entries

Visual Studio activity/cache logs may show MEF/component composition failures, for example:

- `%APPDATA%\Microsoft\VisualStudio\<instance>\ActivityLog.xml`
- `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache\Microsoft.VisualStudio.Default.err`
- Missing assemblies in web/XAML/Razor/CPS/LiveShare components

This points more strongly to Visual Studio cache/install/extension state than to the user project source.

## Safe first action

Close Visual Studio first. Then back up and recreate the MEF cache folder.

Git Bash / MSYS example:

```bash
INSTANCE='17.0_cb0d6b9e'
CACHE="/c/Users/yjs/AppData/Local/Microsoft/VisualStudio/${INSTANCE}/ComponentModelCache"
STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP="${CACHE}.bak_${STAMP}"

ps -W | grep -Ei 'devenv|PerfWatson|ServiceHub|MSBuild|VBCSCompiler' || true
mv "$CACHE" "$BACKUP"
mkdir -p "$CACHE"
printf 'backup=%s\n' "$BACKUP"
```

Use the actual Visual Studio instance directory for the machine; do not hard-code the example instance unless it matches.

## Follow-up decision

1. Reopen Visual Studio and the solution.
2. If it still crashes, run:

```text
"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe" /SafeMode
```

3. If Safe Mode works but normal mode fails, suspect an extension/cache/MEF issue.
4. If Safe Mode also crashes, use Visual Studio Installer Repair before changing project code.

## Pitfall

Do not treat an IDE crash as proof of a source regression unless the project also fails in command-line build/test. First separate IDE health from project health.