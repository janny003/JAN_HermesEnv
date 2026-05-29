# MRGA 보정 전/후 재생 평가 패턴 (ground_truth 기준)

## 언제 사용
- 원인 매핑/스코어링 로직을 수정했는데, 기존 벤치마크 요약 수치가 변하지 않을 때.
- "코드는 바뀌었는데 지표는 그대로" 상황에서 원인이 집계 데이터 stale인지 확인할 때.

## 핵심 원인
- `comparison_eval/runs/agent_only/*.json` 같은 기존 실행 산출물은 과거 모델/코드 결과다.
- 로직 변경 후에도 이 파일들을 그대로 평가하면 수치가 바뀌지 않을 수 있다.

## 권장 절차
1. 기준 라벨: `comparison_eval/ground_truth.csv` 고정.
2. before/after 커밋을 명시한다.
3. 각 커밋에서 동일 입력 규칙으로 194개 로그를 재추론한다.
4. `cause_top1_accuracy` 전/후, 개선/회귀 건수를 같이 비교한다.
5. 비교 산출물은 csv/json/md 3종으로 남긴다.

## 구현 예시 (이번 세션)
- 스크립트: `tools/replay_compare_prepost.py`
- 입력:
  - `--before 2e05bde`
  - `--after cc32798`
  - `--ground-truth C:/Users/yjs/Desktop/JAN/comparison_eval/ground_truth.csv`
- 출력:
  - `out/eval/prepost_cause_compare.csv`
  - `out/eval/prepost_cause_compare_summary.json`
  - `out/eval/prepost_cause_compare.md`

## 해석 가이드
- delta=0.0이면 먼저 "보정 무효"로 단정하지 말고 입력 쿼리 생성 규칙을 점검한다.
- 특히 운영 질의와 재생 질의의 정보량 차이(FAIL 라인/테스트ID/현장 문맥 누락)가 크면 분리 효과가 약해질 수 있다.
- 다음 단계는 query builder를 운영 입력에 가깝게 보강하는 것이다.
