# DevLib ARINC429 wrapper safety pattern

Use when modifying `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\IO\Arinc429\CArinc429.cs` or similar native hardware wrappers.

## Durable lessons
- Treat ARINC429 wrapper work as a P/Invoke boundary task, not project-specific ICD/BIT logic. Keep fixes in DevLib limited to reusable hardware adapter safety: signatures, calling convention, return propagation, pointer/array safety, and DLL bitness/deployment notes.
- Cross-check C# P/Invoke declarations against the vendor headers before editing. For DDC ARINC429 headers, `DDCAPI` resolves through Windows `WINAPI`, so `CallingConvention.StdCall` is the safer explicit declaration.
- Do not convert native status-rich functions into unconditional `true`/`false`. Preserve native outcomes where the existing public API allows it, and only map to `bool` when the API already expects bool.

## Specific ARINC429 checks
1. `InitCard`, `ConfigTimeStamp`, `GetChannelCount`, and `FreeCard` return DDC error status; success is `0` (`ERR_SUCCESS`).
2. `GetLibVersionEx` uses `U16BIT*`; use `ushort*` on the C# side rather than signed `short*`.
3. `ReadRxQueueIrigOne` returns meaningful status: `0` queue empty, `1` success, negative error. Do not ignore it.
4. `ReadRxQueueIrigMore` returns `S16BIT` count/error, not `void`. Its output pointers are arrays sized at least `s16N`; never pass the address of one `uint` field when `s16N > 1`.
5. `LoadTxQueueMore` returns loaded count/error. Validate `s16N > 0`, array non-null, and `array.Length >= s16N` before pinning.
6. Backward-compatible convenience wrappers may keep legacy public fields (`pu32Data`, `pu32StampHi`, `pu32StampLo`) by copying the first returned item after a safe array call.

## Verification pattern
1. Search for all call sites before changing public signatures. If only the wrapper itself calls the method, a return-type improvement is lower risk.
2. Build a temporary isolated smoke project that links only `CArinc429.cs` when full DevLib is blocked by unrelated device dependencies.
3. In the smoke program, avoid calling native DLL functions unless the DLL and hardware environment are intentionally present. Exercise safe guard paths, such as invalid `s16N`/short arrays returning `0`, so compile and boundary checks are verified without hardware.
4. Remove temporary smoke project after collecting output.
5. Separately run full DevLib build with:
   - `dotnet build DevLib/DevLib.csproj -c Debug` to expose SDK/COMReference issues.
   - Visual Studio .NET Framework MSBuild when COM references are involved: `MSYS2_ARG_CONV_EXCL='*' 'C:/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe' DevLib/DevLib.csproj /p:Configuration=Debug /m`.
6. Report full-build failures separately from isolated ARINC429 smoke success. Missing OpenCvSharp/Advantech/Imperx-style dependencies are not ARINC429 regressions unless the modified file appears in the compiler errors.

## Reporting note
For this user, include the actual smoke output and explicitly state whether any `CArinc429.cs` compiler errors appeared in full DevLib build logs.
