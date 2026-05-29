# 단기 기준 모델팩토리 구현 메모 (JAN OrobrosTest)

## 적용 목표
- 단기 운영안 우선 구현:
  - 이상탐지: Robust Z-score + Isolation Forest
  - 원인분류: LightGBM 우선 (CatBoost/XGBoost/RandomForest/rule-based fallback)
  - 단기예측: LightGBM 30/60/90일 (없으면 rule-based fallback)

## 반영 파일
- C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\tools\model_factory.py
- C:\Users\yjs\Desktop\JAN\OrobrosTest\tools\model_factory.py
- C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\tests\test_model_factory.py
- C:\Users\yjs\Desktop\JAN\OrobrosTest\tests\test_model_factory.py

## 아티팩트 이름
- isolation_forest_anomaly_model.pkl
- lightgbm_fault_cause_classifier.pkl
- lightgbm_short_term_failure_predictor.pkl
- model_manifest.json

## 구현 포인트
1) 환경에 따라 ML 패키지가 없어도 아티팩트 생성이 실패하지 않게 fallback 체인 유지
2) manifest에 requested/actual_algorithm과 fallback_reason을 남겨 운영 투명성 확보
3) fixture 기반 단위테스트 2개를 양쪽 프로젝트에서 동일 통과 상태 유지

## 검증 커맨드
- python -m pytest -q tests/test_model_factory.py
- python tools/model_factory.py --input tests/fixtures/sample_test_log.csv --output-dir out/model_factory_short_term_check

## 주의
- 프로젝트 두 경로(Policy/OrobrosTest, OrobrosTest) 동시 반영 필요
- 의존 패키지 유무는 바뀔 수 있으므로 'fallback 가능 구조'를 고정하고 특정 패키지 부재를 영구 규칙으로 저장하지 않는다.
