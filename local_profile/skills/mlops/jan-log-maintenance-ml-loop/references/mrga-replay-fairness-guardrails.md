# MRGA Replay Fairness Guardrails

## Why this exists
Pre/post 성능 비교에서 query builder가 ground-truth 힌트(`gt_hint`)를 입력으로 사용하면 평가 누수(data leakage)가 발생한다. 지표가 좋아 보여도 실제 운영 성능 개선으로 해석할 수 없다.

## Guardrails (must)
1. `replay_compare_prepost.py`의 질의 생성 함수는 `log_name`, `text` 같은 관측 신호만 입력으로 받는다.
2. `gt_hint`, 정답 라벨, 평가용 메타데이터는 질의 생성 경로에 절대 전달하지 않는다.
3. 튜닝 후 비교는 항상 `--before <commit> --after <commit>`으로 동일 로그셋 재추론으로 수행한다.
4. 공정성 관련 스크립트 수정이 있으면 재실행 결과와 함께 즉시 commit/push 한다.

## Quick verification checklist
- [ ] query builder 시그니처에 GT 관련 인자가 없는가
- [ ] before/after 정확도 delta가 재현 가능한가
- [ ] pytest 회귀 테스트가 모두 통과하는가
- [ ] out/eval 요약(json/md/csv) 산출물이 갱신되었는가

## Reporting convention
- 지표가 개선되지 않아도, "누수 제거로 평가 신뢰도 상승"을 분리해서 명시한다.
- 개선 수치와 신뢰도 개선을 혼합해 표현하지 않는다.
