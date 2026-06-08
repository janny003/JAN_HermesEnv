# DevLibInstrument separated instrument tabs and oscilloscope graph pattern

## When this applies
- User asks to split DevLibInstrument combined instrument screens into separate device-specific screens.
- User asks for oscilloscope received data to be displayed graphically.
- Work is under `C:\Users\yjs\Desktop\JAN\DevLibInstrument` WPF app referencing built `DevLib.dll`.

## UI structure pattern
Keep instrument concerns separated into individual tabs:
- `전원공급기`
- `신호발생기`
- `오실로스코프`
- `DMM`
- `네트워크 분석기`
- `스펙트럼 분석기`

Avoid combined tabs such as `오실로스코프/DMM` or `네트워크/스펙트럼` once the user asks for instrument-level separation. Each tab should have:
1. connection/control input group,
2. deterministic judgement input group,
3. mapping/result output group.

## Oscilloscope graph implementation
For WPF without adding chart dependencies, use built-in `Canvas` + `Polyline`:
- XAML: `Canvas x:Name="ScopeGraphCanvas"` inside a dark graph container.
- Code-behind fields: `private List<double> _scopeWaveform = new();`
- Parse CSV waveform input with separators `, ; whitespace \r \n \t` using invariant-culture doubles.
- Render steps:
  1. clear canvas,
  2. draw simple grid lines,
  3. normalize Y using min/max and guard zero range with epsilon,
  4. build `PointCollection`,
  5. add a cyan `Polyline`,
  6. show `Samples`, `Min`, `Max`, and optionally peak-to-peak in a status/result text.
- Hook `Canvas.SizeChanged` to redraw the current waveform after layout changes.

## DevLib API boundary found in this session
- `COscilloscope` currently exposes scalar measurement/control methods such as:
  - `SCOPEViewChannel(int channel)`
  - `SCOPEChannelSetVol(int channel, double voltage)`
  - `SCOPETimeRange(double range)`
  - `SCOPEMeasureVoltAmp()`
- `COscilloscope` does not currently expose a public `Open(resource)` or waveform block-read API. Do not claim full waveform hardware acquisition is complete unless such an adapter is added.
- Safe default: graph CSV/sample waveform data. If `실제 장비 호출 허용` is checked, the current safe bridge is to call `SCOPEMeasureVoltAmp()` and append that scalar measurement to the plotted series.
- `CDigitalMultimeter` can be mapped separately with `Open(resource)` and `ReadData(range, resolution, mode)`.
- `CNetworkAnalyzer` has frequency/marker APIs, but no public `Open(resource)` in the checked class; keep Resource as UI/mapping input until an adapter exists.
- `DevLib.Device.NI.CSpecturmAnalyzer.cs` had no detected public API in this session; keep the spectrum tab adapter-ready and use deterministic noise-floor `UpperLimit` judgement until a public API exists.

## Verification pattern
After changing DevLibInstrument WPF:
1. Build DevLib first: `dotnet build C:\Users\yjs\Desktop\JAN\DevLib\DevLib\DevLib.csproj -c Debug`.
2. Build project and solution:
   - `dotnet build DevLibInstrumentWpf.csproj -c Debug`
   - `dotnet build DevLibInstrumentWpf.sln -c Debug`
3. Launch smoke: `timeout 5s dotnet run --no-build --project DevLibInstrumentWpf.csproj -c Debug` and treat timeout with no startup error as pass.
4. If a previous WPF smoke leaves `DevLibInstrument.exe` running and locks `bin\Debug\net8.0-windows\DevLibInstrument.exe`, kill the process and rebuild. In Git Bash/MSYS, use `taskkill.exe //PID <pid> //F` or `taskkill.exe //IM DevLibInstrument.exe //F` because single-slash Windows switches may be rewritten as paths.
5. Check Korean replacement characters (`�`) in XAML, code-behind, and README.
6. Run `git diff --check`.

## Reporting notes
- Report separated tabs explicitly.
- Clearly distinguish CSV/sample graph rendering from real hardware waveform acquisition.
- If the graph uses scalar `SCOPEMeasureVoltAmp()` appending, call it a temporary bridge, not a full waveform read.
