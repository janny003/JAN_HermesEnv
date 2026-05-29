# MRGA 튜닝 사이클 운영 규칙: baseline 고정 + 혼합신호군 분리 평가

## 배경
MRGA 튜닝에서 `agents.py`(진단 스코어링)와 `replay_compare_prepost.py`(질의 생성/신호라인 추출)를 함께 바꾸면, 절대 성능 수치가 변해도 **튜닝 효과(delta)** 가 0.0으로 반복 관측될 수 있다. 이때는 모델 성능이 정체된 것과 평가 입력이 동시에 이동한 것을 분리해야 한다.

## 운영 규칙
1. **비교 기준 커밋을 고정**한다.
   - pre/post 비교는 항상 `--before <직전-확정-기준>` vs `--after <현재>` 형태로 실행.
   - 기준점(benchmark baseline)을 바꿨으면 리포트에 반드시 명시한다.

2. `agents.py` 튜닝과 `replay_compare_prepost.py` 변경을 **동일 실험으로 해석하지 않는다**.
   - 질의빌더 변경은 평가 입력 분포를 바꾸므로, 별도 실험으로 분리 기록.

3. 성능 보고는 2축으로 고정한다.
   - 전체: `cause_top1_accuracy` (194건)
   - 타깃: `communication_path recall` (93건)

4. delta가 연속 0.0이면, 가중치 미세조정보다 **평가셋 분할**을 먼저 한다.
   - 권장 분할: communication GT를
     - (A) 통신 단일신호군
     - (B) 통신+전원/RF 혼합신호군
   - 튜닝은 (B)에 한정해 calibration 룰을 적용하고 부작용을 (A)에서 확인.

## 권장 실행 순서
1) 코드 변경
2) `pytest -q`
3) `python tools/replay_compare_prepost.py --before <baseline> --after <candidate> --out-dir out/eval`
4) `python tools/targeted_comm_misclass_eval.py --compare-csv out/eval/prepost_cause_compare.csv --out-dir out/eval`
5) commit/push
6) 리포트에 baseline SHA, total/target 지표, delta, 개선/회귀 건수 기록

## 보고서 최소 항목
- before/after commit SHA
- total accuracy before/after/delta
- communication recall before/after/delta
- improved/regressed case count
- 이번 변경이 `diagnosis scoring`인지 `query builder`인지 분류
