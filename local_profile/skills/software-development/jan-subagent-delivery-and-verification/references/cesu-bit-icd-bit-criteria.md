# CESU BIT ICD Bit Criteria (Session Note)

Purpose: Prevent mis-implementation of BIT pass/fail logic in CESU Task07.

## Confirmed rules
- PowerBIT
  - bit[0] == 1 : completion flag (required)
  - bit[1..8] == 0 : fault bits must be clear
- IBIT
  - bit[0] == 1 : completion flag (required)
  - bit[1..8] == 0 : fault bits must be clear
- PBIT
  - bit[0..8] == 0 : all clear required

## Implementation reminder
- Keep receive mapping and variable names aligned:
  - `(4,4,1)` -> power bit status array
  - `(4,5,1)` -> ibit status array
  - `(4,6,1)` -> pbit status array
- Avoid naming `(4,4,1)` payload as `cbitBit`; this is a readability trap and causes future maintenance errors.

## Validation checklist after edits
1. Build `K2.sln` with `Debug|x86`.
2. Confirm no new compile errors.
3. Re-check Task07 pass/fail predicates against this bit table before reporting completion.
