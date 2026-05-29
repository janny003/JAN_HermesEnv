# Role/Tone Policy Enforcement for Named Subagents

Use this when users require fixed named subagents with policy markdown files.

## Quick protocol
1. Discover policy files (`subagent_*.md`) in requested root.
2. Map each agent name -> role file path explicitly.
3. Confirm operation mode: real delegated subagents (not speaker-roleplay labels).
4. Execute with maximum safe parallelism; disclose any serialization constraints.
5. Re-check policy files on demand; if unchanged, report unchanged status.
6. Keep output format exactly as requested (e.g., `name : message`).

## Common failure to avoid
- Presenting multiple voices without actual delegation/execution.
- Applying role labels but ignoring tone/persona constraints.
- Updating only one of mirrored roots (`project/` vs `Policy/project/`).

## Validation checklist before final response
- [ ] Role file paths verified and readable
- [ ] Named-role mapping reflected in output
- [ ] Tone compliance preserved per role
- [ ] Parallel/serial execution truthfully reported
- [ ] Mirrored roots synchronized when files changed
