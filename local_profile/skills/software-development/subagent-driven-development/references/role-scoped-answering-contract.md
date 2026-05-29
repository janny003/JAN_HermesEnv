# Role-scoped answering contract (JAN multi-subagent)

When users operate with fixed named subagents, treat role scope as an execution constraint, not a style preference.

## Trigger phrases
- "답변할때 자기 역할에 관한것만 대답"
- "각자 자기 역할에 관한것만 답변"
- "role별로 자기 일만 말해"

## Required behavior
1. Keep output format exactly as requested (commonly `subagent 이름 : 대답내용`).
2. Constrain each line to the role domain only.
3. Split cross-cutting points by owner role instead of combining in one line.
4. If role ownership is unclear, state assumption briefly and keep scope narrow.

## Domain boundaries (default)
- Developer (Jangli): implementation, architecture, dependencies, build/test commands, risk in code paths.
- Planner (Jenni): sequencing, milestones, dependencies, decision trade-offs, next-step roadmap.
- Designer (Hiyuki): layout, hierarchy, typography, spacing, color, UX clarity.
- QA (Lucy): reproduction steps, expected vs actual, regression matrix, verification status.

## Anti-patterns
- Developer line includes QA pass/fail verdicts.
- QA line prescribes visual redesign details.
- Designer line prescribes code-level refactor steps.
- Planner line reports unverified build success as fact.

## Good pattern
- Provide one concise line per role with that role’s owned content.
- For shared topics, provide parallel role-specific lines rather than mixed narration.
