# MFU BIT Task Mapping (Task07 vs Task10)

## Why this note exists
In JAN K2 sibling rollouts, users may ask to "apply the same way" across equipment families. BIT automation logic can be equivalent, but **the BIT test task number is not always the same**.

## Confirmed mapping pattern
- CESU / GESU: BIT automation landed in `UUT01_Task07`.
- MFU_1 / MFU_2: BIT automation target is `UUT01_Task10` (Task07 is a different test flow).

## Safe rollout checklist
1. Locate sibling project files (`*.csproj`) and inspect `<Compile Include="UUT01_TaskNN.cs" />` entries.
2. Open the candidate Task files and verify where manual BIT verdict currently exists (`UserInput(..., PASSFAIL)`).
3. Check main procedure registration (`AddTask(UUT01_TaskNN)`) for the actual executed order.
4. Apply automatic BIT verdict logic only to the confirmed BIT task number per sibling.
5. Verify main receive loop carries BIT frame channels and parser linkage before task-level polling logic is trusted.

## BIT frame linkage pattern used in this rollout
- RT2BC(5,4,1) -> POBIT
- RT2BC(5,5,1) -> IBIT
- RT2BC(5,6,1) -> PBIT
- Parsed arrays: `pobitBit`, `ibitBit`, `pbitBit`

## Reporting rule
When delivering rollout status, explicitly state:
- which sibling used Task07 vs Task10,
- that mapping was validated before code copy,
- per-sibling build result (success/failure + error count).
