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
8. JAN 정책 기반 4개 에이전트(젠니/장리/루시/히유키) 역할과 톤을 분리해 응답한다.
9. 사용자 호칭은 `유노`를 사용한다.
10. 사용자 응답 형식은 `에이전트이름: 내용`을 기본으로 유지한다(브리핑/중간보고/최종보고 동일).

# 데이터 경로
- 원천 DB(데이터 수집 기준): C:\Users\yjs\Desktop\JAN\ATESWR-25KA4\UAV_ATE\Data\ATE.mdb
- TXT 로그 참고 경로(보조/비교용): C:\Users\yjs\Desktop\JAN\LOG
- 프로젝트(복제본1): C:\Users\yjs\Desktop\JAN\OrobrosTest
- 프로젝트(복제본2): C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest
- MFC 자동 저장 CSV: C:\Users\yjs\Desktop\JAN\Policy\Data\latest_features.csv

# MFC(Hermes) 연동 운영 규칙
1. Start 버튼은 목적별로 child process를 실행한다: (a) Hermes CSV 추출 모드 또는 (b) Python 리포트 생성 모드.
2. Python 실행은 `python` 상대명이 아닌 **절대 경로 python.exe + quote된 인자**를 사용한다(CreateProcessW PATH 의존 방지).
2-1. GUI command 입력칸은 사용자가 이전 디버그 토큰(예: `z`)을 남길 수 있으므로, 기본 wrapper command를 `DefaultMaintenanceCommand()` 같은 단일 helper로 보관하고 로그 선택/Start 전에 wrapper 토큰(`run_maintenance_with_review.py`)을 검증한다. 토큰이 없으면 기본 command로 자동 복구한 뒤 `--focus-log`를 붙인다. `[START] z --focus-log ...` + `GetLastError=2`는 분석 파이프라인 문제가 아니라 stale command 실행 문제이며, 복구 후 transcript의 `[START]` 줄이 quoted `python.exe` + wrapper 경로로 시작하는지 확인한다.
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
15. 다음 실행의 `우선점검권고`는 (a) 시험ID별 해결 누적 우선순위, (b) Step7 Yes/No 인터뷰 답변, (c) 사용자 우선점검 선호(`prefer_first_check`)를 순서대로 반영한다. 이 보정은 `tools/recommendation_policy.py` 같은 전용 정책 모듈에 두고, `generate_maintenance_report.py`에는 raw 분석/보고서 생성 책임만 남기는 방향을 우선한다.
16. `tools/generate_maintenance_report.py`는 DOCX와 함께 JSON 보고서도 저장한다. `--out-json` 미지정 시 `--out-doc`와 동일 basename의 `.json`을 자동 생성해 후속 파이프라인(대시보드/자동검증) 입력으로 재사용한다.
17. Step7~9 자동검토는 `tools/ouroboros_review_loop.py`로 실행하고, 입력은 6단계 보고서 JSON을 사용한다.
18. Step8 비교용 `history-dir`에는 보고서 JSON 위주로 누적한다(운영 메모리 JSON 혼입 시 통계 왜곡 가능).
19. MFC에서 Step7 질문이 "안 보이는" 이슈를 막기 위해, 리뷰 실행기는 질문을 stdout에 `[INTERVIEW_Q1..]` 형태로 반드시 출력한다(파일 저장만으로 끝내지 않음).
20. GUI 질문 팝업 트리거는 command 문자열에 `ouroboros`만 의존하지 말고, 실제 래퍼 스크립트명(예: `run_maintenance_with_review.py`, Agent Only의 `agent_only_runner.py`)도 허용한다. `[INTERVIEW_Q1]` 뒤 완료 메시지가 없으면 runner 실패로 단정하지 말고, 먼저 GUI 팝업 게이트가 해당 runner 토큰을 허용하는지와 child가 stdin 입력 대기 중인지 확인한다.
21. MFC 기본 Start 커맨드는 리포트+리뷰 래퍼(`tools/run_maintenance_with_review.py`)를 사용해 6단계 이후 7~9단계가 자동으로 연속 실행되게 유지한다.
22. `generate_maintenance_report.py`와 `ouroboros_review_loop.py` 사이 브리지에서 `[REVIEW] score/verdict`를 stdout으로 함께 노출해 UI transcript에서 검토 성공 여부를 즉시 확인 가능하게 한다.
23. Step7 인터뷰 질문은 일반적인 재시험/확정 질문으로 두지 말고, 현재 고장·불량 의심 항목(`focus.file`, `test_ids`, `risk`) + 고장배제 목록(`recommended_exclusion_items`) + 프로그램이 판단에 사용한 소스/설정 근거(`source_action_candidates`)를 포함한 Yes/No 현장 확인 질문 4개로 생성한다. 단, 사용자가 소스코드를 직접 확인하라는 질문처럼 쓰지 말고, 소스/설정 근거상 주장비·전원·케이블·통신 라인 등 어떤 현장 부위를 확인해야 하는지와 실제 확인 여부를 묻는다.
24. GUI Yes/No 답변은 `ouroboros_review_result.json`뿐 아니라 `out/inspection_memory.json`의 `last_interview`와 `interview_history`에도 저장해 다음 진단에서 우선점검 문구/순서에 반영한다.
23. Step7 Yes/No 인터뷰 답변은 `ouroboros_review_result.json`에만 남기지 말고 `out/inspection_memory.json`의 `last_interview`와 `interview_history[]`에도 저장한다. 다음 진단은 이 값을 읽어 `focus.interview_memory_note`, 종합의견, 필요 시 `recommended_exclusion_items` 우선순위에 반영해야 한다.

# 사용자 확정 개발 진행 프로세스
JAN 진단/정비 자동화는 아래 12단계 흐름을 기본 개발·운영 프로세스로 따른다.

1. ATE/EGSE 시험 로그 수집
2. 로그 Feature 추출 및 수집 데이터 가공(전처리)
3. Isolation Forest 기반 이상 탐지
4. XGBoost 기반 원인 분석
5. 현재 진단/운영 규칙을 SKILL.md에 저장하여 다음 작업에 재사용
6. 정비 보고서 초안 작성
7. Ouroboros가 진단 내용을 Interview/QA/Evaluate 방식으로 검토
8. 과거 정비 이력, 시험 로그, 보고서와 비교
9. 빠진 점, 근거 부족, 추가 점검 항목, 우선순위 재정렬 피드백
10. 사용자가 최종 진단 확정
11. 최종 결과를 지속 메모리/정비 이력으로 저장
12. 다음 진단 때 다시 참고

# 권장 단계
## 1) 수집/정규화
- 우선순위: 프로그램 DB 원천(TEST_LOG + 상세 테이블) > TXT/XLS/XML 내보내기 파일.
- ATE Access MDB 원천 예시: `C:\Users\yjs\Desktop\JAN\ATESWR-25KA4\UAV_ATE\Data\ATE.mdb`는 64-bit `Microsoft Access Driver (*.mdb, *.accdb)` + `pyodbc`로 읽을 수 있다. 주요 테이블은 `TEST_LOG`(시험 헤더), `EQUIP_TD`(시험 상세/측정값), `EQUIP`(장비명), `FAULT`(고장/부품 후보)이다.
- ATE/EGSE 장비 마스터 목록은 `C:\Users\yjs\Desktop\JAN\OrobrosTest\data\ate_egse_equipment_inventory.csv`를 기준으로 사용한다. 현재 27개 장비가 `equipment_name,maker,model,category,note` 스키마로 정리되어 있다.
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
- 리포트 DOCX+JSON 동시 저장 계약(옵션/인코딩/검증)은 `references/report-json-output-contract.md`를 확인한다.
- Ouroboros 7~9단계 자동검토(Interview/QA/Evaluate + 과거 JSON 비교 + 우선순위 피드백)는 `references/ouroboros-review-loop-step7-9.md`를 확인한다.
- 리포트 DOCX+JSON 동시 저장 계약(옵션/인코딩/검증)은 `references/report-json-output-contract.md`를 확인한다.
- Ouroboros 7~9단계 자동검토 루프(Interview/QA/Evaluate + 과거비교 + 우선순위 피드백)는 `references/ouroboros-step7-9-review-loop.md`를 확인한다.
- MFC↔Ouroboros 검토질문 가시화/연동 체크리스트는 `references/mfc-ouroboros-review-visibility.md`를 확인한다.
- 고장·불량 항목 기반 Step7 질문 생성과 Yes/No 답변의 다음 진단 반영은 `references/defect-specific-interview-and-memory.md`를 확인한다.
- 유사사례 기반 점검우선순위 학습(`해결:` 피드백 누적, 시험ID별 우선항목 재배치)은 `references/similar-case-priority-memory.md`를 확인한다.
- Step7 Yes/No 인터뷰 답변 지속 저장 및 다음 진단 반영(`last_interview`, `interview_history`, Q3 우선순위 반영)은 `references/interview-answer-memory-reflection.md`를 확인한다.
- 12단계 개발 프로세스 대비 현재 구현 누락/부분구현을 감사할 때는 `references/implementation-gap-audit-12-step-process.md`를 확인한다. 특히 원인분류 normal 편향, XGBoost/LightGBM artifact 경로 불일치, history-dir에 `inspection_memory.json`이 섞이는 문제, Step10~11 최종확정/이력화 미통합 여부를 우선 점검한다.
- 정적/동적/에피소드/검증 메모리 4계층 구조 구현 여부를 감사하거나, Agent 전환 vs 기존 파이프라인 유지 방향을 판단할 때는 `references/four-layer-maintenance-memory-architecture.md`를 확인한다. 현재 기준 권장 결론은 전체 Agent 전환이 아니라 **결정론적 파이프라인 core + Agent 보조 계층 + 분리된 memory layer**이다.
- 파이프라인 코어 6단계(수집/정규화, feature 추출, 이상탐지, 원인분류, 위험도 계산, DOCX/JSON 보고서 생성) 구현 여부와 `inspection_memory.json` 역할 분리 필요성을 검토할 때는 `references/pipeline-core-and-memory-separation-audit.md`를 확인한다. 현재 기준 판정은 “기능은 구현되어 있으나 `generate_maintenance_report.py`에 core/report/memory/recommendation 책임이 혼재되어 있어 `memory_layer`와 `recommendation_policy` 분리가 우선”이다.
- 기존 파이프라인 큰틀을 유지하면서 Agent Orchestrator 기반으로 전환할 때는 `references/agent-orchestrator-transition.md`를 확인한다. 구현 순서는 `agent_memory.py`로 4계층 메모리 분리 → `recommendation_policy.py` 분리 → `pipeline_core.py` 순수화 → `agent_orchestrator.py` 추가 → GUI wrapper 호환 유지 → `report_writer.py` 분리 순서가 안전하다.
- deterministic `agent_orchestrator.py`를 구현/검토할 때는 `references/deterministic-agent-orchestrator.md`를 확인한다. 각 agent step은 `agent/mode/side_effect/status/input/output` 계약을 명시하고, 초기 Orchestrator는 DOCX/JSON 저장이나 memory write 없이 읽기/조율만 수행한다.
- `generate_maintenance_report.py`에서 순수 분석 payload 생성을 `tools/pipeline_core.py`로 분리하거나 회귀 검증할 때는 `references/pipeline-core-extraction-pattern.md`를 확인한다. 핵심 원칙은 core는 dict payload만 반환하고, DOCX/JSON 저장 및 `inspection_memory.json` 갱신은 CLI wrapper에 남기는 것이다.
- 추천 우선순위 보정(해결 이력 + Step7 Yes/No 인터뷰 답변 + 사용자 우선점검 선호)을 보고서 생성기에서 분리하거나 테스트할 때는 `references/recommendation-policy-module.md`를 확인한다.
- Agent Only 비교 구현/감사 시에는 `references/agent-only-comparison-implementation.md`를 확인한다. 핵심은 기존 MFC GUI shell 유지, 기본 command의 `agent_only_runner.py` 연결, 5개 Agent 단계 명시, DOCX+JSON 산출물, 단위 테스트 + MFC Debug x64 빌드/실행 검증까지 함께 완료하는 것이다.
- Agent Only 저장소를 Pipeline Only에서 복사·분기한 뒤 QA할 때는 `references/agent-only-qa-regression-after-repo-copy.md`를 확인한다. 전체 pytest에서 남아 있는 Pipeline Only 전용 GUI command 기대값을 잡아내고, Agent Only 기본 command/출력명 기준으로 테스트를 정렬한 뒤 runner smoke와 한글 DOCX/JSON 검증까지 수행한다.
- Agent Only 구현물을 GitHub에 게시하거나 GUI 실행 후 연속 검증할 때는 `references/agent-only-git-publish-and-execution-verification.md`를 확인한다. 푸시 전 focused pytest, scratch 파일 제외, remote SHA 검증, GUI 종료 exit code 확인, CLI smoke 재검증, DOCX/JSON 한글 검증을 한 묶음으로 보고한다.
- Agent Only GUI에서 `[INTERVIEW_Q1]` 이후 Yes/No 팝업이나 `[DONE]`이 나오지 않는 문제를 디버깅할 때는 `references/agent-only-gui-interview-dialog-gating.md`를 확인한다. 핵심은 `MaybeShowQuestionDialog()`의 command gate가 `agent_only_runner.py`를 허용해야 하며, 미허용 시 child process가 Q1 stdin 입력 대기 상태로 멈춘다는 점이다.
- Pipeline Only / Hybrid / Agent Only 3-way 성능시험은 `C:\Users\yjs\Desktop\JAN\comparison_eval\run_three_way_benchmark.py` 형태의 별도 benchmark harness로 전체 `LOG`를 동일 focus-log 기준 반복 실행하고, `benchmark_results.csv`, `benchmark_summary.csv/json`, `JAN_three_way_performance_report.docx`로 정리한다.
- 성능 지표 확장 시에는 `comparison_eval`의 결과 CSV를 재실행 없이 재사용해 `ground_truth.csv`를 생성하고(로그 원문+파일명 규칙 기반), 상태/원인/조치 Top-1·Top-3 지표를 별도 summary(`benchmark_summary_with_ground_truth.csv/json`)로 계산한다. 이때 규칙 기반 ground truth는 "임시 일관비교용"으로 표기하고, 현장 확정 라벨이 들어오면 동일 스키마로 즉시 재평가한다.
- JAN TRD 벡터DB가 이미 있는 경우(`C:\Users\yjs\Desktop\JAN\01. TRD 문서_이전 사업\vector_db`)에는 Chroma를 새로 만들기 전에 기존 `trd_chunks.sqlite + tfidf_vectorizer.joblib + tfidf_matrix.npz`를 우선 연결하는 어댑터를 검토한다.
- 세부 재현 절차와 파일 계약은 `references/benchmark-ground-truth-and-trd-vector-db.md`를 확인한다.
- 4개 모델(3-way + RAG) 재시험을 동시에 운영할 때는 진행 브리핑/최종확정 게이트를 `references/four-model-benchmark-live-briefing-and-finalization.md` 기준으로 맞춘다(실행 중 중간본과 최종본을 명확히 분리).
- RAG 지표 스키마 차이(precision/f1 결측 처리)와 최종 엑셀 시트 구성은 `references/rag-metric-schema-and-excel-reporting.md`를 확인한다.
- 논문/보고서 최종제출형에서 템플릿 양식을 보존하며 본문만 교체할 때는 `references/docx-final-submission-style-preservation.md`를 확인한다.
- 사용자가 전달한 `.docx`를 리뷰할 때는 먼저 파일 유효성(OOXML zip 여부)을 확인한다. 확장자가 `.docx`여도 내부 시그니처가 zip이 아니면(`python-docx` PackageNotFoundError) 문서가 손상/비표준 저장 상태일 수 있으므로, Word에서 `다른 이름으로 저장(.docx)` 후 재전달을 요청한다.
- 유효하지 않은 `.docx`가 섞인 상황에서도 작업 중단 대신, 같은 폴더의 최근 유효본을 임시 기준으로 먼저 리뷰하고, 최종 코멘트에서 "임시 기준 리뷰"임을 명시한다.

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
- 3-way 벤치가 실행 중일 때 4모델 통합 보고서를 먼저 생성할 수는 있지만, 이 경우 반드시 `중간본(임시)`로 표기하고 완료 후 동일 조건 최신값으로 재생성해 최종본을 교체한다.
- 진행 브리핑 요청 시에는 `완료/진행중/대기`를 분리하고, 백그라운드 프로세스 session_id 및 진행 카운터(예: n/total)를 함께 적어 재현 가능성을 보장한다.
- 사용자가 선호하는 답변 규격(`에이전트이름: 내용`)을 브리핑에서도 유지한다.
- 논문/최종제출형 DOCX 수정은 템플릿 스타일 보존이 우선이다. `python-docx`로 문단 객체를 새로 만들지 말고 기존 문단의 `paragraph.text`만 치환한다.
- 치환 전 `len(new_lines) <= len(doc.paragraphs)`를 확인하고, 초과 시 강제 삽입 대신 요약 압축/문단 매핑 재설계를 먼저 수행한다(스타일 붕괴 및 저장 오류 방지).
- bash heredoc로 긴 한국어 본문을 넣을 때는 인용부호 mismatch(`unexpected EOF while looking for matching '\''`)가 빈번하므로, 작은 블록 단위 또는 외부 .py 파일 실행 방식으로 분리한다.
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

# 참고 레퍼런스(최근 추가)
- MRGA 벡터DB 연동 + 진단 점수화 튜닝 노트: `references/mrga-vector-db-and-diagnosis-tuning.md`
- MRGA 전/후 재생 비교 + 신호라인 기반 query 보강: `references/mrga-prepost-replay-and-signal-query-calibration.md`
- MRGA 보정 전/후 재생 평가 패턴(ground_truth 고정, before/after 커밋 재추론 비교): `references/mrga-prepost-replay-evaluation.md`
- MRGA 리플레이 공정성 가드(질의 생성에서 GT 힌트 누수 방지, 수정 후 즉시 commit/push 및 재측정): `references/mrga-replay-fairness-guardrails.md`
- MRGA 리플레이 공정성 가드(질의 생성에서 GT 힌트 누수 방지, 수정 후 즉시 commit/push 및 재측정): `references/mrga-replay-fairness-guardrails.md`
- MRGA 메모리 스키마 강화 + Ground Truth 자동평가 파이프라인: `references/mrga-memory-schema-and-ground-truth-eval-automation.md`
- MRGA 지속 메모리 스키마 강화/레거시 마이그레이션 패턴: `references/mrga-persistent-memory-schema-migration.md`
- MRGA 튜닝 사이클 운영 규칙(튜닝/질의빌더 변경 시 baseline 고정 비교, 혼합신호군 분리 평가): `references/mrga-tuning-cycle-baseline-and-mixed-signal.md`

# 완료 기준
- 신규 로그 투입 시 자동으로 이상/원인/장기위험 리포트가 생성되고,
- 정비 피드백 누적으로 모델 정확도와 조치 리드타임이 개선된다.
