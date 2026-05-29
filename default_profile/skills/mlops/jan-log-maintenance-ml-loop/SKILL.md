---
name: jan-log-maintenance-ml-loop
description: JAN LOG 누적 기반 정비효율 향상 파이프라인 (Isolation Forest 이상탐지 + XGBoost 원인분류 + LSTM-Transformer 장기고장예측)
---

# 목적
C:\Users\yjs\Desktop\JAN\LOG 데이터를 지속 누적하여,
1) 이상 탐지,
2) 원인 분류,
3) 장기 고장 예측
을 순차적으로 고도화하고 정비 효율을 높인다.

# 트리거
- 사용자가 JAN 로그 분석/고장예측/정비효율 향상을 요청할 때
- 신규 LOG 파일이 추가되었을 때
- 모델 재학습 또는 성능 점검이 필요할 때

# 기본 원칙
1. 먼저 데이터 스키마를 고정한다.
2. 단기 운영은 Robust Z-score + IsolationForest(이상탐지), LightGBM(원인분류/30·60·90일 예측) 조합을 우선한다.
3. CatBoost/XGBoost/RandomForest/Rule-based fallback을 항상 남겨 패키지 의존성 없이도 산출물을 만든다.
4. 시계열 길이가 충분할 때 Survival/Deep 모델로 확장한다.
5. 학습/검증 분할 시 시간 누수와 장비 누수를 방지한다.
6. 결과는 정비 관점 리포트(근거/원인/권장조치)로 출력한다.
7. 사용자 응답은 `subagent 이름 : 대답내용` 형식을 유지한다.

# 데이터 경로
- 원천 로그: C:\Users\yjs\Desktop\JAN\LOG
- 프로젝트(복제본1): C:\Users\yjs\Desktop\JAN\OrobrosTest
- 프로젝트(복제본2): C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest
- MFC 자동 저장 CSV: C:\Users\yjs\Desktop\JAN\Policy\Data\latest_features.csv

# MFC(Hermes) 연동 운영 규칙
1. Start 버튼은 목적별로 child process를 실행한다: (a) Hermes CSV 추출 모드 또는 (b) Python 리포트 생성 모드.
2. Python 실행은 `python` 상대명이 아닌 **절대 경로 python.exe + quote된 인자**를 사용한다(CreateProcessW PATH 의존 방지).
3. Hermes CSV 추출 모드에서는 출력 계약을 명시한다:
   - `CSV_START` 다음 줄부터 CSV 본문
   - 마지막 줄 `CSV_END`
4. CSV 후처리는 `CSV_START/CSV_END`가 실제 존재할 때만 실행한다(리포트 모드에서는 CSV 파싱 생략).
5. 리포트 모드 기본 커맨드는 `python` 상대명이 아니라 **절대 경로 python.exe + quote 인자**를 사용한다. (GUI CreateProcessW의 PATH 의존 제거)
6. 프로세스 종료코드는 `WaitForSingleObject` 후 읽고, `259(STILL_ACTIVE)`는 미확정 상태로 간주한다.
7. 동일 변경은 OrobrosTest / Policy\OrobrosTest 양쪽에 동기 반영한다.
8. 소스 변경 후에는 반드시 Rebuild해서 최신 exe가 새 command를 반영했는지 transcript의 `[START]` 라인으로 재확인한다.
9. 종합의견 개인화: `--operator-feedback`(예: `우선점검: 모체반`)를 입력받아 보고서 문구와 점검 순서에 반영한다.
10. 지속 점검 메모리: `out/inspection_memory.json`에 이전 점검 선호(`prefer_first_check`)를 저장하고 다음 실행의 `우선점검권고` 순서 재배치에 사용한다.
11. 한글 UI 안정화: 리소스(.rc)는 ASCII 라벨(`Load Log`)로 두고, 런타임 `SetDlgItemTextW(..., L"로그 읽기")`로 한글을 설정해 인코딩 깨짐을 회피한다.
12. GUI 레이아웃 수정 후 빌드 검증 시, 버튼 폭/간격(특히 Start/로그읽기/Stop)과 한글 표시를 실제 exe에서 확인한다.
13. `focus-log`를 읽으면 이전 로그와의 유사사례를 먼저 계산해 종합의견에 `유사 이력:`으로 표기한다(최소 상위 3건).
14. 운용자가 `해결:`(또는 resolved/조치완료)로 종료한 점검 항목은 시험 ID(Txx)별 해결 우선순위로 누적한다.
15. 다음 실행의 `우선점검권고`는 (a) 시험ID별 해결 누적 우선순위, (b) 사용자 우선점검 선호(`prefer_first_check`)를 순서대로 반영한다.

# 권장 단계
## 1) 수집/정규화
- 우선순위: 프로그램 DB 원천(TEST_LOG + 상세 테이블) > TXT/XLS/XML 내보내기 파일.
- TXT/XLS 등 다양한 로그에서 공통 컬럼 추출:
  - timestamp, device_id, module, test_item, metric_name, metric_value, unit, pass_fail, note
- pass/fail, 주파수/전압/전류/응답시간/CRC/재시도 관련 값은 수치화
- 파일명 메타데이터(장비종류/신품·기존/시험명/날짜) 파싱
- 코드베이스 추적이 필요한 경우 `references/ateswr-log-lineage.md`를 먼저 확인한다.
- MFC 연동 상세(C++ 패치 포인트/CSV 후처리)는 `references/mfc-hermes-csv-postprocess.md`를 확인한다.
- MFC Start 정비보고서 모드(Word 출력/exit code 처리/본문수치피처 추출)는 `references/mfc-start-maintenance-report.md`를 확인한다.
- SRU 후보 라벨링/소스 규칙 추출/multi-label 분류는 `references/sru-rule-extraction-and-multilabel.md`를 확인한다.
- SRU 실학습 성능판정 기준(micro/macro/FAIL recall)은 `references/sru-training-metrics-criteria.md`를 확인한다.
- 단기 모델팩토리 구현/테스트 포인트는 `references/short-term-model-factory-implementation.md`를 확인한다.
- MFC Start 버튼으로 정비 Word 보고서(전체 로그+기존 모델 추론) 자동생성은 `references/mfc-start-maintenance-report.md`를 확인한다.
- 보고서 해석 규칙(FAIL 후보 선정 이유/원인 라벨 매핑/고위험 비어있을 때 해석)은 `references/report-interpretation-and-label-mapping.md`를 확인한다.
- 유사사례 기반 점검우선순위 학습(`해결:` 피드백 누적, 시험ID별 우선항목 재배치)은 `references/similar-case-priority-memory.md`를 확인한다.

## 2) 단기 이상탐지: Robust Z-score + Isolation Forest
- 입력: 정규화된 수치 피처 + 조건 피처
- 1차 게이트: Robust Z-score 임계치
- 2차 판정: Isolation Forest score
- 출력:
  - anomaly_score
  - anomaly_label(normal/anomaly/watch)
  - high_risk_features(근거)
- 운영 기준:
  - contamination은 초기 보수적으로 설정 후 실제 정비 피드백으로 보정

## 3) 단기 원인분류: LightGBM 우선
- 대상: anomaly_label in {anomaly, watch} 또는 fail 케이스
- 피처: 기준값 마진(상/하한 대비 편차), 파일명 토큰, FAIL 라벨 파생 피처
- 라벨 사전 예시:
  - 전원/통신/주파수/센서/케이블/포트/부팅/기타
- 출력:
  - cause_top1
  - cause_prob
  - feature_importance(or SHAP)
- 구현 우선순위:
  - 1순위 LightGBM
  - 2순위 CatBoost (범주형 비중이 높은 경우)
  - 3순위 XGBoost

## 4) 단기 고장 예측: LightGBM 30/60/90일
- 단위: device_id 또는 장치군 집계
- horizon: 30/60/90일 FAIL 확률
- 출력:
  - failure_risk_h30
  - failure_risk_h60
  - failure_risk_h90
  - early_warning_flag
- 전제:
  - timestamp 품질 확보
  - horizon 라벨 생성 로직(미래 윈도우 내 FAIL 유무) 고정

## 4-1) 중장기 확장 로드맵
- 누적 이력/정비일/고장일 정합성 확보 후:
  - Random Survival Forest
  - Cox Time-Varying
  - DeepSurv

## 5) 정비 리포트 자동화
- 필수 섹션:
  - 이상 판단 근거
  - 추정 원인 및 확률
  - 유사 정비 사례
  - 추천 점검 순서
- 결과를 누적 저장하여 다음 학습 데이터에 반영

# 검증 체크리스트
- [ ] 동일 장비/동일 시점 데이터가 train/test에 동시에 섞이지 않았는가
- [ ] 클래스 불균형 대응(가중치/샘플링)을 적용했는가
- [ ] 최신 로그 추가 후 성능 변동을 추적하는가
- [ ] 리포트의 원인 근거가 수치적으로 설명 가능한가

# 피트폴/주의사항
- TXT/XLS는 운영 DB의 내보내기 산출물일 수 있으므로, 가능하면 DB 원천 데이터로 라벨/피처를 구성한다.
- 파일명/메모 텍스트 기반 라벨링 시 노이즈가 크므로 라벨 품질 검수 필요
- 시계열 예측은 데이터가 적으면 과적합 위험이 큼
- 모델 성능보다 정비현장 해석 가능성을 우선한다

# 실행 전략(반복 루프)
1. 신규 로그 수집
2. 정규화/적재
3. IF 추론
4. XGBoost 추론
5. 리포트 생성
6. 정비 결과 피드백 반영
7. 주기적 재학습

# 완료 기준
- 신규 로그 투입 시 자동으로 이상/원인/장기위험 리포트가 생성되고,
- 정비 피드백 누적으로 모델 정확도와 조치 리드타임이 개선된다.
