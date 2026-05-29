# MRGA Persistent Memory 스키마 강화 패턴 (v1.1)

## 목적
MRGA에서 단일 `records[]` 저장을 4계층 메모리 구조로 확장하면서, 기존 메모리 파일과의 호환성을 유지한다.

## 적용 상황
- `src/mrga/memory.py`가 단순 append만 수행할 때
- 과거 진단 맥락(episode)과 승인/보류 이력(verification)을 분리 저장해야 할 때
- 기존 JSON 파일(`{"records": [...]}`)을 파손 없이 이관해야 할 때

## 구현 핵심
1. `schema_version` 필드 도입 (`"1.1"`).
2. 4계층 루트 키를 고정:
   - `static_memory`
   - `dynamic_memory`
   - `episode_memory`
   - `verification_memory`
3. 레거시 자동 마이그레이션:
   - 입력에 `records`가 있으면 `episode_memory.history`로 이관.
4. 저장 API 분리:
   - `append_episode(record)`
   - `append_verification(record)`
5. 각 레코드에 `timestamp_utc` 자동 부여.

## Agent 연동 패턴
`MemoryAgent.run()`에서 최소 아래 두 레코드를 함께 기록한다.
- episode 레코드: `query, cause, risk, approved, feedback, actions, confidence, evidence_sources`
- verification 레코드: `query, approval_status, risk, confidence, feedback`

## 회귀 테스트 체크포인트
- 새 실행 후 메모리 파일에 `schema_version == "1.1"` 존재.
- `episode_memory.history` 및 `verification_memory.history` 둘 다 append됨.
- 레거시 `records` 파일 주입 시 자동 이관 + 신규 기록 공존 확인.
- 진단 회귀(예: `IFCC 통신 CRC fail -> communication_path`)가 깨지지 않는지 확인.

## 권장 커밋 단위
- memory 스키마 변경 + MemoryAgent 연동 + 테스트 보강을 한 커밋으로 묶는다.
- 푸시 전 `pytest -q`와 대표 질의 1건 스모크(`python -m mrga.main --query ...`)를 함께 검증한다.
