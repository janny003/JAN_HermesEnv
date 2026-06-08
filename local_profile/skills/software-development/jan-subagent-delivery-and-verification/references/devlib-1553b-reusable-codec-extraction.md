# DevLib 1553B reusable codec extraction

Use this reference when the user asks to move ATESWLIB 1553B knowledge into DevLib for reuse, or to prepare 1553B logic for DevLibGUI/TestProgram without requiring Excalibur hardware.

## Durable pattern
1. Keep hardware-owning classes stable first.
   - Do not casually modify existing `CEXC1553B.cs` or device open/run/stop flows.
   - Extract pure logic first so regression risk stays low.
2. Split by responsibility.
   - `IO/1553B/Common/`: MIL-STD-1553 command word encode/decode, word/hex conversion, bit packing/sign-extension.
   - `IO/1553B/K2/`: KGPS/KCPS/K2 sight ICD codecs and BIT status parsing.
   - `IO/1553B/Excalibur/`: RscDo command/resource name constants only, not live device control.
3. Preserve existing byte order and semantics.
   - ATESWLIB/TpsManager-style `ushort[]` to hex string conversion may use `Buffer.BlockCopy` little-endian behavior; for example `0x1234` becomes `3412` in the hex string. Do not “fix” this unless the caller contract is explicitly changed.
   - MIL-STD-1553 word count 32 is encoded as 0 in the command word.
4. BIT parser rules to keep explicit.
   - POBIT/IBIT: first semantic bit is completion and should be `1`; following 8 fault bits should be `0`.
   - PBIT: semantic bits 1..9 should all be `0`.
   - Preserve legacy bit numbering as the default when matching existing ATESWLIB behavior, and expose an explicit option for zero-based ICD interpretation if needed.
5. Verification should not depend only on the full solution.
   - Build the new reusable `.cs` files in a temporary SDK-style classlib or equivalent isolated compile first.
   - Add a smoke test for command word roundtrip, word/hex roundtrip, BIT status pass/fail, and at least one KGPS/KCPS packing path.
   - Then attempt the full `DevLib.sln` build and report environment/restore failures separately from source-code compilation failures.

## Reporting notes
- State clearly whether existing files were modified or only new files were added.
- If full `DevLib.sln` fails because NuGet/SDK restore sources are incomplete, do not store that as a durable tool limitation; report it as current environment state only.
- For JAN reports, keep the `Jangli : ...` format and include exact verification command/result summary.