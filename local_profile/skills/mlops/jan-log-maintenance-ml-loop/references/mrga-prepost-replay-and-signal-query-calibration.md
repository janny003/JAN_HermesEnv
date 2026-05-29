# MRGA 전/후 재생 비교 + 신호라인 기반 query 보강 운영 노트

## 목적
- 원인 매핑 보정 커밋의 효과를 `ground_truth.csv` 기준으로 전/후 비교할 때, 단순 텍스트 앞부분 질의가 아니라 **운영형 신호 추출 query**를 사용해 민감도를 높인다.

## 적용 위치
- 저장소: `C:\Users\yjs\Desktop\JAN\RAGMaintenanceArchitecture`
- 스크립트:
  - `tools/replay_compare_prepost.py` (전/후 commit replay 비교)
  - `tools/evaluate_agent_only_with_ground_truth.py` (ground truth 자동 채점)

## 핵심 패턴
1) 신호라인 추출 기반 query 생성
- FAIL/불량/고장/CRC/통신/전원/RF/retry/Txx 라인을 우선 추출
- 중복 라인 제거 후 요약
- query 템플릿에 아래를 명시:
  - `focus_log`
  - `symptom_lines`
  - `hint_cause`
  - `keywords`
  - `task=원인 경로 추정`

2) 전/후 비교 실행
- 예시:
  - `python tools/replay_compare_prepost.py --before <old_sha> --after <new_sha> --out-dir out/eval`
- 산출물:
  - `out/eval/prepost_cause_compare.csv`
  - `out/eval/prepost_cause_compare_summary.json`
  - `out/eval/prepost_cause_compare.md`

3) 결과 해석 규칙
- delta=0이어도 실패로 단정하지 않는다.
- 먼저 확인:
  - 입력 query 품질(신호라인 추출 정상 여부)
  - 혼선 상위쌍(예: communication->power/rf) 비중
  - PASS/정상 케이스의 오탐 비율

## 실무 피트폴
- replay 스크립트가 `git checkout <sha>`를 수행하므로, **작업트리가 dirty이면 실패**할 수 있다.
- 운영 순서:
  1. 변경사항 커밋 또는 stash
  2. replay 실행
  3. 원래 브랜치 복귀 확인

## 이번 세션에서 확인된 사실(재사용 포인트)
- 신호라인 기반 query로 재생 평가 절대 정확도는 개선 가능(예: 27.32% -> 33.51%)
- 그러나 특정 규칙 보정 커밋의 전/후 delta는 0일 수 있으므로, 다음 단계는 상위 혼선 subset 타깃 실험이 효율적이다.
