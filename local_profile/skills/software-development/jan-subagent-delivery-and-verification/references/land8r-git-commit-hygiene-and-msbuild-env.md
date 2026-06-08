# LAND8R/LAND8116 Git commit hygiene + MSBuild env retry

Use this when committing LAND8R/LAND8116 GUI changes after a verified build.

## Durable workflow lessons

1. Stage only intentional source/resource files.
   - Include `.cpp`, `.h`, `.rc`, `resource.h` when they are part of the requested UI/code change.
   - Do not stage Visual Studio local artifacts such as `*.APS` or `*.vcxproj.user`; remove them before final status if they are just generated noise.

2. Check `.rc` diffs for whitespace-only churn before committing.
   - A resource-editor or broad rewrite can add trailing whitespace across `TEXTINCLUDE`, `DLGINIT`, or EOF sections unrelated to the feature.
   - If the `.rc` diff contains large unrelated whitespace changes, rebuild the `.rc` from `git show HEAD:<path>` and reapply only the intended resource hunks using explicit CP949 decode/encode.
   - Verify with `git diff --cached --check` before commit.

3. Preserve JAN local git identity for this workspace.
   - Use repo-local identity when needed:
     - `git config user.name JAN`
     - `git config user.email JAN@genohco.com`

4. Git-Bash/MSBuild retry pattern for duplicate `tmp`/`TMP` environment keys.
   - Symptom: MSBuild fails before compilation with `MSB6001` / `System.ArgumentException: item already added ... key: 'tmp' ... key: 'TMP'` in `ToolTask.GetProcessStartInfo`.
   - Treat this as environment-variable collision, not a source compile error.
   - Retry the same build with lowercase `tmp` removed:
     - `env -u tmp MSYS2_ARG_CONV_EXCL='*' '<MSBuild.exe>' LAND.sln -m -t:Build '-p:Configuration=Debug;Platform=Win32' -v:minimal`

5. Push verification.
   - After commit, check `git status --short --branch` and `git rev-parse HEAD`.
   - If `git push origin master` fails because the UNC remote path is inaccessible or not recognized as a repository, report that push is blocked while local commit is complete and ahead by 1. Do not claim remote delivery.

## Reporting pattern

- Local commit SHA and message.
- Staged file list or diff stat.
- Build result before commit.
- `git diff --cached --check` result.
- Push success/failure and final branch state.
