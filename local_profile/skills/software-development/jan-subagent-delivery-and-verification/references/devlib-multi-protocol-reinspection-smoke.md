# DevLib multi-protocol reinspection and smoke verification

## When this applies
Use this note when the user asks to "recheck the same way" across several DevLib IO protocol folders, especially mixed sets such as I2C, SPI, SpaceWire, SpaceFibre, CCSDS, and CAN.

## Durable lesson
Do not stop at folder existence. For this class of request, verify three layers:
1. File/API shape for each requested protocol.
2. Implementation boundary: vendor-free common helper versus real vendor/hardware wrapper.
3. Build plus deterministic smoke behavior.

## Protocol boundary checklist
- I2C/SPI/SpaceWire/SpaceFibre/CCSDS should normally remain project-neutral common helpers unless the user provides a concrete controller, card, FPGA, or SDK target.
- CAN in the current DevLib tree is different: it is a real vendor-backed wrapper area, not a vendor-free helper.
  - Kvaser path uses `Kvaser.CanLib`.
  - UCAN path uses `uCANDLL.dll` P/Invoke and native deployment.
  - Report CAN separately from vendor-free helper modules.
- For all protocols, distinguish "common DLL helper works" from "real hardware communication verified". Hardware verification requires device drivers, adapters, and project ICD-level transaction logic.

## DevLibGUI coverage-extension pattern
When the user asks to modify `DevLibGUI` so that all DevLib IO communication code can be verified by communication type, do not limit the GUI to previously vendor-free helpers. Preserve the distinction between deterministic helper validation and vendor/hardware wrapper coverage.

Recommended WPF additions:
- Keep existing deterministic tabs for `1553B`, `CCSDS`, `SPI`, `I2C`, `SpaceWire`, `SpaceFibre`, and ARINC629/664/717 software-loopback.
- Add a separate tab/group for `TCP`, `UDP`, `Serial`, `CAN`, and `ARINC429` rather than mixing them into helper-only tabs.
- For `TCP`/`UDP`/`Serial`, expose public API coverage and readiness information (for example detected COM ports) without claiming full send/receive unless endpoint, port, server lifecycle, and hardware/adapter conditions are defined.
- For `CAN` and `ARINC429`, report vendor wrapper API coverage and dependency boundary explicitly:
  - Kvaser CAN: `Kvaser.CanLib` wrapper, real verification requires Kvaser driver/device or virtual channel.
  - UCAN: `uCANDLL.dll` P/Invoke wrapper, real verification requires DLL/USB device.
  - ARINC429: `DD42992.dll` DDC wrapper, real verification requires DLL/card.
- If `DevLibGUI` references the built `DevLib.dll`, avoid adding new package references casually just to inspect optional APIs. A robust pattern for Serial readiness is reflection-based `System.IO.Ports.SerialPort` lookup so the GUI can still build when the direct package/reference is absent.
- The "run all samples" button should include the newly added coverage sections so one action exercises every GUI-verifiable communication area.

Verification for this pattern:
- Build `DevLib` first, then `DevLibGUI`.
- Run a GUI launch smoke (`dotnet run --no-build -c Debug` with a timeout is acceptable) and treat a stable timeout with no crash as start-smoke pass.
- Search edited XAML/C# for replacement characters (`�`) and confirm Korean UI strings such as `통신별 전체 커버리지`, `검증 가능`, and `실제 통신은 장비 필요` render as normal text.

## Recommended reinspection sequence
1. List requested folders under `DevLib/DevLib/IO/<Protocol>` and confirm expected `.cs` files plus `Read.txt`.
2. Read or summarize public types/methods and namespace consistency.
3. Search for accidental native/vendor dependencies in vendor-free modules:
   - `DllImport|Kaya|STAR|4Links|NationalInstruments|vendor|\.dll|PInvoke|extern|Canlib|Kvaser|uCANDLL`
   - Treat prose hits such as "vendor-free" or enum names such as `StartOfPacket` as harmless; inspect context before reporting.
4. Run full DevLib build with both styles when practical:
   - `dotnet build DevLib/DevLib.csproj -c Debug --no-restore -v:minimal`
   - Visual Studio MSBuild from Git-Bash should use hyphen switches, not slash switches, because MSYS can strip `/p` and `/v`:
     - `'/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe' DevLib/DevLib.csproj -p:Configuration=Debug -p:RestorePackages=false -v:minimal`
5. Create a temporary smoke console under `%LOCALAPPDATA%/Temp` or equivalent and reference `DevLib.csproj`.
6. Smoke deterministic behavior:
   - I2C: 7-bit write/read address byte, 10-bit address bytes, register write/read-prefix, hex parse/roundtrip.
   - SPI: bus config, register read command, bit reverse, hex roundtrip.
   - SpaceWire: EOP and EEP roundtrip, full `0x00..0xFF` byte payload, CRC-8 vector `123456789 => 0xF4`, time-code boundary `63`.
   - SpaceFibre: segmentation/reassembly, sequence wrap `0xFE -> 0xFF -> 0x00`, frame byte parse, broadcast payload roundtrip, CRC-16/CCITT-FALSE vector `123456789 => 0x29B1`.
   - CCSDS: create/parse primary header, APID/sequence/length, CRC append/verify, user-data extraction, hex roundtrip.
   - CAN: compile/build-only by default unless hardware/drivers are explicitly available; do not claim real bus send/receive verification from software smoke alone.

## Reporting pattern for this user
Use concise subagent-name format:
- `Yuno :` overall status and conclusion.
- `Jangli :` exact paths, build/smoke evidence, and boundary classification.
- `Lucy :` test coverage and residual verification gaps.
- `Hiyuki :` Read.txt/documentation or UI/legibility notes if relevant.

Always include:
- Build command result: success/failure, error count, and warning class summary.
- Smoke result phrase, e.g. `PROTOCOL SMOKE PASS`.
- Residual risk: helper-only modules are not hardware communication; CAN still needs device/driver/hardware validation.

## Pitfalls
- In Git-Bash/MSYS, `MSBuild.exe ... /p:Configuration=Debug /v:minimal` can be transformed into `p:Configuration=Debug`/`v:minimal`, causing `MSB1008`. Use `-p:` and `-v:` switches instead.
- A failed first smoke run due to the temporary project missing restore assets is not a durable tool failure; rerun without `--no-restore` or perform restore first.
- If a smoke compile fails because the test guessed the wrong property name, inspect the actual DTO/container file and update the smoke code. Example: `SpaceWirePacket` exposes `Data`, not `Cargo`.
- Do not persist temporary smoke projects into the repo. Keep them under temp paths and report that source code was not modified if only smoke scaffolding changed.
