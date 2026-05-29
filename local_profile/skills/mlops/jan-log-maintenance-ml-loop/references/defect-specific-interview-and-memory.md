# 고장·불량 항목 기반 Step7 인터뷰 + 다음 진단 반영 패턴

## 목적
Ouroboros Step7 질문이 추상적인 확인 질문으로 끝나지 않고, 현재 진단에서 실제로 고장/불량이 뜬 항목을 기준으로 현장 확인 여부와 다음 진단 반영 정보를 수집하도록 한다.

중요한 UX 원칙: 사용자가 소스코드나 설정 파일을 직접 확인하라는 질문으로 쓰지 않는다. 프로그램이 `fault_exclusion_master_map.csv`, 리포트 JSON, 리뷰 루프 근거를 읽어 판단한 뒤, 그 근거상 현장에서 확인해야 하는 주장비/고장배제 부위를 실제 확인했는지 묻는다.

## 질문 생성 원칙
- 항상 GUI Yes/No Dialog와 맞게 4개의 폐쇄형 질문으로 생성한다.
- 각 질문은 다음 근거를 포함한다.
  - `focus.file`: 불량/고장 의심 로그 파일명
  - `focus.test_ids`: 시험 ID
  - `focus.risk`: 위험도
  - `focus.recommended_exclusion_items`: 고장배제 목록
  - `step7.source_action_candidates`: 프로그램이 판단에 사용한 소스/설정 후보
- 질문 문장은 "조치할까요/수정할까요/소스코드를 확인할까요"보다 "실제로 확인했습니까/누락 없이 확인했습니까/정비 이력에 남기겠습니까"처럼 현장 확인 완료 여부를 묻는 형태를 우선한다.
- 질문 예시는 다음 구조가 좋다.
  1. `불량/고장 의심 항목 '<파일>'(시험ID <Txx>, 위험도 <risk>)의 고장배제 1순위 '<항목>'을 실제로 확인했습니까? (Yes/No)`
  2. `고장배제 목록 '<항목1 / 항목2 / 항목3>' 중 케이블/전원/연동 경로를 누락 없이 확인했습니까? (Yes/No)`
  3. `소스/설정 근거(<파일>)상 주장비 측 확인 필요 부위로 보이는 '<부위1 / 부위2>'를 주장비에서 확인했습니까? (Yes/No)`
  4. `원인분류 '<cause>'와 현장 확인 결과가 맞지 않을 경우, 주장비 측 추가 확인 부위와 동일 조건 재시험 필요성을 정비 이력에 남기겠습니까? (Yes/No)`

## 소스/설정 후보 선정
- 우선 후보:
  - `data/fault_exclusion_master_map.csv`
  - `tools/generate_maintenance_report.py`
  - `tools/ouroboros_review_loop.py`
  - `tools/run_maintenance_with_review.py`
- 추가 후보는 focus 파일명 토큰과 시험 ID(`Txx`)를 코드/CSV/문서에서 검색해 선정한다.
- 결과는 `step7.source_action_candidates[]`에 `file`, `reason`, `action`으로 저장한다.

## 답변 저장 및 다음 진단 반영
- GUI Yes/No 응답은 `ouroboros_review_result.json`의 `step7.interview_answers`에 저장한다.
- 동시에 `out/inspection_memory.json`에도 저장한다.
  - `last_interview`: 최신 1회 답변
  - `interview_history[]`: 누적 이력, 200건 cap 권장
- 다음 진단 보고서에서는 `last_interview.answers`를 읽어 `summary_text`에 `이전 인터뷰 답변 반영` 문구를 남긴다.
- 예: Q3(전원/케이블/통신 우선점검 유지)이 `예`이면 다음 권고 순서에 `전원/케이블/통신 라인`을 앞쪽에 반영한다.

## 검증 체크
- `python -m py_compile tools/ouroboros_review_loop.py tools/run_maintenance_with_review.py tools/generate_maintenance_report.py`
- review 실행 후 `step7.interview_questions`가 4개인지 확인한다.
- 모든 질문에 `(Yes/No)`가 포함되는지 확인한다.
- 질문 안에 고장/불량 항목, 고장배제 목록, 소스코드/설정 후보가 포함되는지 확인한다.
- 다음 보고서 JSON의 `focus.summary_text`에 `이전 인터뷰 답변 반영`이 포함되는지 확인한다.
