# ATESWLIB BIT 수정 후 ICD 재검증 체크

Use when the user asks to re-check JAN `C:\Users\yjs\Desktop\JAN\ATESWLIB` BIT code against ICD documents, especially after adding or modifying `UUT01_TaskNN.cs` tasks.

## Source documents to check
- `C:\Users\yjs\Desktop\JAN\ICD\포수조준경 2형 ICD.hwp`
- `C:\Users\yjs\Desktop\JAN\ICD\전차장 조준경 2형 ICD.hwp`
- `C:\Users\yjs\Desktop\JAN\ICD\전차장 조준경 1형 ICD.hwp`
- `C:\Users\yjs\Desktop\JAN\ICD\DTP2형 ICD.hwp`
- `C:\Users\yjs\Desktop\JAN\ICD\DTP1형 ICD.hwp`
- `C:\Users\yjs\Desktop\JAN\ICD\K2조준경_열상_성능개선_통신ICD_v3.5_220914.xlsx`

## Required checks
1. Confirm task wiring, not only code existence:
   - `*Main_UUT01.cs` has the correct `AddTask(UUT01_TaskNN)`.
   - `*.csproj` includes `<Compile Include="UUT01_TaskNN.cs" />`.
   - `CheckByStringValue(big, small, ...)` numbers match the task number and expected subtest ordering.
2. Compare BIT semantics against ICD:
   - POBIT/IBIT: bit1 is a completion flag and should be `1`; bit2~bit9 are fault bits and should be `0`.
   - PBIT: bit1~bit9 should all be `0` for normal.
3. Check that frame meaning and parser names stay aligned:
   - Prefer `GetPOBIT(msgdataPOBIT)`, `GetIBIT(msgdataIBIT)`, `GetPBIT(msgdataPBIT)`.
   - Avoid leaving `GetPowerOnBIT(...)` reused for IBIT/PBIT when parser-specific methods exist; it may compile but obscures ICD meaning.
4. For TIU_2 Task08:
   - Do not treat `CommReceive` existence alone as ICD-compliant automatic judgement.
   - If final result still uses `UserInput("8.5", PASSFAIL)`, report it as manual judgement remaining and not full ICD automatic judgement.
   - Verify `IBITRequest`, `CBITRequest`, and `CBITDetailRequest` each have `CommSend` + `CommReceive`, then inspect/implement response content parsing.
   - Cross-check `C:\Users\yjs\Desktop\JAN\TIUSimulator\MainPanel\MainPanelDlg.cpp` when the user says “TIUSimulator TIU_2 보고 bit 다시 확인”:
     - `DSP_TO_SYSTEM_VIDEOACK_STATUS`: `m_RecvVideo.VideoStat[1].Bit6 == _OFF` means IBIT/PBIT OK; `_ON` means FAIL.
     - `DSP_TO_SYSTEM_VIDEOACK_DETAILBIT`: `DetailBit[0]` and key `DetailBit[1]` fault bits use 0 = normal, 1 = fault. Treat Detail BIT as more than receive-existence.
     - For Detail BIT response in ATESWLIB `UUT01_Task08.cs`, require DLE/STX, `Command 03H`, `detail0 == 0`, `detail1 & 0xE2 == 0` for board/communication/cool-ready bits, `detail1 & 0x10 == 0` for detector SERDAT, and cooling status `(detail1 & 0x0C)` in `{0x00, 0x04}` (Cool Done or Cooling). `0x08` is Cool Fail and should fail.
   - After changing Task08, run a small deterministic smoke check with normal/cooling/fault/wrong-command samples before MSBuild, then build both `K2/TestProgram/TIU_2/TIU_2.csproj` and `K2/K2.sln`.
5. For KDTP_2 Task11:
   - PO-BIT is power-on/self-test report.
   - P-BIT should be independently received/validated as periodic BIT, not inferred by reusing the PO-BIT receive buffer.
   - I-BIT should be request/response based and interpreted according to ICD result bits/lists, not only by list count unless that mapping is documented.
6. Rebuild all touched BIT projects after the semantic review.

## Known module mapping from the verified session
- CESU: Task07
- GESU: Task07
- MFU_1: Task10
- MFU_2: Task10
- PA_2: Task18
- KCPS_1/KCPS_2: Task35
- KGPS_1: Task37
- KGPS_2: Task38
- KDTP_2: Task11
- TIU_2: Task08

## Legacy GPS/CPS bit-number cross-check
When the user questions whether `bitNo - 1` is correct, re-check the legacy MFC references before answering:

- GPS: `C:\Users\yjs\Desktop\JAN\GPS\JoystickDlg.cpp`
  - `DecodeBiteInfo(USHORT data)` around line 1646.
  - `m_intBite0 = data & 0x0001` means ICD bit1 is the received word LSB.
  - `m_intBite1 = (data >> 1) & 0x0001` confirms subsequent bits are zero-based shifts.
  - `rb4[0]` -> POBIT, `rb5[0]` -> IBIT, `rb6[0]` -> PBIT.
- CPS: `C:\Users\yjs\Desktop\JAN\CPS\JoystickDlg.cpp`
  - `DecodeBiteInfo(USHORT data)` around line 1634.
  - Same `m_intBite0 = data & 0x0001`, `m_intBite1 = (data >> 1) & 0x0001` mapping.
  - Same `rb4[0]`/`rb5[0]`/`rb6[0]` channel mapping.

Core parser helpers that accept ICD bit numbers `1..9` should therefore use:

```csharp
return (ushort)((inputData[0] >> (bitNo - 1)) & 0x0001);
```

Explain the distinction clearly:
- ICD bit7 -> `(inputData[0] >> 6) & 0x0001`.
- C/C# zero-based bit index 7 -> `(inputData[0] >> 7) & 0x0001`.

## ICD extraction and verification technique
- HWP source documents can be text-extracted with `hwp5txt`, but many embedded tables/figures may appear only as `<표>`/`<그림>`. Do not overclaim table-cell details from extracted text alone.
- Still use the extracted text to confirm durable semantic clues such as LSB wording, BIT result meaning (`1` = 이상/fault, `0` = 정상), and PO-BIT/P-BIT/I-BIT report sections.
- For the K2 thermal sight Excel ICD, use a spreadsheet reader (`openpyxl`/similar) to dump non-empty cells before keyword searching; it preserves more BIT lines than the HWP text extraction.
- Combine ICD document evidence with legacy GPS/CPS source evidence and Core parser source evidence. Treat the three-way agreement as stronger than any one extraction artifact.

## Parser smoke checks
After parser changes, run a deterministic bit-mapping smoke check before building:

```text
ICD bit1 -> word 0x0001 -> parser[0] == 1
ICD bit2 -> word 0x0002 -> parser[1] == 1
...
ICD bit7 -> word 0x0040 -> parser[6] == 1
ICD bit8 -> word 0x0080 -> parser[7] == 1
ICD bit9 -> word 0x0100 -> parser[8] == 1
POBIT/IBIT normal sample 0x0001 -> [1,0,0,0,0,0,0,0,0]
PBIT normal sample 0x0000 -> all zero
```

## Build sequence for this class of ATESWLIB BIT parser change
Use the verified paths and separate warnings from errors:

1. Core:
   - `MSBuild.exe K2/TestProgram/Core/Core.csproj /p:Configuration=Debug /p:Platform=AnyCPU`
   - Expected success artifact: `C:\Users\yjs\Desktop\JAN\ATESWLIB\Bin\TPS\Core.dll`.
2. K2 full solution:
   - `MSBuild.exe K2/K2.sln /p:Configuration=Debug /p:Platform=x86`
   - Existing warnings can include platform mismatch and unused-variable warnings; do not report them as failures unless an error occurs.
3. AteMgr:
   - `MSBuild.exe AteMgr/AteMgr_K2.sln /p:Configuration=Debug /p:Platform=x86`
   - Expected success artifact: `C:\Users\yjs\Desktop\JAN\ATESWLIB\AteMgr\Source\bin\x86\Debug\AteMgr.exe`.

## Reporting guidance
Separate three verdicts clearly:
- `빌드 기준`: compile success/failure.
- `Task 연결 기준`: AddTask/csproj/result-number mapping.
- `ICD 자동판정 기준`: whether response bits/frames are interpreted according to ICD.
- `비트 번호 기준`: explicitly distinguish ICD 1-based bit numbers from C/C# zero-based shift indexes when the user asks about expressions like `inputData[0] >> 7`.

Do not call a module fully ICD-compliant just because it builds and receives bytes. If it still relies on manual PASS/FAIL or reuses an unrelated BIT frame, mark it as a remaining ICD gap.
