# DevLibInstrument real instrument input validation

## When this applies
- User asks to make `C:\Users\yjs\Desktop\JAN\DevLibInstrument` accept the same kind of real input parameters that were added to `DevLibGUI`.
- The target is the root-level WPF app (`DevLibInstrumentWpf.csproj` / `MainWindow.xaml`), not the preserved native C++ folder `DevLibInstrumnet`.
- The app should keep referencing built `DevLib.dll` instead of duplicating DevLib source files.

## UI pattern
- Keep deterministic performance judgement inputs, but add a separate connection/control input area per instrument tab.
- Add a global safety toggle such as `실제 장비 호출 허용`.
  - Default/off mode: validate required inputs and show API mapping only.
  - On mode: call public DevLib instrument APIs that are safe and actually available.
- Useful tab inputs:
  - Power supply: VISA Resource, Channel, Set Voltage, Set Current.
  - Signal generator: VISA Resource, Frequency Hz, Level dBm, RF Output ON/OFF.
  - Oscilloscope/DMM: Scope Resource, Scope Channel, Scope Range V, Scope Time Range s, DMM Resource, Mode, Range, Resolution.
  - Network/Spectrum analyzer: Resource, Model, Channel, Trace, Marker, Start/Stop/Center frequency, Span.

## Current DevLib API mapping examples
- Power supply:
  - `CDCPowerSupply.Instance.Open(resource)`
  - `SetOutputChannel(channel)`
  - `DCSetVoltage(voltage)`
  - `DCSetCurrent(current)`
  - `DCMeasureVolt()` / `DCMeasureCurrent()`
- Signal generator:
  - `CSignalGenerator.Instance.Open(resource)`
  - `SetFreq(frequency)`
  - `SetOutputPower(level)`
  - `SetRFSweep(onOff)`
  - `GetFreq()` / `GetOutputPower()`
- Oscilloscope/DMM:
  - `COscilloscope.Instance.SCOPEViewChannel(channel)`
  - `SCOPEChannelSetVol(channel, range)`
  - `SCOPETimeRange(timeRange)`
  - `SCOPEMeasureVoltAmp()`
  - `CDigitalMultimeter.Instance.Open(resource)`
  - `ReadData(range, resolution, mode)`
- Network analyzer:
  - `CNetworkAnalyzer.Instance.LinkCheck(model)`
  - `SetStartFrequency(startHz)` / `SetStopFrequency(stopHz)`
  - `ActivateMarker(marker)` / `ReadMarkerAmp(channel, trace, marker)`
  - `CentFreq(channel, centerHz)` / `SpanFreq(channel, spanMHz)`

## Important boundary
- Do not claim full hardware connection coverage if a DevLib public class has no open/session method.
- In the observed codebase, `COscilloscope` and `CNetworkAnalyzer` expose many session-dependent methods but no `Open(resource)` public method. In that case:
  - Still accept Resource input in the WPF UI for operator clarity.
  - Report it as mapping/documentation only.
  - Only call the session-dependent methods when the user explicitly enables hardware calls, and state the session prerequisite.
- Keep real adapter/session construction as a follow-up DevLib API task rather than hiding it inside WPF.

## Verification checklist
1. Build the referenced DevLib DLL first:
   - `dotnet build C:\Users\yjs\Desktop\JAN\DevLib\DevLib\DevLib.csproj -c Debug`
2. Build both project and solution when present:
   - `dotnet build DevLibInstrumentWpf.csproj -c Debug`
   - `dotnet build DevLibInstrumentWpf.sln -c Debug`
3. Launch smoke:
   - `timeout 5s dotnet run --no-build --project DevLibInstrumentWpf.csproj -c Debug`
   - Treat timeout with no startup error as a WPF launch pass.
4. Check Korean text for replacement characters (`�`) in XAML, code-behind, and README.
5. Run `git diff --check`.

## Reporting notes
- Separate deterministic PASS/FAIL judgement from actual device I/O claims.
- Report any existing DevLib build warnings separately from WPF wiring failures.
- Mention exact changed files and whether `DevLib.dll` remains the consumed dependency.
