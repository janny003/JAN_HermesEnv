# DevLib Core Cross-Platform Primitives

Use this when modifying DevLib `Core` primitives such as shared memory, events, semaphores, mutexes, critical sections, threads, or time helpers for Windows/Linux compatibility.

## Goal
Keep existing Windows behavior stable while preventing non-Windows runtime failures from named OS primitives or Windows-only APIs.

## Files commonly involved
- `DevLib/Core/SharedMemory/CSharedMemory.cs`
- `DevLib/Core/Event/CEvent.cs`
- `DevLib/Core/Semaphore/CSemaphore.cs`
- `DevLib/Core/Mutex/CMutex.cs`
- Adjacent smoke-only files: `CCriticalSection.cs`, `CThread.cs`, `CTime.cs`

## Implementation pattern
1. Preserve the Windows path first.
   - Use `OperatingSystem.IsWindows()` or an equivalent runtime guard.
   - Keep named `EventWaitHandle`, `Semaphore`, `Mutex`, or `MemoryMappedFile` behavior on Windows unless the user explicitly asks for a breaking change.
2. Add non-Windows fallback deliberately.
   - For Event/Semaphore/Mutex, prefer unnamed local managed primitives when cross-process naming cannot be guaranteed.
   - Do not claim Linux named cross-process behavior unless it is actually verified.
3. For shared memory, prefer file-backed mapping on non-Windows.
   - Put backing files under temp, e.g. `%TEMP%` or `/tmp` plus a DevLib-specific subdirectory.
   - Convert user-provided memory names into safe filenames with a stable hash such as SHA256.
   - Avoid passing arbitrary `memName` values directly into filesystem paths.
4. Harden public methods against null handles and lifecycle reuse.
   - `Create` failure should return `false` when the class API is bool-style.
   - `Set`, `Reset`, `Wait`, `Lock`, `UnLock`, `Return`, `Read`, and `Write` should fail safely rather than throwing `NullReferenceException`.
   - If a class tracks `_disposed`, reset it on successful `Create`/re-create paths so `Destroy()` followed by `Create()` does not leave the object permanently disposed.
   - When adding nullable annotations to handle fields, keep method signatures and smoke-project nullable context consistent enough that touched-file warnings are meaningful.
5. Keep the report precise.
   - Separate “Windows named primitive behavior preserved” from “Linux fallback compiles/should avoid Windows-only API failure”.
   - If Linux runtime was not available, say so plainly and do not overstate verification.

## Verification checklist
1. Full DevLib build when possible:
   - `dotnet build DevLib/DevLib.csproj -c Debug`
   - Report success/failure, error count, warning count, and whether CA1416 Windows-only warnings remain in touched Core files.
   - Also filter the build log for each touched Core file and report touched-file warning/error counts separately. This avoids hiding new Core warnings inside existing DevLib-wide warning noise.
2. Isolated Core compile/smoke when full build is noisy or external dependencies interfere.
   - Link only touched Core files plus minimal adjacent Core files into a temporary console project outside the repo.
   - Keep the smoke project `Nullable` setting aligned with DevLib (`enable`) when nullable annotations were added; otherwise smoke-only CS8632/CS86xx noise can misrepresent the touched files.
   - Exercise:
     - `CCriticalSection` enter/leave/TryEnter
     - `CEvent` create/set/reset/wait
     - `CSemaphore` create/wait/return
     - `CMutex` create/lock/unlock
     - `CSharedMemory` create/write/read round-trip
     - `CThread` callback execution
     - `CTime` formatting
   - Print an explicit pass marker such as `CORE_SMOKE_PASS`.
3. Linux verification hierarchy:
   - Prefer actual Linux runtime smoke if Docker/WSL/Linux host is available.
   - If actual Linux runtime is unavailable, still try a Linux RID publish/compile smoke before stopping: `dotnet publish <smoke>.csproj -c Release -r linux-x64 --self-contained false --source https://api.nuget.org/v3/index.json -v minimal`.
   - The explicit `--source https://api.nuget.org/v3/index.json` is useful when the host is configured only with Visual Studio Offline Packages and cannot restore `Microsoft.NETCore.App.Host.linux-x64`.
   - If Linux RID publish succeeds but no Linux runtime is available, report “linux-x64 publish/compile passed; Linux OS runtime smoke unverified” rather than claiming full Linux runtime validation.
   - Do not save missing Docker/WSL or offline package source as a durable rule; those are environment setup states.

## Reporting template
- `Jangli : 변경 범위: <Core files>`
- `Jangli : Windows 경로: named primitive 유지 여부`
- `Jangli : 비Windows 경로: fallback 방식과 한계`
- `Jangli : 빌드 검증: <command/result/warnings>`
- `Jangli : smoke 검증: <scope/pass marker>`
- `Jangli : 남은 위험: Linux 실기동 여부와 named cross-process 보장 범위`
