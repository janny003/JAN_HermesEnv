# Sub-agent policy roster update checklist (JAN)

Use this when the user asks to add or rename a JAN sub-agent persona/policy.

## Minimal reliable sequence
1. Create/update policy file under:
   - `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\policies\`
2. Keep canonical section structure:
   - Identity
   - Tone
   - Behavioral Policy
   - Working Style
   - Example Voice
3. Update README index:
   - `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\README.md`
   - Add the policy filename in `Sub-agent policy applied`.
4. Re-open both files and verify:
   - file exists
   - section headings present
   - README list includes the new policy exactly once

## Reporting pattern
- Confirm created file path
- Confirm README index updated
- Avoid claiming build/test validation for policy-only requests unless code actually changed
