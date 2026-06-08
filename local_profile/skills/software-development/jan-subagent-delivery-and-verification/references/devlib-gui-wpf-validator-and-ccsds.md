# DevLib GUI validator and CCSDS common module pattern

## When this applies
Use when the user asks to make DevLib easier to validate or consume from other JAN projects, especially requests involving `C:\Users\yjs\Desktop\JAN\DevLibGUI` or new protocol folders under `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\IO`.

## DevLibGUI WPF validator pattern
- If the user asks to replace the old DevLibGUI, the expected direction is a clean WPF validator app, not continued MFC/InstrumentControl maintenance.
- Keep the GUI focused on common reusable DevLib functions. Do not surface project-specific ICD/BIT/TPS task logic in this validator.
- Prefer linking only the touched common `.cs` files from DevLib instead of referencing the whole DevLib project. This avoids unrelated external dependencies such as OpenCV, Advantech, Imperx, COM references, or device DLLs blocking validator builds.
- For WPF validation screens, include simple deterministic sample actions and a visible log area so the user can confirm behavior without hardware.
- Use Korean UI text carefully and verify there are no mojibake replacement characters (`�`) in XAML/README outputs.

## CCSDS common module pattern
- Put CCSDS reusable code under `DevLib\IO\CCSDS`.
- Keep the module at CCSDS standard helper level only:
  - primary header create/parse
  - packet create/parse/TryParse
  - byte[] ↔ hex conversion
  - CRC-16/CCITT-FALSE compute/append/verify
  - simple packet/header containers and enums
- Do not encode project-specific APID meanings, equipment-specific TM/TC interpretation, secondary-header mission formats, BIT/ICD judgment, test numbers, or TPSData labels as executable validation rules.
- If the user asks for APID meaning examples, keep them explicitly non-normative: XML comments and README tables are acceptable, but parser/create/TryParse behavior must remain APID-agnostic.
  - Example-only APID notes may document meanings such as `0x001 = 위성 상태 데이터`, `0x002 = 전원계 데이터`, `0x003 = 자세제어 데이터`, `0x004 = 탑재체 카메라 데이터`, `0x005 = 고장 진단 데이터`.
  - Future project-specific APID policy belongs in each project `Core/Data` or TPS/TMTC layer, not in DevLib common CCSDS helpers.
- Make DLL consumption easy with a static facade class such as `CcsdsPacketCodec` and small DTO/container types.
- Use CCSDS big-endian/network byte order for multi-byte header fields.

## Adding CCSDS validation to an existing DevLibGUI WPF validator
When DevLibGUI already exists as the WPF common-function validator and the user asks to validate CCSDS there:

1. Keep the existing WPF shell and add a new `CCSDS Packet` tab rather than replacing the app again.
2. In `DevLibGUI.csproj`, link only the CCSDS common files from the sibling DevLib tree:
   - `..\DevLib\DevLib\IO\CCSDS\CcsdsEnums.cs`
   - `..\DevLib\DevLib\IO\CCSDS\CcsdsPrimaryHeader.cs`
   - `..\DevLib\DevLib\IO\CCSDS\CcsdsPacket.cs`
   - `..\DevLib\DevLib\IO\CCSDS\CcsdsCrc.cs`
   - `..\DevLib\DevLib\IO\CCSDS\CcsdsPacketCodec.cs`
3. The tab should cover deterministic, hardware-free checks:
   - APID input (`0x000..0x7FF`), sequence count, packet type selection.
   - data-field hex input.
   - packet generation with optional CRC-16/CCITT-FALSE append.
   - packet hex parse, header field display, CRC verify PASS/SKIP, user-data hex display.
4. Add the CCSDS generation/parse handlers to the existing "sample all" action so one click exercises both old 1553B checks and new CCSDS checks.
5. Update `README.md` with CCSDS validation items and linked source list.

## Verification
1. Search new DevLib common protocol folders and DevLibGUI edits for project-specific residue:
   - `K2`, `KGPS`, `KCPS`, `POBIT`, `IBIT`, `PBIT`, `RscDo`, `TpsManager`, `ATESWLIB`.
2. Run full DevLib build if useful, but treat existing external dependency failures separately.
3. Always create an isolated smoke project that links only the new/touched common module files and runs representative deterministic checks.
   - For CCSDS common code: create packet, parse header, verify APID/sequence/length, append/verify CRC, hex roundtrip, user payload extraction.
   - For DevLibGUI: `dotnet build DevLibGUI.sln -c Debug` and verify build output has 0 errors; remove `bin/obj` if not meant to commit.
4. For GUI validation changes, launch the built `DevLibGUI.exe`, confirm the process reaches running state, then terminate it cleanly. This catches WPF startup/XAML wiring errors that build alone may miss.
5. Search XAML/README/code for mojibake replacement characters (`�`) before reporting completion.
6. Report full-build status, isolated smoke success, DevLibGUI build, and launch check separately.

## Commit hygiene
- If committing after replacing DevLibGUI, stage deletions and new WPF files together; exclude `bin/`, `obj/`, `.vs/`, and user files via `.gitignore`.
- If DevLib common code and DevLibGUI live in separate repositories, commit each repository separately and report each commit hash/path distinctly.
