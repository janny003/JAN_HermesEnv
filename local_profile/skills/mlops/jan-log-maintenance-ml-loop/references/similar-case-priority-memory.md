# 유사사례 기반 점검우선순위 학습 패턴 (OrobrosTest)

## 목적
focus 로그를 읽을 때 과거 유사 로그를 함께 제시하고, 운용자가 `해결:`로 확정한 조치항목을 누적해 다음 권고 순서를 자동 재정렬한다.

## 입력 규약
- `--focus-log <path>`: 현재 분석 대상 로그
- `--operator-feedback "우선점검: ...; 해결: ..."`
  - 우선점검 파싱 키: `우선점검|먼저점검|first`
  - 해결 파싱 키: `해결|resolved|조치완료`

## 저장소
- 파일: `out/inspection_memory.json`
- 주요 키:
  - `preferences.prefer_first_check`: 사용자 일반 선호 1순위
  - `resolved_priority.<Txx>.<항목>`: 시험ID별 해결 누적 카운트
  - `history[]`: 시점/focus_log/cause/risk/feedback/resolved_item/similar_tests

## 추천 알고리즘
1. 각 로그에서 `features` 벡터와 `test_ids`를 확보한다.
2. focus 로그와 과거 로그 cosine similarity를 계산한다.
3. 시험ID가 겹치면 가중치(+0.08)를 더해 유사사례 상위 K(기본 5)를 선택한다.
4. 권고항목 생성 후 `resolved_priority`를 먼저 적용해 재정렬한다.
5. 그 다음 `prefer_first_check`를 적용해 최종 1순위를 보정한다.
6. 보고서 종합의견에 `유사 이력:`과 `지속 메모리 반영` 근거를 함께 남긴다.

## 구현 포인트
- `build_exclusion_recommendation(...) -> (items, checklist, test_ids)`로 test_ids를 함께 반환.
- 파일명 접두 숫자(`6. RICA...`)를 T06으로 보정하는 fallback을 둔다.
- 해결 누적은 해당 시험ID가 없으면 `GLOBAL` 버킷에 기록.

## 운영 팁
- 입력 예시: `우선점검: 모체반; 해결: 모체반 전원라인 재체결`
- `history`는 200건 cap으로 유지해 파일 비대화 방지.
- 한글 보고서/CSV는 UTF-8-sig 또는 UTF-8 저장으로 깨짐을 예방.
