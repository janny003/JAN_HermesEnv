# ATESWLIB BIT subtest label reconciliation

Use this when comparing ICD/TPSData BIT labels against C# `CheckByStringValue` output slots.

## Durable lesson
Do not assume every JAN BIT task uses the same subtest order. Reconcile three sources before changing logic:

1. `BIN/TPSData/<PROJECT>.json`
   - Locate the `BIT 시험` task and its `Tests` labels.
   - Record the actual subtest labels, e.g. `1: POBIT`, `2: IBIT`, `3: PBIT`.
2. `K2/TestProgram/<PROJECT>/UUT01_TaskNN.cs`
   - Check each `CheckByStringValue(taskNo, subNo, ...)` target.
   - Verify that each subNo receives the same BIT type as the TPSData label.
3. Main receive loop / parser wiring
   - Verify independent receive buffers and parser functions:
     - POBIT -> `GetPOBIT(...)`
     - IBIT -> `GetIBIT(...)`
     - PBIT -> `GetPBIT(...)`
   - Treat any `ibitBit = ...GetPowerOnBIT(...)` or `pbitBit = ...GetPowerOnBIT(...)` as suspicious unless the project has no separated parser and the wrapper is explicitly equivalent.

## Known JAN patterns from this session
- CESU keeps TPSData order `1: IBIT`, `2: POBIT`, `3: PBIT`; do not force it to the common order without checking data.
- GESU, KGPS_1, KGPS_2, MFU_1, MFU_2 commonly use `1: POBIT`, `2: IBIT`, `3: PBIT`; if code writes IBIT to slot 1 and POBIT to slot 2, swap the output slots only after confirming TPSData.
- KDTP_2 Task11 should align with `11.1 POBIT`, `11.2 IBIT`, `11.3 PBIT`; do not reuse PO-BIT receive data for P-BIT judgment.

## Verification commands/patterns
- After edits, scan for parser misuse:
  - regex: `(ibitBit|pbitBit)\s*=\s*\w+\.GetPowerOnBIT`
- Re-scan `CheckByStringValue` calls and compare with TPSData labels.
- Build every touched project individually using the repository's known MSBuild pattern; report warnings and errors separately.

## Reporting
In the final report, explicitly separate:
- ICD/TPSData label reconciliation result
- parser wiring result
- modified files
- build result per project
