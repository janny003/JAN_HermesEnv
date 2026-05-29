# MRGA communication-path 튜닝 후 delta=0 지속 시 운영 플레이북

## 상황
- `agents.py`에서 communication intent 토큰 확장/가중치 보정을 해도 pre/post accuracy delta가 0으로 유지될 수 있다.
- 특히 `ground_truth=communication_path` 케이스에서 `power_path`로 쏠리는 혼선이 반복된다.

## 이번 세션에서 검증된 사실
1. fail-coupled communication boost(예: crc/packet/timeout + fail) 추가 후에도 전체 pre/post delta는 0.0일 수 있다.
2. 타깃 리콜도 delta 0.0일 수 있다.
3. 이 경우 원인은 모델 scoring보다 **입력 query 구성(signal line 추출/노이즈 비율)**일 가능성이 높다.

## 재현/검증 절차(권장 순서)
1. `pytest -q`로 회귀 먼저 확인.
2. `tools/replay_compare_prepost.py --before <sha> --after <sha> --out-dir out/eval` 실행.
3. `tools/targeted_comm_misclass_eval.py --compare-csv out/eval/prepost_cause_compare.csv --out-dir out/eval` 실행.
4. `communication_path` 오분류 분포(power/rf) 확인 후, query builder에서 fail 라인 우선 추출 비중을 점검.

## 튜닝 우선순위 가이드
1. 점수 가중치 미세조정보다 query builder 정제 우선
   - 정상 루틴(전원/주파수 PASS boilerplate) 라인 비중 축소
   - FAIL/오류 라인, CRC/packet/timeout line 가중 우선
2. 힌트 누설 금지 유지
   - replay query 생성 시 GT 힌트 사용 금지
3. 변경 단위 축소
   - 한 번에 하나의 calibration만 바꾸고 pre/post 비교 고정

## 보고 포맷(권장)
- before/after commit
- total accuracy, delta
- target(comm) recall, delta
- improved/regressed case 수
- 다음 액션: scoring vs query-builder 중 어디를 건드릴지 명시
