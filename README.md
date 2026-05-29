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
