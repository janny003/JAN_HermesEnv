# JAN_HermesEnv policy sync checklist

When a new JAN subagent policy file is created/updated in local policy workspace, and the user asks to publish it to environment repo:

1. Target repo
- `https://github.com/janny003/JAN_HermesEnv.git`
- Branch: `main`

2. Copy targets (both required)
- `default_profile/policies/subagent_<role>_<name>.md`
- `local_profile/policies/subagent_<role>_<name>.md`

3. Skill reference sync
- Update both files:
  - `default_profile/skills/software-development/subagent-driven-development/SKILL.md`
  - `local_profile/skills/software-development/subagent-driven-development/SKILL.md`
- Add the new `C:/Users/yjs/Desktop/JAN/Policy/subagent_<role>_<name>.md` line under JAN policy-file convention.

4. Verification gates
- `git status --short` shows only intended files.
- Commit message clearly indicates policy sync scope.
- `git push origin main` success output captured.

5. Reporting template
- repo URL
- branch
- commit hash
- changed file list (absolute local paths + repo relative paths)
