# Report interpretation and label mapping (JAN MFC maintenance report)

## Trigger
Use when the Word report is generated from MFC Start flow and users ask:
- why HIGH-risk table is empty
- why cause labels are numeric/unknown
- why row counts look doubled
- why FAIL candidates need explicit rationale text

## Durable rules
1. De-duplicate log file discovery:
   - If scanning both `*.TXT` and `*.txt`, merge with `set(...)` before iteration.
   - Without dedup, counts can inflate (e.g., 194 -> 388).

2. Unwrap pickled model payloads:
   - Some models are stored as dict wrappers: `{model, feature_names, classes}`.
   - Always use `payload['model']` when present.
   - For classifiers, map predicted integer indices to `classes` for human-readable labels.

3. Keep feature schema aligned with trained model feature_names:
   - For model_factory artifacts, expected order is:
     `voltage, current, response_time_ms, fail_count, crc_error_rate, retry_count`
   - Mismatched feature width/order causes invalid scoring and misleading report sections.

4. FAIL-candidate section should include rationale text per row:
   - Example reasons: `파일명에 FAIL 포함`, `이상탐지 점수<0`, `실패/에러 키워드 N회`, `retry 키워드 N회`.
   - This is required for operational explainability in maintenance review.

5. Empty HIGH-risk table is valid if threshold not met:
   - Current heuristic may yield LOW/MEDIUM only.
   - Report should not imply failure; explain that no rows crossed HIGH threshold.

## Pitfalls
- Word save can fail with PermissionError if target .docx is open in Word.
  - Close the document and rerun generation.

## Verification checklist
- Cause labels appear as domain words, not raw integers.
- Total row count equals unique log-file count.
- FAIL candidate rows show explicit reasons.
- If HIGH table is empty, summary still reports risk distribution clearly.