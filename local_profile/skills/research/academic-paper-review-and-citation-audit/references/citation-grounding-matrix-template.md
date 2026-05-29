# Citation Grounding Matrix Template

Use this matrix in Pass 2 to prove citation integrity quickly.

| Ref | Cited in body? | Claim type | Source type | Grounding verdict | Action |
|---|---|---|---|---|---|
| [n] | Yes/No | method / result / governance | paper / standard / gov-guide | strong / weak / missing | keep / add body citation / replace / downgrade claim |

## Practical rules
1. Bibliography-only reference => add at least one in-text citation or remove from bibliography.
2. High-impact method/result claim should be backed by paper-grade evidence first.
3. Governance/safety claims can cite standards/framework docs, but avoid using policy docs as sole support for technical performance claims.
4. When two protocols are mixed (e.g., status vs cause/action), require explicit separation sentence and per-table condition labels.
5. Verify metrics are identical across Abstract, table, results paragraph, and conclusion summary.

## Encrypted DOCX fallback
If `.docx` cannot be parsed and begins with non-OOXML signature (e.g., `DS420210`), treat as protected container:
- Ask for re-save as standard Word `.docx`, or
- Continue review from exported PDF with an encoding sanity pass on bibliography names.
