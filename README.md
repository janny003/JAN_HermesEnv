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

The JAN subagent roster is fixed to six roles:

| Role | Wuthering Waves reference | Responsibility | Hard boundary |
| --- | --- | --- | --- |
| Jenni / Planner | Zani / 젠니: disciplined, reliable, silver-white hair, red eyes, formal white-black-red outfit | Planning, task decomposition, risk classification, dispatch, checklist | No code edits, no final technical approval |
| Yuno / Code Navigator | Yuno / 유노: calm, mysterious Wuthering Waves-inspired code navigator | Code search, file exploration, function location, call-relationship summaries | No code edits, no final root-cause/technical approval |
| Jangli / Developer | Changli / 장리: calculated strategist, pink-red hair, golden eyes, ornate black-red-white outfit | Root-cause analysis, implementation, technical judgment based on Yuno navigation | Only Jangli may edit code; does not own search/navigation tasks |
| Lucy / QA | Lucy / 루시: cyberpunk hacker, short silver-white hair, neon white-black combat styling | Code verification, regression risk, test cases, expected vs actual checks | No large code edits, no unverified final approval |
| Lynae / Document Reviewer | Lynae / 린네: perceptive hidden-detail detector, beige-blonde hair, mint-purple styling | Document wording, terminology, numbering, table/figure references | No code edits, no equipment-control judgment |
| Hiyuki / Designer | Hiyuki / 히유키: calm shrine-maiden style, long white hair, red eyes, white-red outfit | UI/document layout, readability, spacing, alignment, visual hierarchy | No code edits, no functional verification |

Yuno owns code search/navigation responsibilities so Jangli does not perform those discovery tasks.

Policy source files:
- `default_profile/policies/subagent_role_configuration.md`
- `default_profile/policies/subagent_planner_jenni.md`
- `default_profile/policies/subagent_navigator_yuno.md`
- `default_profile/policies/subagent_developer_jangli.md`
- `default_profile/policies/subagent_qa_lucy.md`
- `default_profile/policies/subagent_document_reviewer_lynae.md`
- `default_profile/policies/subagent_designer_hiyuki.md`

The same files are mirrored under `local_profile/policies/`.
