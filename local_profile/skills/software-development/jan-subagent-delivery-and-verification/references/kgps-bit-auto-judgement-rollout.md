# KGPS BIT Auto-Judgement Rollout Checklist

## Scope
Apply CESU/GESU/MFU-style automatic BIT judgement to `KGPS_1` and `KGPS_2` safely.

## Why this reference exists
KGPS siblings can diverge in task-file mapping and parser API surface. A direct copy from other equipment often compiles with hidden mismatches.

## Preconditions
1. Confirm target root: `C:\Users\yjs\Desktop\JAN\ATESWLIB\K2\TestProgram`
2. Confirm BIT task file actually compiled in each sibling `*.csproj`
3. Confirm available parser methods in `Core/Data/*/1553BICD.cs`

## Safe rollout sequence
1. Locate BIT task candidates by PASS/FAIL input usage.
2. In each sibling, verify compile include:
   - `KGPS_1.csproj` may include `UUT01_Task38.cs` even when analysis started from `Task37`.
   - Treat `csproj Include` as build truth.
3. Replace manual PASS/FAIL with automatic judgement logic:
   - Wait for BIT reception update.
   - Apply ICD rule set:
     - POBIT/IBIT: bit1=1, bit2~9=0
     - PBIT: bit1~9=0
4. In main loop, add/verify RT2BC channels and per-frame parsing/forwarding:
   - `(5,4,1)` -> POBIT
   - `(5,5,1)` -> IBIT
   - `(5,6,1)` -> PBIT
5. Parser compatibility step (mandatory):
   - If `GetPOBIT/GetIBIT/GetPBIT` do not exist, use available method path (e.g., `GetPowerOnBIT`) and map outputs consistently.
6. Rebuild both siblings immediately with same config and report both outcomes.

## Verification commands (Git-Bash)
- `"/c/Windows/Microsoft.NET/Framework/v4.0.30319/MSBuild.exe" "C:\Users\yjs\Desktop\JAN\ATESWLIB\K2\TestProgram\KGPS_1\KGPS_1.csproj" -t:Build -p:Configuration=Debug -p:Platform=AnyCPU`
- `"/c/Windows/Microsoft.NET/Framework/v4.0.30319/MSBuild.exe" "C:\Users\yjs\Desktop\JAN\ATESWLIB\K2\TestProgram\KGPS_2\KGPS_2.csproj" -t:Build -p:Configuration=Debug -p:Platform=AnyCPU`

## Report contract
- Always include: target csproj, configuration/platform, error count, first core error (or success evidence).
- If only warnings remain, state "error 0, warnings only" explicitly.

## Common pitfalls
- Assuming task number is identical across siblings.
- Editing task file not referenced by `csproj`.
- Calling parser methods that are not implemented in KGPS data class.
- Declaring completion before running both sibling builds.