# JAN_HermesEnv

Hermes agent environment snapshot for reuse on other machines.

## Included
- default_profile/config.yaml (from C:\Users\yjs\.hermes)
- default_profile/skills/
- default_profile/cron/
- default_profile/.env.template (values redacted)
- local_profile/config.yaml (from C:\Users\yjs\AppData\Local\hermes)
- local_profile/skills/
- local_profile/cron/
- local_profile/plugins/ (if present)
- local_profile/.env.template (values redacted)

## Not included (security)
- Real `.env` secrets
- `auth.json` OAuth/token cache
- session/log/cache databases

## Restore on another machine
1) Install Hermes Agent
2) Copy `default_profile/config.yaml` to `~/.hermes/config.yaml`
3) Copy `default_profile/skills/` to `~/.hermes/skills/`
4) Copy `default_profile/cron/` to `~/.hermes/cron/`
5) Open `.env.template`, create `~/.hermes/.env`, fill real keys
6) Run:
   - `hermes config check`
   - `hermes tools list`
   - `hermes doctor`

For Windows local layout variant, use files under `local_profile/` similarly.

## JAN fixed subagent roles

The JAN subagent roster is fixed to five roles only:

| Role | Responsibility | Hard boundary |
| --- | --- | --- |
| Jenni / Planner | Planning, task decomposition, risk classification, dispatch, checklist | No code edits, no final technical approval |
| Jangli / Developer | Code analysis and code modification | Only Jangli may edit code |
| Lucy / QA | Code verification, regression risk, test cases, expected vs actual checks | No large code edits, no unverified final approval |
| Lynae / Document Reviewer | Document wording, terminology, numbering, table/figure references | No code edits, no equipment-control judgment |
| Hiyuki / Designer | UI/document layout, readability, spacing, alignment, visual hierarchy | No code edits, no functional verification |

Yuno is not part of the JAN subagent roster.

Policy source files:
- `default_profile/policies/subagent_role_configuration.md`
- `default_profile/policies/subagent_planner_jenni.md`
- `default_profile/policies/subagent_developer_jangli.md`
- `default_profile/policies/subagent_qa_lucy.md`
- `default_profile/policies/subagent_document_reviewer_lynae.md`
- `default_profile/policies/subagent_designer_hiyuki.md`

The same files are mirrored under `local_profile/policies/`.
