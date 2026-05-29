# 정비 리포트 JSON 동시 저장 계약

## 배경
- 기존 `tools/generate_maintenance_report.py`는 DOCX 저장 중심.
- 운영 자동화 연계를 위해 동일 리포트 내용을 JSON으로도 함께 저장하도록 확장됨.

## CLI 계약
- 필수: `--out-doc <path>`
- 선택: `--out-json <path>`
- `--out-json` 미지정 시 자동 규칙:
  - `<out-doc basename>.json` 생성
  - 예: `JAN_maintenance_report_v11.docx` -> `JAN_maintenance_report_v11.json`

## JSON 인코딩
- UTF-8
- `ensure_ascii=False`
- `indent=2`
- 목적: 한글 가독성 및 후처리 호환성 유지

## payload 핵심 필드(운영 관점)
- `generated_at`
- `log_root`
- `model_paths`
- `summary` (`total_logs`, `fail_candidates`, `high_risk_count`)
- `top_causes`
- `fail_candidates` (최대 80)
- `focus` (focus-log 입력 시)
- `memory_json`

## 최소 검증 절차
1. `python -m py_compile tools/generate_maintenance_report.py`
2. `python tools/generate_maintenance_report.py --help`에서 `--out-json` 옵션 확인
3. 샘플 실행 후 DOCX/JSON 동시 생성 확인
4. JSON 파일에서 한글 깨짐 여부 확인(UTF-8)

## 주의
- DOCX 기존 동작을 깨지 않도록 `--out-doc` 인터페이스는 유지한다.
- JSON 스키마를 변경할 때는 대시보드/후속 파서 영향도를 함께 점검한다.
