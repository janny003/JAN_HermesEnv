# Policy pack rollout checklist (Windows mirrored repos)

Use when users ask to "apply policy" across similar project trees.

## Discovery
- Confirm target path exists.
- If missing, enumerate nearest parent and compare similar names.
- Prefer explicit absolute Windows paths in report output.

## Rollout pattern
- Source policy files from a canonical folder (example: `C:\\Users\\<user>\\Desktop\\JAN\\Policy`).
- Create `policies/` folder in each active repo root.
- Copy all policy markdown files in one transaction-like pass.

## Verification
- List resulting `policies/*.md` for each root.
- Search README for an "applied policy" section or add one.
- Ensure mirrored roots contain identical policy filenames.

## Common pitfall
- Updating only one tree (`repo/`) while forgetting the mirrored tree (`Policy/repo/`) causes divergence in later agent runs.
