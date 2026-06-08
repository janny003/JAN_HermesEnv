# DevLib ARINC429 Wrapper Verification

Use this reference when inspecting or modifying `DevLib\IO\Arinc429\CArinc429.cs` or adjacent DDC/DD42992 P/Invoke wrappers.

## Scope
- Applies to JAN DevLib ARINC429 wrapper review, bug fixing, and smoke verification.
- Keep DevLib changes limited to reusable protocol/device-wrapper behavior. Do not add project-specific TPS, ICD task, or UI logic here.

## Discovery checklist
1. Confirm the real path/name first. In the current codebase the folder/class spelling is `Arinc429`, even if the user says `Aring429`.
2. Compare every P/Invoke signature against the vendor headers under `IO\Arinc429\Include`.
3. For each wrapper method, record whether it:
   - returns the native status accurately,
   - silently converts failure to success,
   - swallows deployment exceptions such as `DllNotFoundException`, `BadImageFormatException`, or `EntryPointNotFoundException`,
   - passes a scalar pointer where the native API expects an array.

## Known wrapper risks to check
- `Open` should not always return `false`; it must reflect `InitCard` and any required setup status.
- `Close` and `DOConfigTimeStamp` should reflect native return values instead of returning a fixed value.
- `DOGetChannelCount` must inspect the native status, not treat "no exception" as success.
- `ReadRxQueueIrigOne` returns meaningful native status: `0` no word, `1` success, negative error. Preserve this distinction.
- `ReadRxQueueIrigMore` native signature returns `S16BIT`; do not declare it as `void`.
- `ReadRxQueueIrigMore` expects buffers for N words. Do not pass the address of a single `uint` when `s16N > 1`; require arrays and validate lengths before calling native code.
- `LoadTxQueueMore` should return native status/loaded count and validate `s16N <= u32Data.Length`.
- Prefer explicit `CallingConvention` when the vendor macro (`DDCAPI`) requires it; verify against the header/compiler convention rather than assuming.

## Smoke verification without hardware
1. Build a temporary isolated project that links only `CArinc429.cs` when full DevLib build is blocked by unrelated COM/video/equipment references.
2. Run a smoke program that instantiates the wrapper and calls safe entry points.
3. Test both DLL deployment states:
   - without `DD42992.dll`: expect and report `DllNotFoundException` or equivalent deployment failure,
   - with matching bitness DLL copied beside the executable: confirm native DLL loads and wrapper returns native statuses.
4. Report full DevLib build separately from isolated smoke results. A full `dotnet build` may fail on `ResolveComReference` under .NET Core MSBuild; this is not evidence that the ARINC429 source itself fails to compile.

## Reporting template
- `Jangli : ARINC429 경로/명칭 재실측: <path>`
- `Jangli : isolated smoke 결과: <success/fail and key output>`
- `Jangli : full DevLib build 결과: <success/fail; separate unrelated infrastructure failures>`
- `Jangli : wrapper 위험: <return-value, buffer, DLL deployment, bitness>`
- `Lucy : 하드웨어 없이 검증 가능/불가능 범위를 분리하면 ...`

## Hardware boundary
Without the actual ARINC429 card/driver environment, do not claim that channel enable, queue read/write, timestamp, or IRIG behavior is functionally correct. Limit the conclusion to compileability, DLL loading, wrapper status handling, and obvious P/Invoke/buffer safety.