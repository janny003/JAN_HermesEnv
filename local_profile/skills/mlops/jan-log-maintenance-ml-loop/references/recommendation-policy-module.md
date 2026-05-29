# Recommendation Policy 모듈 분리

## 언제 참고할 것
- JAN 정비 보고서의 `우선점검권고` 순서가 과거 해결 이력, Step7 Yes/No 인터뷰 답변, 사용자 우선점검 선호에 따라 바뀌어야 할 때
- `tools/generate_maintenance_report.py`가 분석/보고서/메모리/추천정책 책임을 너무 많이 갖고 있어 분리가 필요할 때
- Agent Orchestrator 전환 과정에서 결정론적 파이프라인 core와 추천 보정 계층을 구분해야 할 때

## 권장 구조
- `tools/recommendation_policy.py`를 추천 우선순위 보정 전용 모듈로 둔다.
- `generate_maintenance_report.py`는 raw 분석 결과를 만들고, 추천 보정은 `apply_recommendation_policy()` 같은 단일 진입점에 위임한다.
- 입력 리스트(`recommended_exclusion_items` 등)는 함수 내부에서 직접 변형하지 말고 복사본 기반으로 처리한다. 원본 변형은 테스트와 후속 리포트 비교에서 부작용을 만든다.

## 모듈 책임 예시
- `apply_resolved_priority()`
  - 시험 ID(Txx)별 해결 이력을 읽어, 과거에 실제 해결로 이어진 점검 항목을 앞쪽으로 재배치한다.
- `apply_interview_priority()`
  - Step7 Yes/No 인터뷰 답변, 특히 전원/케이블/통신 라인 확인 답변을 다음 진단의 추천 순서와 문구에 반영한다.
- `apply_preference_priority()`
  - 사용자의 명시적 우선점검 선호(`prefer_first_check`)를 추천 항목 앞쪽으로 이동한다.
- `build_interview_memory_note()`
  - 이전 인터뷰 답변을 보고서 종합의견/근거 문장에 반영할 짧은 메모 문장으로 만든다.
- `apply_recommendation_policy()`
  - 위 정책들을 순서대로 적용하는 단일 public entry point로 유지한다.

## 적용 순서
1. raw 분석/모델 추론 결과를 먼저 생성한다.
2. `inspection_memory.json` 또는 agent memory layer에서 해결 이력, 인터뷰 이력, 사용자 선호를 읽는다.
3. 추천 정책 모듈에 raw 추천 항목과 memory context를 전달한다.
4. 보정된 추천 항목과 memory note를 보고서 payload에 반영한다.
5. DOCX/JSON 보고서 양쪽에서 같은 추천 순서가 나오도록 확인한다.

## 테스트 기준
- 시험 ID별 해결 이력이 추천 순서를 바꾸는지 확인한다.
- Q3/전원·케이블·통신 라인 관련 Yes 답변이 우선순위와 문구에 반영되는지 확인한다.
- 사용자 선호 우선점검 항목이 기존 순서보다 앞에 배치되는지 확인한다.
- legacy memory 구조와 split memory/agent memory 구조를 모두 읽을 수 있게 한다.
- raw 입력 리스트가 함수 호출 후 변형되지 않는지 확인한다.
- `python -m pytest -q`로 전체 테스트를 실행하고, 사용자에게 성공/실패와 핵심 에러를 보고한다.

## 주의사항
- 추천정책은 모델 추론 자체가 아니라 후처리/정책 계층이다. 모델 score를 재계산하지 말고, 보고서의 점검 순서와 근거 문구를 안정적으로 보정하는 역할로 제한한다.
- Step7 인터뷰 답변은 일회성 UI 결과로 끝내지 말고 `last_interview`/`interview_history` 또는 4계층 memory layer에 저장해 다음 진단에서 재사용한다.
- 보고서 생성기 내부에 정책 함수를 다시 늘려 붙이면 Agent Orchestrator 전환 시 core 분리가 어려워진다. 새 정책이 생기면 추천정책 모듈에 추가하고 public entry point를 유지한다.
