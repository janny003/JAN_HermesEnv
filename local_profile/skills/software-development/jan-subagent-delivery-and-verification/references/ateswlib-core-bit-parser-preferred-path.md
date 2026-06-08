# ATESWLIB Core BIT parser preferred path

## Trigger
Use this when KGPS/GESU/MFU or CPS-related TPS projects need `GetPOBIT`, `GetIBIT`, or `GetPBIT` for 1553B BIT parsing.

## User-corrected workflow
Do not create project-local `C1553BBitExtensions.cs` files as the default fix. The preferred implementation is in Core parser source files so TPS projects continue to load the parser from `Core.dll`:

Do not infer the parser family only from the visible project name. Confirm the actual `Core.Data.Excalibur.*` namespace/type used by the TPS, then apply the current K2 family mapping:

- KGPS-family BIT callers currently include:
  - `KGPS_1`
  - `KGPS_2`
  - `MFU_1`
  - `MFU_2`
  - `GESU`
  - preferred Core file: `K2/TestProgram/Core/Data/KGPS_2/1553BICD.cs`
- KCPS-family BIT callers currently include:
  - `KCPS_1`
  - `KCPS_2`
  - `PA_2`
  - `CESU`
  - preferred Core file: `K2/TestProgram/Core/Data/KCPS_2/1553BICD.cs`

If another sibling is in scope, re-check its actual `using Core.Data.Excalibur...` and receiver type before editing; do not carry the family assignment across by assumption.

## Implementation pattern
1. Add or verify the parser methods inside the Core class actually used by the caller:
   - `GetPOBITBit`, `GetIBITBit`, `GetPBITBit`
   - `GetPOBIT`, `GetIBIT`, `GetPBIT`
   - `GetPowerOnBIT` as a compatibility wrapper to `GetPOBIT`
2. For the current K2 split, use the user's explicit source paths as the durable parser boundary:
   - CPS/KCPS family: `C:\Users\yjs\Desktop\JAN\ATESWLIB\K2\TestProgram\Core\Data\KCPS_2\1553BICD.cs`
   - GPS/KGPS family: `C:\Users\yjs\Desktop\JAN\ATESWLIB\K2\TestProgram\Core\Data\KGPS_2\1553BICD.cs`
3. Use a class-level helper such as `GetBitFromWord9(ushort[] inputData, int bitNo)`:
   - return `0` for `null` or empty input
   - return `0` for bit numbers outside `1..9`
   - extract `(inputData[0] >> bitNo) & 0x0001`
4. Prefer a shared class-level array helper such as `GetBitsFromWord9(ushort[] inputData, Func<ushort[], int, ushort> bitReader)` to keep `GetPOBIT/GetIBIT/GetPBIT` identical and reduce duplicated bit-name assignment blocks. This is especially useful when normalizing both KCPS_2 and KGPS_2 Core parser files in the same session.
5. Do not silently change bit numbering while refactoring. The existing ATESWLIB parser convention reads ICD `bit1..bit9` with `(inputData[0] >> bitNo) & 0x0001`, so `bit1` maps to mask `0x0002`. Preserve this unless the ICD/user explicitly requires LSB-as-bit1 remapping; report the residual ICD numbering risk after build success.
6. Remove any project-local extension shim files if present:
   - `K2/TestProgram/*/C1553BBitExtensions.cs`
7. Remove `<Compile Include="C1553BBitExtensions.cs" />` from affected TPS `.csproj` files.
8. Rebuild in this order:
   - `K2/TestProgram/Core/Core.csproj` with `Debug|AnyCPU`
   - `K2/K2.sln` with `Debug|x86`
   - `AteMgr/AteMgr_K2.sln` with `Debug|x86`
9. If `CS1061` persists after the source methods exist, treat `BIN/TPS/Core.dll` as potentially stale. Rebuild Core first, then rebuild the dependent TPS/solution; do not reintroduce project-local extension files just to mask a stale Core reference.

## Git-Bash and edit pitfalls
- When invoking Visual Studio MSBuild from Git-Bash, protect slash switches from MSYS path conversion. Use `MSYS2_ARG_CONV_EXCL='*'` before `MSBuild.exe ... /p:Configuration=Debug /p:Platform=x86 /m /v:minimal /nologo`, or use an already validated alternative switch style from `references/msbuild-gitbash-and-dual-sln-check.md`.
- When removing `<Compile Include="C1553BBitExtensions.cs" />` from old `.csproj` files, preserve BOM/CRLF and remove only that exact line. Avoid fuzzy patching a tiny line if it can absorb the adjacent `Properties\\AssemblyInfo.cs` or first task include line; a safer pattern is byte-level replacement of exactly `b'    <Compile Include="C1553BBitExtensions.cs" />\r\n'`.
- Full K2/AteMgr builds can dirty many tracked `BIN`, `obj`, and `AteMgr/.../bin` artifacts. Before reporting or committing, separate source changes from build-output noise. If cleanup is destructive or approval-gated, report the blocker plainly and do not imply the tree is clean.

## Verification checklist
- Confirm the Core parser methods are present in the actual parser class used by the callers, not just in a sibling source file. For the current KGPS-family path, verify `K2/TestProgram/Core/Data/KGPS_2/1553BICD.cs` contains `GetPOBIT`, `GetIBIT`, `GetPBIT`, and `GetPowerOnBIT`.
- `git grep C1553BBitExtensions -- K2` returns no references when the Core path is intended.
- `CS1061` count is zero in Core/K2/AteMgr build logs.
- KGPS/GESU/MFU call sites remain separated:
  - `GetPOBIT(msgdataPOBIT)`
  - `GetIBIT(msgdataIBIT)`
  - `GetPBIT(msgdataPBIT)`
- Search confirms no mixed-parser leftovers:
  - `ibitBit = myd.GetPowerOnBIT(...)`
  - `pbitBit = myd.GetPowerOnBIT(...)`
  - `GetPowerOnBIT(msgdataIBIT)`
  - `GetPowerOnBIT(msgdataPBIT)`
- Build-output noise (`BIN`, `obj`, cache files, DLL/PDB churn) is restored or cleaned before final status/commit.

## Fallback note
A project-local extension shim can still be useful as a temporary diagnostic workaround, but it is not the preferred durable fix for this user's ATESWLIB workflow.