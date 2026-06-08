# KCPS sibling BIT rollout checklist (KCPS_1/KCPS_2)

Use when one TPS line (e.g., PA_2 or CESU) has BIT added and user requests the same for KCPS siblings.

## 1) Main procedure sync (`*Main_UUT01.cs`)
- Add next Task registration line:
  - `AddTask(UUT01_TaskNN); // NN. BIT 시험`
- Expand test tracking capacity if fixed-size array exists:
  - `arrayTestNum = new bool[NN];`
- Add BIT status fields:
  - `pobitBit`, `ibitBit`, `pbitBit` as `ushort[9]`
- In `ProcessSendCanonMessage`:
  - Ensure frame creation includes `(4,4,1)`, `(4,5,1)`, `(4,6,1)`
  - Ensure receive buffers are separated (`msgdataPOBIT`, `msgdataIBIT`, `msgdataPBIT`)
  - Ensure parsing uses separated APIs:
    - `GetPOBIT`, `GetIBIT`, `GetPBIT`

## 2) Task file sync
- Create `UUT01_TaskNN.cs` per sibling project.
- Minimal flow:
  - `UserInput("NN.1", CONFIRM)`
  - Trigger `SelfTest = 1` then timeout polling
  - Auto-judge 3 checks and write:
    - `CheckByStringValue(NN, 1, POBIT)`
    - `CheckByStringValue(NN, 2, IBIT)`
    - `CheckByStringValue(NN, 3, PBIT)`
- Preserve existing Korean pass/fail constants (`strPass`/`strFail`).

## 3) Project include sync (`*.csproj`)
- Add compile include in each sibling:
  - `<Compile Include="UUT01_TaskNN.cs" />`

## 4) TPSData JSON sync (`BIN/TPSData/*.json`)
- Append task object with same Number/Title/Tests across siblings.
- Keep numbering contiguous and sorted by `Task[].Number`.
- Validate each JSON file:
  - parse success
  - last task number/title check
  - tests count check

## 5) Verification sync
- Build full solution (`K2.sln`, `Debug|x86`) immediately.
- Verify both sibling projects are actually compiled in log (`KCPS_1.csproj`, `KCPS_2.csproj`).
- Report: success/failure, errors=0 여부, warning summary.

## Notes
- Prefer separated naming (`POBIT/IBIT/PBIT`) end-to-end; avoid legacy `PowerBIT` mixed naming.
- If user asks "동일하게", mirror behavior and data shape, not only file creation.
