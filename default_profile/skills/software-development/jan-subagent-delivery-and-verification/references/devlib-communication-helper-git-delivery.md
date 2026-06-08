# DevLib communication helper delivery and git hygiene

## When this applies
Use this when delivering DevLib shared communication/helper work such as `RemoteAccess`, ARINC/CCSDS/I2C/SPI/SpaceWire/SpaceFibre helpers, or related `Read.txt`/root README documentation.

## Implementation boundary
- Keep DevLib additions project-neutral: generic protocol codecs, metadata helpers, deterministic loopback helpers, and wrapper safety improvements.
- Do not add TPS task numbers, BIT pass/fail rules, K2/KGPS/KCPS-specific ICD semantics, or equipment-specific judgment logic to DevLib.
- For SSH helpers, prefer OpenSSH/key/agent based command execution rather than storing passwords in DevLib.
- For Telnet helpers, document plainly that it is plaintext and should be limited to closed test/equipment networks.

## Verification pattern
1. Build DevLib after code/document changes:
   - `dotnet build DevLib/DevLib.csproj -c Debug --no-restore -v:minimal`
2. If a helper can be validated without real hardware, create a temporary smoke project outside the repository and link only the touched `.cs` files.
   - Validate deterministic behavior such as option construction, codec round-trips, loopback queue behavior, timeout handling, and Telnet prompt/read/write flow.
   - Delete the temporary project before committing.
3. Check for project-specific residue in new common folders:
   - `K2`, `KGPS`, `KCPS`, `POBIT`, `IBIT`, `PBIT`, `RscDo`, `TPSManager`, `ATESWLIB`.
4. Re-open Korean documentation with a file reader before reporting, to confirm the root README/Read.txt text is present and legible.

## Git delivery pattern
1. Set local repository identity for this DevLib/JAN repository before committing if the user asks to commit as JAN:
   - `git config user.name JAN`
   - `git config user.email JAN@genohco.com`
2. Preserve existing `.gitignore` entries when adding ignores for `.vs/`, build intermediates, logs, and smoke artifacts. Do not overwrite old ignore rules.
3. Remove or avoid staging temporary smoke artifacts. If `.vs` files are locked by Visual Studio, do not fight the lock; ensure `.vs/` is ignored and not staged.
4. Update the root `README.md` with a concise progress summary: implemented modules, verification command/result, smoke result, and remaining hardware/runtime cautions.
5. Stage intentionally, then run:
   - `git diff --cached --stat`
   - `git diff --cached --check`
6. Commit with a concise functional message and push to the active branch.
7. Verify push by comparing local and remote SHAs:
   - `git rev-parse HEAD`
   - `git ls-remote origin refs/heads/<branch>`

## Reporting notes
- Report the commit hash, author identity, branch, remote, build result, and remote SHA match.
- Separate compile verification from real-equipment verification. Do not imply SSH/Telnet/ARINC hardware communication was tested unless actual equipment was contacted.
- Mention if warnings remain and distinguish pre-existing/library-wide warnings from errors introduced by the change.
