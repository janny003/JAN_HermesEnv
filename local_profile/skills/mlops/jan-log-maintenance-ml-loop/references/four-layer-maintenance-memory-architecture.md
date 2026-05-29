# JAN 4계층 지속 메모리 아키텍처 감사 메모

## 언제 참고할 것
- 사용자가 JAN 지속 메모리 구현 여부를 묻거나, 정적/동적/에피소드/검증 메모리 구조를 연구 문장과 대조해 달라고 할 때.
- 기존 파이프라인을 Agent 프로그램으로 전환할지, 파이프라인+Agent 하이브리드로 갈지 판단할 때.

## 현재 구현 판정 기준

### 1) 정적 메모리(static memory)
현재 부분 구현으로 본다.
- 근거 파일: `data/ate_egse_equipment_inventory.csv`
- 현재 포함: 장비명, 제조사, 모델, 분류, 비고
- 부족 항목: 시리얼 번호, 구성품 계층, 설치 환경, 제조사 권장 점검 기준, 장비별 허용오차/교정 주기
- 향후 권장: `static_memory.json` 또는 DB 테이블로 장비 마스터를 확장한다.

### 2) 동적 메모리(dynamic memory)
현재 분석 feature 중심의 부분 구현으로 본다.
- 근거 코드: `tools/generate_maintenance_report.py`, `tools/inspection_pipeline.py`
- 현재 포함: 전압, 전류, 응답시간, FAIL 수, CRC 오류율, retry 수, 이상점수, 위험도
- 부족 항목: 센서 로그 장기 누적 테이블, 경보 이력 전용 구조, 교정 상태, 부품 사용 시간, 운전 조건의 시간축 누적
- 향후 권장: `dynamic_memory.db`에 timestamp/device_id/test_id 기준으로 누적한다.

### 3) 에피소드 메모리(episode memory)
현재 가장 많이 구현된 계층으로 본다.
- 근거 파일: `out/inspection_memory.json`
- 현재 포함: `history[]`, `preferences`, `resolved_priority`, `last_interview`, `interview_history[]`
- 현재 저장되는 맥락: focus_log, cause, risk, feedback, prefer_first_check, resolved, resolved_item, similar_tests, Yes/No 인터뷰 답변
- 부족 항목: 증상/원인 후보/수행 조치/결과/재발 여부가 명확히 분리된 정규 스키마, placeholder 해결 항목 제거, 재발 여부 필드
- 향후 권장: `episode_memory` 스키마에 `symptom`, `cause_candidates`, `actions_taken`, `result`, `recurrence`를 명시한다.

### 4) 검증 메모리(verification memory)
현재 인터뷰/QA 일부만 구현된 상태로 본다.
- 근거 코드/파일: `tools/ouroboros_review_loop.py`, `out/ouroboros_review_*`, `out/inspection_memory.json`의 인터뷰 기록
- 현재 포함: Yes/No 질문, 운용자 답변, review score/verdict 일부
- 부족 항목: 전문가 승인 여부, 거절 사유, 안전 차단 기록, 감사 로그, 승인자, 승인 시각, 변경 전후 근거
- 향후 권장: `verification_memory` 스키마에 `approved_by`, `approval_status`, `reject_reason`, `safety_block`, `audit_log`, `final_confirmed`를 분리 저장한다.

## 구조 판단: Agent 전환 vs Pipeline 유지
권장 결론은 전체 Agent 전환이 아니라 `결정론적 파이프라인 core + Agent 보조 계층 + 분리된 memory layer`이다.

### Pipeline Core로 유지할 것
- 데이터 수집/정규화
- feature 추출
- Isolation Forest/Robust Z-score 이상탐지
- XGBoost/LightGBM/Rule fallback 원인분류
- 위험도 계산
- DOCX/JSON 보고서 생성

### Agent Layer로 둘 것
- 과거 유사사례 검색
- 현장 Yes/No 질문 생성
- 검증/승인 전 누락 항목 점검
- 이전 인터뷰/해결 이력 기반 점검 우선순위 재정렬
- 정적/동적/에피소드/검증 메모리 연결 설명

### 이유
- 모델 성능은 Agent화 자체가 아니라 데이터 품질, feature, 라벨, 검증 분할 개선으로 좋아진다.
- JAN 정비 흐름은 재현성, 감사 가능성, 안전성이 중요하므로 핵심 판단은 결정론적 파이프라인에 두는 편이 안전하다.
- Agent는 사람과의 상호작용, 맥락 유지, 질문/검토/우선순위 조정에서 효과가 크다.

## 사용자에게 답할 때의 표현
- “현재 4계층 지속 메모리가 완성 구현된 상태는 아니고, 에피소드 메모리와 일부 검증 메모리가 먼저 구현된 상태입니다.”
- “기존 파이프라인을 유지하고 Agent를 메모리 조회, 현장 인터뷰, 검증 피드백, 우선순위 재조정 계층으로 얹는 구조가 가장 적합합니다.”
- 코드 수정 없이 검토만 요청받은 경우, 파일을 변경하지 말고 근거 파일/코드와 테스트 결과만 명확히 보고한다.
