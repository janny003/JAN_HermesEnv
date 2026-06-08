# ATESWLIB C1553B BIT extension shim pattern

## Trigger
Use this only as a fallback or short-lived diagnostic workaround when K2.sln fails with CS1061 on `C1553B.GetPOBIT`, `C1553B.GetIBIT`, or `C1553B.GetPBIT` and the preferred Core parser path cannot be applied immediately.

Preferred durable fix for this user's ATESWLIB workflow: implement or verify the parser methods in Core source first:
- KGPS/GESU/MFU `C1553B` path: `K2/TestProgram/Core/Data/KGPS_2/1553BICD.cs`
- CPS/CESU/KCPS/PA `C1553B1` path: `K2/TestProgram/Core/Data/KCPS_2/1553BICD.cs`

See `references/ateswlib-core-bit-parser-preferred-path.md` before using this shim.

Observed failing callers included TPS projects that instantiate `C1553B myd = new C1553B();` and then call:

```csharp
pobitBit = myd.GetPOBIT(msgdataPOBIT);
ibitBit = myd.GetIBIT(msgdataIBIT);
pbitBit = myd.GetPBIT(msgdataPBIT);
```

## Why this happens
Do not assume that a method found in a Core source file is visible to every TPS project. In ATESWLIB, similar parser code may exist on `C1553B1` or in sibling parser files, while a given TPS caller is compiled against `C1553B` and therefore still raises CS1061.

## Fallback shim pattern
Use this only after the Core parser path has been checked and cannot be used immediately. A narrow compatibility shim can unblock diagnosis, but should not be left as the durable implementation when the user expects parser ownership to remain in Core:

1. Add a project-local static extension class in the same namespace already imported by the caller, usually:
   - `namespace Core.Data.Excalibur.KGPS_2`
2. Implement extension methods for `C1553B`:
   - `public static ushort[] GetPOBIT(this C1553B c1553b, ushort[] inputData)`
   - `public static ushort[] GetIBIT(this C1553B c1553b, ushort[] inputData)`
   - `public static ushort[] GetPBIT(this C1553B c1553b, ushort[] inputData)`
3. Return a 9-element array extracted from ICD bit numbers 1~9 using `(inputData[0] >> bitNo) & 0x0001`.
4. Guard null/empty input and out-of-range bit numbers by returning 0.
5. Add the file to every affected TPS project `.csproj` with `<Compile Include="C1553BBitExtensions.cs" />`.

## Projects to check first
The CS1061 pattern has appeared in:
- `K2/TestProgram/KGPS_1`
- `K2/TestProgram/KGPS_2`
- `K2/TestProgram/GESU`
- `K2/TestProgram/MFU_1`
- `K2/TestProgram/MFU_2`

PA/CESU/KCPS may use `C1553B1` and already compile, so verify actual receiver type before changing.

## Verification
1. Rebuild `K2/K2.sln` with `Debug|x86`.
2. Grep the build log for `error CS` and specifically confirm CS1061 disappeared.
3. Rebuild `AteMgr/AteMgr_K2.sln` with the same configuration.
4. Static-recheck the affected TPS projects before reporting success:
   - Confirm the five extension files are byte-identical or hash-identical when the same shim is intended.
   - Confirm each affected `.csproj` contains `<Compile Include="C1553BBitExtensions.cs" />`.
   - Confirm each main caller imports the namespace where the extension class lives, e.g. `using Core.Data.Excalibur.KGPS_2;`.
   - Confirm the receiver is actually `C1553B` at the call site; `C1553B1` callers may already use Core methods and do not need this shim.
   - Confirm POBIT/IBIT/PBIT are separated at the call site: `GetPOBIT(msgdataPOBIT)`, `GetIBIT(msgdataIBIT)`, `GetPBIT(msgdataPBIT)`.
   - Search for stale mixed-parser patterns such as `ibitBit = myd.GetPowerOnBIT(...)`, `pbitBit = myd.GetPowerOnBIT(...)`, `GetPowerOnBIT(msgdataIBIT)`, and `GetPowerOnBIT(msgdataPBIT)`.
5. Clean build-output noise (`BIN`, `obj`, caches) from the working tree, leaving only source and `.csproj` changes.
6. Report both solution results and the final `git status --short` source changes; if build artifacts are still present, explicitly separate them from the intended source changes.

## Pitfall
If the extension file is created but not added to the project `.csproj`, the source will exist on disk yet the project will still fail with CS1061. Always verify the `.csproj` compile include.

A passing full solution build is necessary but not enough for this class of BIT parser fix. Also verify semantic wiring: `powerArray` may still call the legacy `GetPowerOnBIT(msgdataPOBIT)` for compatibility, but `ibitBit` and `pbitBit` must not reuse the PowerOnBIT parser or POBIT receive buffer.