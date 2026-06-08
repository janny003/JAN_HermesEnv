# DevLib RemoteAccess SSH/Telnet helper pattern

## When this applies
Use this when adding or reviewing `C:\Users\yjs\Desktop\JAN\DevLib\DevLib\RemoteAccess` or other reusable remote-session helpers in DevLib.

## Boundary
Keep RemoteAccess project-neutral:
- SSH command execution wrapper, argument/options construction, timeout/result capture.
- Telnet/TCP text session helper: connect, write, read available, read until prompt, close.
- Generic documentation (`README.md` and/or `Read.txt`) with usage examples and security notes.

Do not put these in DevLib RemoteAccess:
- Equipment-specific login scripts, prompt assumptions, command/result judgment logic.
- TPS/ICD/task-number logic or project names such as K2/KGPS/KCPS.
- Password storage or automatic password entry. Prefer key/ssh-agent/OpenSSH config.

## Recommended implementation shape
- `RemoteAccessResult.cs`: `Success`, `Output`, `Error`, `ExitCode`, `Elapsed`.
- `SshConnectionOptions.cs`: host/user/port/key/options, `BuildSshArguments`, display command helper.
- `SshCommandClient.cs`: call platform OpenSSH (`ssh.exe`) with `ProcessStartInfo.ArgumentList`, redirect stdout/stderr, enforce timeout, return `RemoteAccessResult`.
- `TelnetSession.cs`: `TcpClient`/`NetworkStream`, `Connect`, `Write`, `WriteLine`, `ReadAvailable`, `ReadUntil`, `ReadUntilAsync`, `Close`/`Dispose`.
- Filter common Telnet IAC negotiation bytes (`IAC DO/DONT/WILL/WONT`) from text reads.
- Include both markdown README and plain `Read.txt` if the surrounding DevLib protocol folders use `Read.txt`.

## Verification
1. Full DevLib build:
   - `dotnet build DevLib/DevLib.csproj -c Debug --no-restore -v:minimal`
   - Report success/failure and first relevant compile error. Existing unrelated warnings can be summarized separately.
2. Boundary search:
   - Search RemoteAccess for project-specific terms: `K2|KGPS|KCPS|POBIT|IBIT|PBIT|RscDo|TPSManager|ATESWLIB`.
   - Search for native/vendor dependencies: `DllImport|Renci|SshNet|SSH.NET`.
3. Isolated smoke project:
   - Link only RemoteAccess `.cs` files into a temp console project.
   - Verify SSH option/display construction and `RemoteAccessResult` behavior.
   - Verify Telnet read/write/read-until using local `TcpListener` loopback, including IAC byte filtering.
   - Remove the temp project after the run.

## Pitfalls
- DevLib has namespaces/classes that can shadow BCL names. If `Thread.Sleep` resolves as `DevLib.Thread`, use `global::System.Threading.Thread.Sleep(...)` or fully qualify similar BCL calls.
- When creating a temp smoke project with `dotnet new console`, do not add a second `.csproj` in the same directory unless `dotnet run --project <file>` is explicit. Prefer overwriting the generated csproj.
- Git status in DevLib may contain unrelated protocol/helper changes. Report RemoteAccess changes separately and do not imply all working-tree changes belong to the current task.
- Actual SSH equipment communication is not proven by an argument-construction smoke test. State clearly whether real device login was tested or not.
- Telnet is plaintext; document that it should be used only for closed test networks or equipment control contexts.
