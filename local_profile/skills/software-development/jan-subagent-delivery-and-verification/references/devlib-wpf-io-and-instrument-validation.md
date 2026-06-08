# DevLib WPF IO and instrument validation split

## When this applies
- User wants DevLib IO validation to live in `C:\Users\yjs\Desktop\JAN\DevLibGUI`.
- User wants DevLib instrument performance validation to live in `C:\Users\yjs\Desktop\JAN\DevLibInstrument`.
- Both should run as WPF applications.

## Target separation
- `DevLibGUI`: IO/protocol common-helper validation only.
  - Preferred current user direction: make the WPF app reference built `DevLib.dll` and call public functions exposed from that DLL, rather than compiling DevLib source files directly into the GUI.
  - Only fall back to linked vendor-free `.cs` files when full `DevLib.dll` reference is explicitly rejected or blocked by a durable compatibility reason; report this as a fallback, not the target architecture.
  - Suitable tabs: 1553B, CCSDS, SPI, I2C, SpaceWire, SpaceFibre, ARINC software-loopback.
  - Keep project-specific BIT/ICD/TPS/RscDo logic out.
- `DevLibInstrument`: instrument performance validation GUI.
  - Preserve existing C++/DLL source folders such as `DevLibInstrumnet`.
  - Add a separate WPF project/solution at the repo root rather than replacing native sources.
  - Reference built `DevLib.dll` and invoke DLL-contained public validation/adaptor functions from the WPF code-behind/view-model.
  - Start with deterministic manual expected/measured/tolerance checks before adding real hardware adapters.
  - Suitable tabs: power supply, signal generator, oscilloscope/DMM, network/spectrum analyzer, Advantech DAQ when needed.

## Implementation pattern
### DevLibGUI
- Use `net8.0-windows` + `<UseWPF>true</UseWPF>`.
- Preferred reference shape for this user:
  - Build `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\DevLib.csproj` first so `bin\Debug\net6.0\DevLib.dll` exists.
  - Add a `<Reference Include="DevLib"><HintPath>..\DevLib\DevLib\bin\Debug\net6.0\DevLib.dll</HintPath></Reference>` or equivalent project reference if compatible.
  - Remove direct `<Compile Include="..\DevLib\DevLib\...">` links once the needed API is public in `DevLib.dll`.
  - If a helper is not public from `DevLib.dll`, add/adjust the public wrapper inside DevLib first, then call it from the GUI. Do not silently keep duplicate compiled copies in the GUI.
- Legacy/fallback source-link pattern, only when DLL reference cannot be used by request or compatibility constraint:
  - `IO\\1553B\\Common\\*.cs`
  - `IO\\CCSDS\\*.cs`
  - `IO\\SPI\\Spi*.cs`
  - `IO\\I2C\\I2c*.cs`
  - `IO\\SpaceWire\\*.cs`
  - `IO\\SpaceFibre\\*.cs`
  - `IO\\Arinc629\\CArinc629.cs`, `IO\\Arinc664\\CArinc664.cs`, `IO\\Arinc717\\CArinc717.cs`
- Be careful with actual API names:
  - `SpiTransfer` exposes `TxData` and `ReadLength`, not `TransmitData`/`ReceiveLength`.
  - ARINC helper methods are instance methods in this codebase. Use `CArinc629.Instance.BuildWord(...)`, `CArinc664.Instance.BuildEthernetFrame(...)`, `CArinc717.Instance.BuildSubframe(...)`.
  - ARINC664 loopback uses `LoadTxFrame` / `ReadRxFrame`.
  - ARINC717 loopback uses `LoadTxWords` / `ReadRxWords` and `PackWords`.

### DevLibInstrument WPF
- Create root-level WPF files:
  - `DevLibInstrumentWpf.sln`
  - `DevLibInstrumentWpf.csproj`
  - `App.xaml`, `App.xaml.cs`
  - `MainWindow.xaml`, `MainWindow.xaml.cs`
  - `README_WPF.md`
  - `.gitignore`
- Keep first implementation hardware-free:
  - Inputs: expected value, measured value, tolerance/limit.
  - Output: PASS/FAIL, error or margin, rule text, log.
- Suggested deterministic checks:
  - Power supply: voltage/current absolute error.
  - Signal generator: frequency and level absolute error.
  - Oscilloscope/DMM: amplitude/voltage absolute error.
  - Network/spectrum analyzer: S21 tolerance and noise floor upper-limit.

## Verification sequence
1. Build DevLib first so the consuming GUIs reference a current DLL:
   - `dotnet build C:\Users\yjs\Desktop\JAN\DevLib\DevLib\DevLib.csproj -c Debug`
   - Confirm `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\bin\Debug\net6.0\DevLib.dll` timestamp is refreshed.
2. Build DevLibGUI:
   - `dotnet build DevLibGUI.sln -c Debug`
3. Build DevLibInstrument WPF:
   - `dotnet build DevLibInstrumentWpf.sln -c Debug`
4. Launch smoke both WPF apps briefly:
   - `timeout 5s dotnet run --no-build --project <project>.csproj -c Debug`
   - Treat timeout after window startup as launch success when no startup error appears.
5. Search source/XAML/README for Korean mojibake replacement characters (`�`).
6. Run `git diff --check` before reporting or committing.
7. Report warnings separately from errors. Existing nullable warnings in DevLib are not WPF wiring failures if build exits with 0 errors.

## Reporting points
- Report DevLibGUI and DevLibInstrument separately.
- Include exact paths, build command/results, warning/error counts, launch smoke result, and Korean text check result.
- Make clear that DevLibInstrument WPF initially validates performance criteria and UI flow without direct DLL/hardware calls; real hardware should be added later via adapters.
