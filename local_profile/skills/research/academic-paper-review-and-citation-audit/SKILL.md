---
name: academic-paper-review-and-citation-audit
description: Two-pass academic manuscript review with citation-grounding checks (PDF/DOCX), consistency audit, and submission-readiness fixes.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Academic Paper Review and Citation Audit

## When to use
- User asks to review a manuscript draft (DOCX/PDF) for quality and readiness.
- User asks whether in-text citations are truly grounded in referenced sources.
- User asks for "꼼꼼히" review, final submission checks, or consistency checks across abstract/body/tables/conclusion.

## Core workflow (MANDATORY two-pass)
1) Pass 1 — Content/logic review
- Check thesis clarity, contribution statement, scope boundaries, and claim strength.
- Verify section flow (problem -> method -> result -> interpretation -> limitation -> conclusion).
- Flag overclaims (e.g., automation claims not supported by evidence).

2) Pass 2 — Grounding/integrity review
- Cross-check all key metrics across Abstract, tables, body text, and conclusion.
- Verify citation grounding: each high-impact claim must map to a cited source that actually supports it.
- Detect citation anomalies: bibliography-only refs, in-text-only refs, mismatched numbering, weak policy-vs-paper support.
- Check figure/table/equation references and numbering consistency.

Do not skip Pass 2. If user requests careful review, explicitly report both pass outcomes.
For users requesting double-check behavior, always output a compact "1차 검토 결과 / 2차 검증 결과" split.

## File handling guidance
- DOCX: prefer python-docx parsing for structure-aware checks.
- PDF: extract text and run structural and citation consistency checks.
- If a `.docx` is encrypted/wrapped and unreadable (e.g., header starts with `DS420210` / ShadowCube-protected container), treat it as non-DOCX and switch workflow: request "Word에서 다른 이름으로 저장(.docx)" or review the exported PDF.
- When reviewing from PDF extraction, run a quick reference-encoding sanity check (diacritics like `Küttler`, `Rocktäschel`) because author names can degrade in extracted text and must be corrected in final bibliography.

## Output format
- Start with overall verdict: "submission-ready" vs "needs fixes".
- Then provide prioritized issues:
  - High (must-fix before submission)
  - Medium (quality improvement)
  - Low (polish)
- For each issue: location, observed problem, why it matters, exact fix suggestion.

## Citation audit checklist
- [ ] Every cited index [n] appears in bibliography.
- [ ] Every bibliography item is cited in text at least once (or justify background-only references).
- [ ] Core method claims cite method papers, not only policy docs.
- [ ] Policy/governance claims (risk, approval, controls) cite standards/framework docs.
- [ ] New references added in body are renumbered consistently.

## Common pitfalls
- Mixing two evaluation protocols in one table without explicit separation.
- Metric drift (runtime/accuracy mismatch across sections).
- Referencing a paper in bibliography but never citing it in body.
- Relying on web guidance docs for technical method claims better supported by peer-reviewed sources.

## Session support files
- references/jan-paper-review-doublecheck.md: Practical two-pass checklist and insertion templates used in JAN-style maintenance AI manuscripts.
- references/citation-grounding-matrix-template.md: Reusable matrix for bibliography-only detection, claim-to-source typing, and metric consistency checks.
