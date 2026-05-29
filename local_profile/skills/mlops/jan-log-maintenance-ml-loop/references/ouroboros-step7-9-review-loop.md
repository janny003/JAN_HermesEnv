# Ouroboros Step7~9 Review Loop Contract (JAN)

목적: 6단계 정비보고서(JSON)를 입력으로 받아 7~9단계를 자동 산출한다.

입력
- current_report_json: `generate_maintenance_report.py`가 만든 JSON
- history_dir: 과거 보고서 JSON 디렉터리

출력
- `ouroboros_review_result.json`
- `ouroboros_review_result.md`

Step7
- Interview 질문 자동 생성
- QA 체크: summary/fail_candidates/top_causes/focus 포함 여부
- Evaluate: pass 비율 기반 verdict(`ready|needs_review|insufficient`)

Step8
- 과거 비교는 `*.json`만 읽되, 보고서 스키마(`summary`) 없는 파일은 제외 권장
- 비교 지표: `history_count`, `avg_high_risk_count`, `current_high_risk_count`, `high_risk_trend`

Step9
- 우선순위 재정렬: fail_candidates를 위험도 기준으로 정렬 후 top3 제시
- 위험도 정렬 시 문자열 리스크 매핑 필수
  - `HIGH=1.0`, `MEDIUM=0.6`, `LOW=0.3`
  - 숫자/문자 혼재 데이터에서 `float()` 직변환 금지 (예외 발생)
- 피드백 타입: `priority_reorder`, `risk_trend`, `evidence`, `coverage`, `root_cause`

검증 포인트
- focus-log 지정 실행 후 QA의 `focus 분석 포함 여부`가 pass인지 확인
- 리뷰 결과 score/verdict가 기대치와 일치하는지 확인
