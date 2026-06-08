# DevLib Log INI store pattern

## When to apply
- User asks to add INI save/load support under `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\Utiliy\Log` or similar DevLib utility/log persistence code.
- Need reusable DevLib-side configuration/log persistence without pulling in Windows-only P/Invoke APIs.

## Recommended implementation shape
1. Keep the namespace aligned with existing Log utility files:
   - `namespace CORE.Utility.Log;`
2. Add a pure .NET helper rather than `GetPrivateProfileString` / `WritePrivateProfileString` P/Invoke unless the user explicitly requires Win32 compatibility.
3. Prefer two layers:
   - `IniFile`: generic section/key/value load/save helper.
   - `IniLogStore`: adapter that saves/restores existing `Entry` objects (`Timestamp`, `DeviceType`, `Action`, `Value`).
4. Save files as UTF-8 with BOM to reduce Korean text garbling risk in Windows tools.
5. Escape multiline values and backslashes on write, then unescape on read.
6. When updating a single value, load existing sections first, mutate the target key, then save back so unrelated keys are preserved.
7. Avoid creating an empty `[General]` section when the file begins with explicit sections. Only create `General` for key/value lines that appear before any section.

## Verification checklist
- `dotnet build DevLib/DevLib.csproj -c Debug` from `C:\Users\yjs\Desktop\JAN\DevLib`.
- Check that the new INI file does not introduce new warnings, especially nullable warnings in the new helper.
- Run an isolated smoke console outside the repo that references `DevLib\bin\Debug\net6.0\DevLib.dll` and verifies:
  - `IniLogStore.SaveEntry` then `LoadEntry` round-trips an `Entry`.
  - `IniFile.WriteValue` then `ReadValue` round-trips a direct config value.
  - Korean text remains readable.
  - newline/backslash values restore correctly.
- Read the generated `.ini` file directly and confirm Korean text is visible and no replacement character (`�`) appears.

## Pitfalls
- A naive loader that pre-creates `General` will cause later `WriteValue` calls to emit an unwanted empty `[General]` section.
- `Dictionary<string, string>` copied directly into `Dictionary<string, string?>` can trigger CS8620 under nullable-enabled builds; copy entries explicitly into a nullable-value dictionary.
- Do not commit smoke project files created under temp directories or generated sample INI files.
