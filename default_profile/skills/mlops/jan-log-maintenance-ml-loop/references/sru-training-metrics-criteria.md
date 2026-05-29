# SRU multi-label 실학습 성능판정 기준 (단기 운영)

## 왜 '좋다'를 나눠서 봐야 하나
- 상대 비교: 같은 데이터/분할에서 모델 A vs B 중 누가 높은지
- 운영 적합: FAIL 후보를 놓치지 않는지(재현율 중심)

## 1차 채택 기준 (현재 프로젝트)
1. micro F1: 전체 샘플 기준 분류 품질
2. macro F1: 희소 SRU 라벨까지 포함한 균형 품질
3. FAIL 후보(candidate=1)에서 라벨별 Recall

권장 판정:
- 모델 교체는 기존 대비 micro/macro F1 모두 개선일 때 우선 채택
- micro만 높고 macro가 낮으면 희소 라벨 붕괴 여부를 추가 검토

## 이번 세션 관찰값 (Policy 경로 기준)
- LightGBM: micro F1 0.6739, macro F1 0.3303
- CatBoost: micro F1 0.7865, macro F1 0.3656
- 해석: 현재 데이터에서는 CatBoost가 상대 우세

## 출력 산출물 점검
- sru_multilabel_report.json: micro/macro/라벨별 지표
- sru_multilabel_predictions.csv: candidate=1 필터 후 오탐/미탐 확인

## 실무 주의
- 파일명 기반 라벨은 노이즈가 커서 절대 수치 과신 금지
- 운영 반영 전 최신 로그 홀드아웃(시간축 분할)로 재평가 필요
- 보고는 사용자 선호 포맷 `subagent 이름 : 대답내용`으로 유지