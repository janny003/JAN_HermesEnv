# DevLibGUI WPF common-function validator pattern

## When this applies
- User asks to rebuild `C:\Users\yjs\Desktop\JAN\DevLibGUI` as a GUI for validating DevLib.
- DevLib contains broad hardware/vendor dependencies, but the GUI only needs to validate project-neutral common functions.
- User explicitly wants old GUI contents removed and a WPF version created.

## Boundary rule
- Do not reference the whole `DevLib.csproj` from DevLibGUI when only common helper validation is needed.
- Link only the specific common source files that are intended to be reusable across projects.
- Keep project-specific ICD/BIT/TPS/RscDo logic out of DevLibGUI unless the user explicitly asks for a project-specific validator.

## Known-good structure
Create a WPF project directly under `C:\Users\yjs\Desktop\JAN\DevLibGUI`:

- `DevLibGUI.sln`
- `DevLibGUI.csproj`
- `App.xaml`, `App.xaml.cs`
- `MainWindow.xaml`, `MainWindow.xaml.cs`
- `README.md`
- `.gitignore`

For the 1553B common validator, link these sibling DevLib files in the csproj:

```xml
<ItemGroup>
  <Compile Include="..\DevLib\DevLib\IO\1553B\Common\MilStd1553CommandWord.cs" Link="DevLibCommon\MilStd1553CommandWord.cs" />
  <Compile Include="..\DevLib\DevLib\IO\1553B\Common\MilStd1553WordCodec.cs" Link="DevLibCommon\MilStd1553WordCodec.cs" />
  <Compile Include="..\DevLib\DevLib\IO\1553B\Common\MilStd1553BitCodec.cs" Link="DevLibCommon\MilStd1553BitCodec.cs" />
</ItemGroup>
```

## Recommended WPF screens
- Command Word create/decode
- ushort words ↔ hex string conversion
- sign extension
- 18bit/24bit signed pair pack/split
- sample-all button and validation log

Use `FontFamily="Malgun Gothic"` and verify Korean text with a search for replacement characters (`�`) before reporting completion.

## Verification sequence
1. Remove old GUI contents while preserving `.git`.
2. Generate WPF project and solution.
3. Build:
   - `dotnet build DevLibGUI.sln -c Debug`
4. Remove generated `bin/` and `obj/` before staging, and add `.gitignore` for them.
5. Check Korean strings in XAML/README for garbling.
6. `git add -A`, `git diff --cached --check`, then commit.

## Reporting
Report separately:
- DevLibGUI build result: success/failure, warnings, errors.
- Whether Korean text was checked.
- Commit hash for DevLibGUI.
- If DevLib common source changes were also made, commit and report the DevLib repo separately.
