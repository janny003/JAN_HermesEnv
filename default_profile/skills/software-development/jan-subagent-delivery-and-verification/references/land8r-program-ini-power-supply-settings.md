# LAND8R/LAND8116 Program.ini-driven power supply settings

Use this when modifying `C:\Users\yjs\Desktop\JAN\LAND8R-24HS4` / LAND8116 power-control behavior, especially requests like making CC/HUMS voltage/current configurable instead of hard-coded.

## Durable pattern
1. Keep the existing power-supply control path intact.
   - Prefer the existing `PowerSupply.cpp` / e* function route the user expects, such as `eConnectToDevice`, `eConnectToDevice1`, `eSetVolt`, `eSetCurr`, and `eEnableOutput`.
   - Do not replace it with a new control abstraction unless the user explicitly asks.
2. Put user-editable values in `BIN\Config\Program.ini`.
   - Recommended section:
     ```ini
     [PowerSupplyOutput]
     CCVoltage=28.0
     CCCurrent=5.0
     HUMSVoltage=28.0
     HUMSCurrent=5.0
     ```
   - Keep per-test power requirement mapping separate, e.g. `[TestItemPower]` values like `NONE`, `CC`, `HUMS`, `BOTH`.
3. Read INI values immediately before the test item is executed.
   - This allows the operator to change `Program.ini` without recompiling.
   - Validate numeric parsing and fall back to safe defaults if a value is missing or invalid.
4. Preserve Korean/legacy encoding.
   - LAND8116 source/resource files may be CP949/MBCS-sensitive.
   - `Program.ini` may intentionally be UTF-8 BOM depending on existing file state; verify Korean text after editing.
5. Report settings behavior concretely.
   - Include which INI keys control CC and HUMS.
   - Include fallback defaults.
   - Include whether the change is still local or committed/pushed.

## Verification checklist
- `git diff --check` before reporting.
- Confirm encoding for edited source/header/resource/INI files.
  - For LAND8116, `LANDTestView.cpp` / `.h` are CP949-sensitive. If an edit accidentally rewrites them as UTF-8, recover from `git show HEAD:<file>` with CP949 decoding and re-apply only the intended patch; do not leave broad encoding churn in the diff.
  - `git diff --stat` should be reviewed for suspicious large rewrites. A small logic change should not turn into hundreds of insertions/deletions from line-ending or encoding conversion.
- Build `LAND.sln` with the intended configuration, usually `Debug|Win32` unless the user specified otherwise.
- In Git-Bash/MSYS, if MSBuild fails with duplicate environment keys `tmp`/`TMP`, retry with the duplicate lowercase variable removed rather than treating it as a source failure:
  - `env -u tmp MSBuild.exe LAND.sln -p:Configuration=Debug -p:Platform=Win32`
- If possible, launch `Debug\\LAND8116.exe` briefly and terminate it to confirm the executable starts.
- For Stop/OFF requests, verify the actual code path and report the distinction between software path proof and physical hardware observation:
  - Stop path should call the common power-off helper before dialog cleanup.
  - The common helper should reach `DisablePowerSupplyOutput()` and then `pPowerSupply->eDisableOutput()` for both CC (`m_pPS1`) and HUMS (`m_pPS2`).
  - External test tools should be closed with `CUtility::TerminateKnownTestPrograms()` when the user asks about 계측기/보조 프로그램 cleanup.
  - Do not claim actual equipment output is OFF unless connected hardware was observed.

## Reporting shape
Keep the final report concise and in the user's preferred subagent style:
- `Yuno :` one-line completion summary.
- `Jangli :` changed files, INI keys, behavior, verification result.
- Separate build result, execution smoke result, and remaining uncommitted local changes.

## Pitfalls
- Do not commit or report Visual Studio local noise such as `LAND8116.APS` or `LAND8116.vcxproj.user` as intentional changes.
- Do not claim hardware power output was physically verified unless an actual device/hardware response was tested. A GUI/executable launch smoke only verifies software startup.
- Do not hard-code CC/HUMS voltage/current in code after adding INI support; the code defaults should only be fallback values.
