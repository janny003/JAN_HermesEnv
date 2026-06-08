# KDTP_2 / TIU_2 BIT 판정 및 11-project build stabilization

Use this reference when JAN ATESWLIB K2 BIT work touches KDTP_2, TIU_2, or sibling KGPS/MFU/KCPS projects.

## KDTP_2 Task11: do not reuse PO-BIT data for P-BIT

Observed issue:
- `UUT01_Task11.cs` received PO-BIT into `receivePO_BIT`.
- Step 11.2 then calculated P-BIT by calling `dtp2.GetPO_BIT_Report(receivePO_BIT)` again.
- This makes P-BIT a duplicate of PO-BIT instead of an independent channel/result.

Safer pattern:
1. Receive PO-BIT into `receivePO_BIT` and parse with `GetPO_BIT_Report`.
2. Receive P-BIT into a separate `receiveP_BIT` buffer and parse with `GetP_BIT_Report`.
3. Send I-BIT request, receive into `receiveI_BIT`, and parse with `GetI_BIT_Report`.
4. Put receive loops behind a class-level helper such as `TryReceiveBitReport(ref byte[] data, int timeoutMs)` so a missing device response does not create an infinite wait.

Example timeout split used successfully:
- PO-BIT: 60000 ms
- P-BIT: 10000 ms
- I-BIT: 30000 ms

## TIU_2 Task08: prefer ICD-based auto judgement over PASSFAIL prompt

Observed issue:
- Task08 had separate RS422 requests but final judgement still used `UserInput(...PASSFAIL)`.

Safer pattern:
1. Delay before first BIT request if the device needs initialization time.
2. Connect RS422 once.
3. For each request, use a 1:1 `CommSend` -> `CommReceive` pair:
   - `IBITRequest()` -> `ibitRx`
   - `CBITRequest()` -> `cbitRx`
   - `CBITDetailRequest()` -> `cbitDetailRx`
4. Parse with `Core.Data.Serial.KGPS_2.StTermalResponse.GetTermalResponse`.
5. Judge automatically:
   - PBIT/IBIT result: `pbitresult == 0`
   - CBIT result: `cbitresult == 0`
   - detail response: valid response exists and has enough bytes for the ICD parser
6. Only pass when all checks are true.

## KGPS/MFU BIT parser split

When the Core parser exposes semantic wrappers, call the frame-specific method rather than routing all frames through `GetPowerOnBIT`:
- POBIT frame -> `GetPOBIT`
- IBIT frame -> `GetIBIT`
- PBIT frame -> `GetPBIT`

Before changing callers, verify the Core data parser actually contains these wrappers; otherwise add wrappers first and keep `GetPowerOnBIT` as a compatibility alias to `GetPOBIT`.

## Build-stabilization pitfalls seen in K2 11-project verification

During 11-project `Debug|AnyCPU` MSBuild verification, two unrelated compatibility blockers can surface:

1. `using static System.Net.Mime.MediaTypeNames;`
   - In older C# compiler paths, this can fail with CS1041 around `static`.
   - If unused, remove the using instead of changing language version.
   - This occurred in KCPS_1/KCPS_2 `UUT01_Task28.cs`.

2. C# string interpolation `$"..."`
   - Some JAN Core project builds invoke the .NET Framework 4.x compiler path that rejects interpolation with CS1056.
   - Prefer `string.Format(...)` for compatibility in shared Core code.
   - Example: `string.Format("MBIN {0} {1}", display, binNumber) + "\n"`.

These are codebase compatibility fixes, not environment facts. Rebuild immediately after each change.

## Verification pattern

After BIT changes, run both targeted and aggregate builds:
1. Targeted project build right after edit, e.g. `KDTP_2.csproj` or `TIU_2.csproj`.
2. If Core data parser or shared compatibility code changes, build `Core.csproj` first so dependent projects use the new `Core.dll`.
3. Run the affected 11-project set and report every project result:
   - CESU, GESU, KCPS_1, KCPS_2, KDTP_2, KGPS_1, KGPS_2, MFU_1, MFU_2, PA_2, TIU_2.
4. Final report should include PASS/FAIL, error count, warning count, and first key error if any.
