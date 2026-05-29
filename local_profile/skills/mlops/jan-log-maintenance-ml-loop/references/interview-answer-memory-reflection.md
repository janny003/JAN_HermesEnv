# Step7 인터뷰 답변 지속 저장 및 다음 진단 반영

## 목적
GUI의 Ouroboros Step7 Yes/No 인터뷰(Q1~Q4) 답변을 단순 리뷰 결과 파일에만 남기지 않고, 다음 진단의 점검 권고와 종합의견에 재사용한다.

## 저장 흐름
1. `tools/run_maintenance_with_review.py`가 `ouroboros_review_result.json`의 `step7.interview_answers`를 저장한다.
2. 같은 실행 흐름에서 보고서 JSON의 `memory_json` 경로를 읽는다.
3. 해당 지속 메모리 파일(`out/inspection_memory.json`)에 아래 키를 갱신한다.
   - `last_interview`: 가장 최근 Q1~Q4 질문/답변, focus 로그, test_ids
   - `interview_history[]`: 인터뷰 이력 누적, 200건 cap 권장

## 다음 진단 반영 흐름
1. `tools/generate_maintenance_report.py`가 `out/inspection_memory.json`을 로드한다.
2. `last_interview.answers`를 읽어 보고서 JSON의 `focus.interview_memory_note`와 종합의견에 반영한다.
3. Q3(전원/케이블/통신 라인 우선점검 유지)이 `예`이면 다음 진단의 `recommended_exclusion_items`에 `전원/케이블/통신 라인`을 앞쪽에 반영한다.
4. 보고서 종합의견에는 `이전 인터뷰 답변 반영` 문구를 남겨 왜 권고 순서가 바뀌었는지 확인 가능하게 한다.

## 검증 패턴
- 실제 운영 메모리를 직접 오염시키지 않으려면 임시 메모리 파일을 만들어 `--memory-json <temp>`로 실행한다.
- 1차 실행: 보고서 생성 및 리뷰 질문 생성.
- `_persist_interview_answers(report_json, review_json, ['예','아니요','예','아니요'])` 또는 GUI 답변으로 메모리 저장 확인.
- 2차 실행: 같은 focus-log로 보고서를 다시 생성해 아래를 확인한다.
  - `inspection_memory.json.last_interview.answers` 존재
  - `inspection_memory.json.interview_history` 증가
  - `focus.interview_memory_note`에 답변 요약 존재
  - `focus.interview_priority_note` 또는 `summary_text`에 `이전 인터뷰 답변 반영` 존재
  - Q3=`예`인 경우 `recommended_exclusion_items`에 `전원/케이블/통신 라인` 반영

## 주의사항
- `ouroboros_review_result.json`에만 `interview_answers`가 있으면 다음 진단에는 충분히 반영되지 않는다. 반드시 `inspection_memory.json`까지 지속 저장해야 한다.
- 보고서 생성은 Step7 질문보다 먼저 실행되므로, 방금 받은 인터뷰 답변은 현재 보고서가 아니라 “다음 진단”에 반영된다.
- 한글 JSON은 `ensure_ascii=False`, UTF-8 저장을 유지한다.
