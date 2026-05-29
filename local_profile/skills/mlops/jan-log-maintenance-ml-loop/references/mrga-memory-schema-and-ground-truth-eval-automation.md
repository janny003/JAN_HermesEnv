# MRGA 메모리 스키마 강화 + Ground Truth 자동평가 파이프라인

## 언제 사용
- MRGA 기반 진단에서 지속 메모리 구조를 단순 로그 누적에서 운영 가능한 계층형 구조로 올릴 때
- Agent Only 실행 결과(`runs/agent_only/*.json`)를 `ground_truth.csv`와 자동 비교해 재현 가능한 지표를 만들 때

## 핵심 구현 패턴

### 1) Persistent Memory 스키마 버전 관리
- 파일: `src/mrga/memory.py`
- 권장:
  - `schema_version` 필드 명시 (예: `1.1`)
  - 아래 4계층 구조를 기본 골격으로 유지
    - `static_memory`
    - `dynamic_memory`
    - `episode_memory`
    - `verification_memory`
- 레거시 마이그레이션:
  - 기존 `{ "records": [...] }`가 존재하면 `episode_memory.history`로 자동 이관
  - load 시 마이그레이션 후 즉시 파일 재저장(정규화)

### 2) 기록 API 분리
- `append_episode(record)`
- `append_verification(record)`
- 각 record에 `timestamp_utc` 자동 주입

### 3) MemoryAgent 반영 규칙
- 파일: `src/mrga/agents.py`
- episode에는 최소 다음 필드 저장
  - `query`, `cause`, `risk`, `approved`, `feedback`, `actions`, `confidence`, `evidence_sources`
- verification에는 최소 다음 필드 저장
  - `query`, `approval_status`, `risk`, `confidence`, `feedback`

### 4) Ground Truth 자동평가 스크립트
- 파일: `tools/evaluate_agent_only_with_ground_truth.py`
- 입력
  - `ground_truth.csv`
  - `runs/agent_only/*.json` (focus.file 기준 매칭)
- 중복 실행 결과 처리
  - 동일 `focus.file`가 여러 건이면 `generated_at` 최신 건 채택
- 계산 지표
  - `coverage`
  - `status_accuracy`
  - `cause_top1_accuracy`
  - `action_top1_contains_accuracy`
  - `cause_confusion`
- 출력
  - `out/eval/agent_only_eval_vs_ground_truth.csv`
  - `out/eval/agent_only_eval_vs_ground_truth_summary.json`
  - `out/eval/agent_only_eval_vs_ground_truth.md`

## 테스트 포인트
- 파일: `tests/test_workflow.py`, `tests/test_eval_script.py`
- 필수 회귀
  1. 레거시 `records` 마이그레이션 후 `schema_version` 확인
  2. episode/verification 기록 존재 확인
  3. 평가 스크립트에서 100% 일치 샘플 입력 시 모든 정확도 1.0 확인

## 운영상 주의
- `ground_truth.csv`는 `utf-8-sig`로 읽어 BOM 혼선을 피한다.
- action 평가는 완전일치보다 `contains` 기반을 병행해야 현장 문구 변형에 덜 취약하다.
- status 정확도가 높아도 cause/action 정확도가 낮을 수 있으므로, 혼동행렬(`cause_confusion`)을 우선 개선 루프의 입력으로 사용한다.
