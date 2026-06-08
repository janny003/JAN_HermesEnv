# DevLib WPF apps using DevLib.dll reference

## When this applies
- User explicitly asks DevLibGUI and/or DevLibInstrument to reference `DevLib.dll` instead of linking DevLib `.cs` files.
- The goal is to prove that the WPF app calls functions inside the built DLL, not duplicated/link-compiled source.

## Implementation pattern
1. Build DevLib first:
   - `dotnet build C:\Users\yjs\Desktop\JAN\DevLib\DevLib\DevLib.csproj -c Debug`
2. In each WPF `.csproj`, use an assembly reference with a hint path:
   ```xml
   <ItemGroup>
     <Reference Include="DevLib">
       <HintPath>..\DevLib\DevLib\bin\Debug\net6.0\DevLib.dll</HintPath>
       <Private>true</Private>
     </Reference>
   </ItemGroup>
   ```
3. Remove direct DevLib source links when the user specifically asked for DLL reference:
   - No `<Compile Include="..\DevLib\...">` entries should remain.
4. Keep the WPF app target as `net8.0-windows` if already established; referencing the `net6.0` DevLib assembly is valid for the current apps.
5. For DevLibInstrument deterministic validation, put reusable judgement logic inside DevLib, e.g. `DevLib.Instrument.InstrumentPerformanceValidator`, then call that public API from WPF.

## Verification checklist
- Rebuild DevLib, then rebuild each WPF solution/project.
- Confirm output folder contains copied `DevLib.dll`:
  - `DevLibGUI\bin\Debug\net8.0-windows\DevLib.dll`
  - `DevLibInstrument\bin\Debug\net8.0-windows\DevLib.dll`
- Inspect `.csproj` shape:
  - `<Reference Include="DevLib">` exists.
  - Direct `<Compile Include="..\DevLib...">` links do not exist when DLL reference was requested.
- Run a small temporary console smoke that references only the built `DevLib.dll` and calls the new public API. This proves the function is in the DLL and callable externally.
- Run WPF launch smoke briefly with `timeout 5s dotnet run --no-build --project ... -c Debug`; timeout after window startup is acceptable if there is no startup exception.
- Search changed `.cs`, `.xaml`, `.md`, `.csproj` files for Korean mojibake replacement character `�`.
- Run `git diff --check` for each involved repo before reporting.

## Reporting notes
- Separate DevLib build warnings from WPF build errors. Existing DevLib nullable/platform/vendor warnings are not WPF DLL-reference failures if DevLib exits with 0 errors.
- Report both structural proof and build proof:
  - DevLib Reference present.
  - Direct source links absent.
  - WPF output contains `DevLib.dll`.
  - Direct DLL API smoke passed.
