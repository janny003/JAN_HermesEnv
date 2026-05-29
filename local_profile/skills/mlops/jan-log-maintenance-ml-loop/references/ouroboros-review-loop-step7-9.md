# Ouroboros Step7~9 Review Loop (Interview/QA/Evaluate + History Compare)

## Trigger
- 6단계 정비 보고서(DOCX/JSON) 생성 직후, 7~9단계를 자동으로 실행해 검토 품질을 올릴 때.

## Inputs
- current report JSON: `--current-report-json <.../JAN_maintenance_report_v11.json>`
- history directory(JSON reports): `--history-dir <dir>`
- output directory: `--out-dir <dir>`

## Command
```bash
python tools/ouroboros_review_loop.py \
  --current-report-json /c/Users/yjs/Desktop/JAN/OrobrosTest/out/JAN_maintenance_report_v11.json \
  --history-dir /c/Users/yjs/Desktop/JAN/Policy/Data \
  --out-dir /c/Users/yjs/Desktop/JAN/OrobrosTest/out/ouroboros_review
```

## Outputs
- `ouroboros_review_result.json`
- `ouroboros_review_result.md`

Both include:
1) Step7 Interview questions, QA checks, Evaluate verdict
2) Step8 historical comparison (high-risk trend, frequent causes)
3) Step9 prioritized feedback (missing evidence, extra checks, reordered top checks)

## Pitfalls fixed in-session
1. `generate_maintenance_report.py`에서 `fail_rows`를 payload 구성 전에 계산해야 함.
   - 증상: `UnboundLocalError: fail_rows`
   - 조치: `fail_rows = [r for r in rows if r["is_fail"]]`를 payload 생성 전에 배치.

2. review loop에서 `risk`가 숫자가 아니라 `HIGH/MEDIUM/LOW` 문자열로 올 수 있음.
   - 증상: `ValueError: could not convert string to float: 'HIGH'`
   - 조치: `_risk_to_float()` 매핑 사용 (`HIGH=1.0`, `MEDIUM=0.6`, `LOW=0.3`, else float fallback).

## Verification checklist
- `python -m py_compile tools/generate_maintenance_report.py tools/ouroboros_review_loop.py`
- 보고서 생성 실행 후 DOCX+JSON 경로 출력 확인
- review loop 실행 후 `out/ouroboros_review/*.json|*.md` 생성 확인
