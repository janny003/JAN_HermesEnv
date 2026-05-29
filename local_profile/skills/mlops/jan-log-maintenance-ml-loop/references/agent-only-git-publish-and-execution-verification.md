# Agent Only Git publish and execution verification

Use this note when publishing or validating the JAN `AGENT_Only` comparison implementation.

## Scope
- Local workspace: `C:\Users\yjs\Desktop\JAN\AGENT_Only`
- Remote repository: `https://github.com/janny003/AGENT_Only.git`
- Expected branch: `main`
- GUI executable after Debug x64 build: `x64\Debug\OrobrosTest.exe`

## Recommended sequence
1. Verify the repo state before committing:
   - `git status --short --branch`
   - `git remote -v`
   - `git ls-remote --heads origin`
2. Run the focused regression tests before push:
   - `python -m pytest tests/test_agent_only_runner.py tests/test_gui_agent_status_static.py -q`
3. Inspect staged files and exclude obvious scratch artifacts before commit.
   - Example: one-off files such as `test.txt` with dummy content should not be committed.
4. Commit with a class-level message such as:
   - `feat: add JAN agent-only workflow`
5. Push and verify local/remote SHA equality:
   - `git push -u origin main`
   - `git ls-remote --heads origin main`
   - `git rev-parse HEAD`
6. Launch the GUI executable, then poll the tracked process when the user closes it.
   - A clean user close should report `exit_code: 0` from the tracked background process.
7. Continue with CLI smoke validation to confirm the workflow remains functional after GUI execution.

## CLI smoke validation pattern
Use deterministic input for the 4 Yes/No questions and final confirmation:

```bash
printf 'y\ny\ny\ny\napproved\n' | python tools/agent_only_runner.py \
  --project-root . \
  --log-root ../LOG \
  --out-doc out/JAN_agent_only_continue.docx \
  --out-json out/JAN_agent_only_continue.json \
  --operator-feedback 'GUI 실행 후 연속 검증'
```

Expected checkpoints:
- `[AGENT]` lines show all 5 Agent Only roles.
- `[INTERVIEW_Q1]` through `[INTERVIEW_Q4]` are emitted as separate Yes/No questions.
- `[FINAL_CONFIRM_A] approved` is accepted.
- DOCX and JSON output files are created.
- JSON includes `mode: agent_only`, 5 agents, summary counts, Korean questions/answers, and `approval_status: approved`.
- DOCX and JSON should both contain valid Korean text; verify this explicitly because the user is sensitive to Korean encoding issues.

## Git cleanliness after generated outputs
Generated output directories are intentionally ignored by `.gitignore` (`out/`, build folders, caches). After smoke validation, `git status --short --branch` should remain clean relative to `origin/main`.

## Reporting style
When briefing the user, include:
- repository URL, branch, commit SHA if a push occurred;
- focused test result;
- GUI process exit status if applicable;
- generated DOCX/JSON paths;
- Korean text verification result;
- Git cleanliness result.
