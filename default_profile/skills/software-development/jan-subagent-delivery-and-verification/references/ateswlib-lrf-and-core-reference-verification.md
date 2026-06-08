# ATESWLIB LRF + Core Reference Verification

## When this matters
Use this reference when reviewing LRF/BIT-adjacent changes in `C:\Users\yjs\Desktop\JAN\ATESWLIB`, especially when KGPS/KCPS code calls newly added parser methods from `Core.Data.Excalibur.*`.

## Durable lesson from the LRF review
A source file may contain the expected parser method, but a dependent TPS project can still fail if it compiles against a stale or mismatched `BIN\TPS\Core.dll` reference.

Observed pattern:
- `Core\Data\KGPS_2\1553BICD.cs` contained methods such as:
  - `GetPOBIT(...)`
  - `GetIBIT(...)`
  - `GetPBIT(...)`
- `KGPS_1Main_UUT01.cs` called those methods.
- `K2.sln` still failed at KGPS_1 with CS1061 saying `C1553B` did not contain those methods.
- The root risk is reference/build ordering or stale referenced assembly behavior, not simply whether the method text exists in the source file.

## Verification sequence
1. Check source availability:
   - Search `Core\Data\KGPS_2\1553BICD.cs` and `Core\Data\KCPS_2\1553BICD.cs` for the called parser methods.
2. Check dependent project reference:
   - Inspect the TPS project `.csproj` for `Reference Include="Core"` and `HintPath>..\..\..\BIN\TPS\Core.dll`.
3. Build `Core.csproj` using its actual standalone platform:
   - `Debug|AnyCPU` is valid for `Core.csproj`; `Debug|x86` may fail with missing `OutputPath`.
4. Build the dependent TPS project using its actual standalone platform:
   - Some TPS projects also only define `Debug|AnyCPU` for standalone `.csproj` builds, while the solution may be driven as `Debug|x86`.
5. Then build `K2.sln` separately with the normal solution setting:
   - `Debug|x86`.
6. If K2 still fails with CS1061 after rebuilding Core, treat it as a reference/assembly mismatch or solution build-order issue and inspect the generated project build order and actual referenced `Core.dll` metadata.

## Reporting guidance
Separate the findings clearly:
- LRF task linkage status: AddTask / csproj Compile / TPSData JSON.
- Runtime-functional concerns: mode bit inversion, panel target mismatch, input validation.
- Build status: K2.sln and AteMgr_K2.sln separately.

Do not report “overall no issue” when `K2.sln` fails, even if the LRF task linkage itself looks correct.
