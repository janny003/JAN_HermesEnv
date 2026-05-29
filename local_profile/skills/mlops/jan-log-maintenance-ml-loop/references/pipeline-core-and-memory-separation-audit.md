# JAN 파이프라인 코어 구현 및 inspection_memory 분리 감사 메모

## 언제 참고할 것
- 사용자가 “파이프라인 코어가 실제로 구현되어 있는지” 확인해 달라고 할 때.
- `inspection_memory.json` 역할 분리, 메모리 계층 분리, Agent 전환 여부를 판단할 때.
- 코드 수정 없이 현재 구조 검토만 요청받은 경우에는 이 메모를 기준으로 파일 근거와 테스트 결과만 보고한다.

## 현재 파이프라인 코어 구현 판정
결론: 6개 파이프라인 코어 기능은 프로젝트 안에 모두 존재한다. 다만 하나의 순수 코어로 정돈되어 있지 않고 여러 파일에 분산되어 있으며, 실제 보고서 실행 경로인 `tools/generate_maintenance_report.py`에 파이프라인 기능과 메모리 기능이 섞여 있다.

### 1) 데이터 수집/정규화
- 구현 상태: 구현됨.
- 근거 파일:
  - `tools/inspection_pipeline.py`
  - `tools/generate_maintenance_report.py`
- 세부 근거:
  - `inspection_pipeline.py`는 CSV/TXT/SQLite 입력을 읽고 alias 기반 canonical key로 정규화한다.
  - `generate_maintenance_report.py`는 TXT 로그를 직접 읽고 `utf-8`, `cp949`, `euc-kr`, `latin-1` fallback을 적용한다.
- 주의:
  - MDB 원천 DB 중심의 단일 수집 코어로 완전히 통합된 상태는 아니다.

### 2) Feature 추출
- 구현 상태: 구현됨.
- 근거 파일:
  - `tools/inspection_pipeline.py`
  - `tools/generate_maintenance_report.py`
- 주요 feature:
  - `voltage`
  - `current`
  - `response_time_ms`
  - `fail_count`
  - `crc_error_rate`
  - `retry_count`
- 주의:
  - 정형 데이터 feature 추출과 TXT 로그 feature 추출 로직이 병렬/중복 구현되어 있다.

### 3) Isolation Forest / Robust Z-score 이상탐지
- 구현 상태: 구현됨.
- 근거 파일:
  - `tools/inspection_pipeline.py`
  - `tools/model_factory.py`
  - `tools/generate_maintenance_report.py`
- 세부 판정:
  - `inspection_pipeline.py`에는 Robust Z-score + IsolationForest fallback 구조가 있다.
  - `model_factory.py`는 Robust profile + IsolationForest 모델 생성/저장을 담당한다.
  - `generate_maintenance_report.py`는 저장된 `isolation_forest_anomaly_model.pkl`을 로드해 이상점수를 계산한다.
- 주의:
  - 보고서 실행 경로는 저장 모델 의존형이며, 그 파일 자체에 Robust Z-score fallback이 직접 들어간 구조는 아니다.

### 4) XGBoost / Rule fallback 원인분류
- 구현 상태: 부분 구현.
- 근거 파일:
  - `tools/model_factory.py`
  - `tools/maintenance_ml_pipeline.py`
  - `tools/generate_maintenance_report.py`
- 세부 판정:
  - `generate_maintenance_report.py`는 `xgboost_fault_cause_classifier.pkl`을 로드하고 `model.predict()`를 호출한다.
  - `model_factory.py`에는 LightGBM → CatBoost → XGBoost → RandomForest → rule fallback 계층이 있다.
  - `maintenance_ml_pipeline.py`는 실제 XGBoost 학습/추론이라기보다 xgboost 설치 여부를 확인하고 규칙 기반 bootstrap label을 붙이는 수준이다.
- 주의:
  - 실행 경로별로 실제 XGBoost, RandomForest fallback, rule fallback이 달라질 수 있으므로 보고서에는 실제 사용 모델 경로/알고리즘을 함께 표시해야 한다.

### 5) 위험도 계산
- 구현 상태: 구현됨.
- 근거 파일:
  - `tools/generate_maintenance_report.py`
  - `tools/maintenance_ml_pipeline.py`
- 세부 판정:
  - `generate_maintenance_report.py`는 anomaly score와 FAIL 여부를 기반으로 `LOW/MEDIUM/HIGH`를 계산한다.
  - `maintenance_ml_pipeline.py`는 anomaly_score 기반으로 h7/h30 위험도를 계산한다.
- 주의:
  - 현재는 LSTM-Transformer 장기예측이 아니라 현실적 baseline/휴리스틱 위험도 계산이다.

### 6) DOCX / JSON 보고서 생성
- 구현 상태: 구현됨.
- 근거 파일:
  - `tools/generate_maintenance_report.py`
- 세부 판정:
  - `python-docx`의 `Document()`로 Word 보고서를 생성한다.
  - `report_payload`를 JSON으로 저장한다.
- 주의:
  - `inspection_pipeline.py`는 Markdown/CSV 출력 중심이고, DOCX/JSON 통합 보고서 생성은 `generate_maintenance_report.py`가 담당한다.

## inspection_memory.json 역할 분리 판정
결론: 분리 필요성이 높다.

현재 `tools/generate_maintenance_report.py`에는 다음 책임이 같이 들어 있다.
- 로그 읽기
- feature 추출
- 모델 추론
- 위험도 계산
- DOCX/JSON 보고서 생성
- `inspection_memory.json` 읽기/쓰기
- operator feedback 파싱
- `resolved_priority` 갱신
- `last_interview` / `interview_history` 반영
- 과거 해결 이력/인터뷰 답변/사용자 선호 기반 우선점검권고 재정렬

## 구조상 리스크
- 같은 로그와 같은 모델을 입력해도 `inspection_memory.json` 상태가 다르면 `우선점검권고`와 종합의견 문장이 달라질 수 있다.
- 이는 정비 현장 개인화에는 유용하지만, 모델 추론 결과와 과거 기억 기반 보정 결과가 한 흐름에 섞이면 재현성/감사성이 약해진다.
- 분석 코어를 별도로 테스트하거나 교체하기 어렵다.
- `out/inspection_memory.json`은 단순 산출물이 아니라 상태 저장소 역할을 하므로 `out/` 산출물과 장기 메모리 저장소의 경계를 명확히 해야 한다.

## 권장 분리 구조
### pipeline_core
- 로그 수집
- 정규화
- feature 추출
- anomaly detection
- cause classification
- risk scoring
- 순수 report payload 생성

### memory_layer
- static/dynamic/episode/verification memory load/save
- feedback parsing
- resolved priority 관리
- interview history 관리
- final confirmation/audit 관리

### recommendation_policy
- pipeline 결과 + memory snapshot을 입력으로 받는다.
- 과거 해결 이력, 이전 인터뷰 답변, 사용자 선호를 반영해 점검 우선순위만 보정한다.
- 보정 전 원본 모델 판단과 보정 후 권고를 모두 남긴다.

### report_writer
- 최종 payload를 DOCX/JSON으로 직렬화한다.
- 보고서 형식과 인코딩만 담당한다.

## 검토-only 응답 시 권장 결론
- “파이프라인 코어 기능은 구현되어 있습니다.”
- “다만 코어와 메모리 계층이 `generate_maintenance_report.py` 안에서 섞여 있으므로, 다음 작업 1순위는 `inspection_memory.json` 역할 분리입니다.”
- “전체를 Agent 프로그램으로 바꾸기보다 기존 파이프라인 코어를 유지하고 `memory_layer`와 `recommendation_policy`를 분리하는 방향이 안전합니다.”

## GitHub 미러링 참고
JAN `OrobrosTest` 작업물을 별도 GitHub 저장소에도 올려야 할 때는 기존 `origin`을 바꾸지 말고 보조 remote를 추가해 push한다.

```bash
# 작업 경로: C:/Users/yjs/Desktop/JAN/OrobrosTest
if git remote get-url oroboros_agent >/dev/null 2>&1; then
  git remote set-url oroboros_agent https://github.com/janny003/Oroboros_Agent.git
else
  git remote add oroboros_agent https://github.com/janny003/Oroboros_Agent.git
fi

git push -u oroboros_agent main
```

이 패턴은 기존 `origin`(`JANNY`)을 보존하면서 `Oroboros_Agent`에도 동일 main을 반영할 때 사용한다.
