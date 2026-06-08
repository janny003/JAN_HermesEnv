# DevLib common library boundary

## When this applies
Use this when modifying `C:\Users\yjs\Desktop\JAN\DevLib`, especially shared IO/codec/util modules intended for reuse by multiple JAN projects.

## Boundary rule
DevLib is a common-function library. Keep only logic whose meaning stays valid across projects.

Keep in DevLib:
- Project-neutral protocol helpers such as MIL-STD-1553 command word creation/decoding.
- Generic word/hex conversion, payload extraction, sign extension, bit packing/unpacking.
- Hardware adapter layers only when they are not tied to a specific TPS task, ICD interpretation, or project workflow.

Do not keep in DevLib:
- K2/KGPS/KCPS-specific ICD codecs.
- POBIT/IBIT/PBIT or other BIT parsers whose bit numbering and pass/fail semantics come from one project's ICD.
- `TPSManager.RscDo` command string constants or wrappers.
- Test number, Task number, TPSData label, or equipment-specific judgment logic.

## Verification pattern
1. Search the target module for project-specific residues before reporting completion:
   - `K2`, `KGPS`, `KCPS`, `POBIT`, `IBIT`, `PBIT`, `RscDo`, `TpsManager`, `ATESWLIB`, project-specific class names.
2. If the full DevLib build fails due unrelated external dependencies, do not stop at that failure.
   - Create a temporary minimal smoke project that links only the touched common `.cs` files.
   - Compile/run representative checks for the common functions changed.
   - Delete the temporary project afterward.
3. Report both results separately:
   - Full DevLib build status and unrelated external dependency errors, if any.
   - Isolated common-module smoke result, including the exact command/output evidence.

## Reporting note
For this user, explicitly state that project-specific BIT/ICD logic remains in each project Core/Data or TPS layer, not DevLib. This addresses the user's correction that BIT parsers are not reusable common functions.
