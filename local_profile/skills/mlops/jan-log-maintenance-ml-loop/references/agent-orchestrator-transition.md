# JAN Agent Orchestrator 전환 구현 메모

## 언제 참고할 것
- 사용자가 기존 JAN 파이프라인 큰틀은 유지하되 Agent 기반 구조로 전환하자고 할 때.
- `inspection_memory.json` 역할 분리, Agent Orchestrator, ReAct/Reflexion 기반 정비지원 구조를 구현할 때.
- 기존 `generate_maintenance_report.py`에 섞인 pipeline/report/memory/recommendation 책임을 분리할 때.

## 핵심 방향
기존 결정론적 파이프라인은 유지하고, 그 위에 Agent Orchestrator를 얹는다.

- Pipeline Core: 로그 수집, feature 추출, 이상탐지, 원인분류, 위험도 계산을 담당한다.
- Memory Layer: 정적/동적/에피소드/검증 메모리를 분리 저장한다.
- Recommendation Policy: pipeline 결과와 memory snapshot을 입력으로 받아 점검 우선순위를 보정한다.
- Agent Orchestrator: MemoryAgent → PipelineAgent → RecommendationAgent → VerificationAgent → ReportAgent 순서로 실행을 조율한다.
- Report Writer: DOCX/JSON 저장만 담당한다.

Agent는 모델 판단을 대체하지 않는다. 모델 결과는 pipeline core가 산출하고, Agent는 해석·검증·질문·우선순위 보정·장기 메모리 갱신을 담당한다.

## 구현 순서
1. `inspection_memory.json` 역할 분리
   - 신규: `tools/agent_memory.py`
   - 테스트: `tests/test_agent_memory.py`
   - legacy `history[]` → episode memory
   - legacy `preferences`, `resolved_priority` → preference memory
   - legacy `last_interview`, `interview_history[]` → verification memory
   - 한글 JSON은 `ensure_ascii=False`, UTF-8로 저장한다.

2. `recommendation_policy.py` 분리
   - `apply_resolved_priority`, `apply_interview_priority`, `prefer_first_check` 반영 로직을 별도 모듈로 이동한다.
   - raw analysis payload는 변경하지 않고 recommendation payload만 보정한다.

3. `pipeline_core.py` 순수화
   - 같은 입력/모델이면 memory 상태와 무관하게 같은 `analysis_payload`를 반환해야 한다.
   - memory write와 report write는 금지한다.

4. `agent_orchestrator.py` 추가
   - deterministic agent class부터 시작한다.
   - 기본 순서는 `MemoryAgent → PipelineAgent → RecommendationAgent → VerificationAgent → ReportAgent`로 둔다.
   - 각 Agent step은 `agent`, `mode`, `side_effect`, `status`, `input`, `output` dict를 명시한다. `details`만 두면 계약이 모호하므로 RED 테스트로 잡는다.
   - Orchestrator는 읽기/조율만 담당하고 DOCX/JSON 저장이나 memory write를 하지 않는다.
   - 실제 LLM 호출은 후순위로 둔다.
   - 상세 체크리스트는 `references/deterministic-agent-orchestrator.md`를 함께 확인한다.

5. GUI wrapper 호환 유지
   - `run_maintenance_with_review.py`의 `[INTERVIEW_Q1]`~`[INTERVIEW_Q4]` stdout 계약을 유지한다.
   - Yes/No 답변 저장과 한글 표시를 유지한다.
   - Step7 Yes/No 답변은 legacy `inspection_memory.json`뿐 아니라 split memory `out/memory/verification_memory.json`에도 저장한다. `append_verification_record()`를 사용해 `last_interview`와 `interview_history[]`를 함께 갱신한다.

6. `report_writer.py` 분리
   - DOCX/JSON 직렬화만 담당한다.
   - 판단 로직과 메모리 갱신 로직을 넣지 않는다.
   - 구현 패턴은 `write_maintenance_report(payload, out_doc, out_json, operator_feedback="")` 형태로 둔다.
   - `generate_maintenance_report.py`는 CLI, memory load/update/save, pipeline core 호출, writer 호출만 조율한다.
   - writer 회귀 테스트는 payload 비변경, JSON exact match, memory side effect 없음, DOCX 핵심 한글 섹션/표 헤더 유지, 금지 import/call 정적 검사를 포함한다.
   - TDD guard를 둔다: writer 단위 테스트는 payload를 mutate하지 않는지, JSON이 payload와 정확히 같은지, `memory_json` 경로가 있어도 writer가 memory 파일을 만들지 않는지 확인한다.
   - 정적 guard를 둔다: `report_writer.py`가 `build_maintenance_analysis_payload`, `apply_recommendation_policy`, `load/save_inspection_memory`, `update_memory_with_feedback`, `parse_feedback`, `pickle`, `numpy`를 import/call하지 않는지 검사한다.
   - CLI smoke 검증은 기존 산출물 삭제(`rm -rf out/...`)보다 매번 새 고유 출력 디렉터리/파일명을 사용해 비파괴적으로 수행한다. Hermes 안전 차단을 피하려고 같은 삭제 의도를 우회하지 말고, 처음부터 삭제 없는 smoke 경로를 설계한다.

## 현재 1차 구현 패턴
- `tools/agent_memory.py`는 `MemoryPaths`, `empty_memory_bundle`, `split_legacy_inspection_memory`, `migrate_legacy_inspection_memory`, `load_memory_bundle`, `save_memory_bundle`, `append_episode`, `append_verification_record` 형태로 시작한다.
- `tests/test_agent_memory.py`는 legacy memory 분리, UTF-8 한글 유지, episode/verification append를 검증한다.
- 검증 명령 예:
  - `python -m pytest tests/test_agent_memory.py tests/test_inspection_pipeline.py tests/test_model_factory.py -q`

## 피트폴
- Agent Orchestrator를 먼저 크게 만들지 말고 memory layer부터 분리한다. 그래야 Agent가 읽고 쓸 상태 경계가 안정된다.
- `generate_maintenance_report.py`는 현재 pipeline, report, memory, recommendation 책임이 혼재되어 있으므로 한 번에 갈아엎지 말고 compatibility wrapper를 유지하며 점진 분리한다.
- Memory 상태가 바뀌어도 raw model analysis는 같아야 한다. Memory는 recommendation/verification/report wording 단계에만 반영한다.
- GUI 계약(`[INTERVIEW_Q*]`, Yes/No 4문항, 한글 인코딩)은 Agent 전환 중에도 깨면 안 된다.
