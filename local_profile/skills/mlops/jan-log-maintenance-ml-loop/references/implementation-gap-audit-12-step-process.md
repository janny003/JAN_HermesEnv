# JAN 12단계 개발 프로세스 구현 점검 기준

이 참고 문서는 현재 OrobrosTest/JAN 정비 자동화 프로그램을 사용자가 확정한 12단계 프로세스에 맞춰 점검할 때의 기준과 반복적으로 발견된 보완 포인트를 정리한다.

## 점검 대상 핵심 파일

- GUI 실행/질문 팝업/프로세스 연동: `OrobrosTestDlg.cpp`
- 로그 로딩/Feature/이상탐지: `tools/inspection_pipeline.py`
- ML 실행 파이프라인: `tools/maintenance_ml_pipeline.py`
- 모델 생성: `tools/model_factory.py`
- Word/JSON 정비 보고서: `tools/generate_maintenance_report.py`
- 보고서+검토 연속 실행: `tools/run_maintenance_with_review.py`
- Step7~9 검토: `tools/ouroboros_review_loop.py`
- 지속 메모리: `out/inspection_memory.json`
- 검토 결과: `out/ouroboros_review*/ouroboros_review_result.json`

## 12단계별 구현 판정 포인트

1. ATE/EGSE 시험 로그 수집
   - TXT 로그뿐 아니라 CSV/SQLite/원천 DB 흐름이 실제 GUI 또는 실행 스크립트에 연결되어 있는지 확인한다.
   - TXT만 읽으면 `부분 구현`으로 판정한다.

2. 로그 Feature 추출 및 전처리
   - `voltage/current/response_time_ms/fail_count/crc_error_rate/retry_count` 등 표준 피처가 추출되는지 확인한다.
   - JAN 시험항목별 세부 피처가 부족하면 baseline 구현으로 판정한다.

3. Isolation Forest 기반 이상 탐지
   - `IsolationForest` 모델 파일 존재와 `score_anomalies()` 또는 보고서 생성에서 실제 사용 여부를 확인한다.
   - Robust Z-score fallback이 있는 것은 정상이다.

4. XGBoost 기반 원인 분석
   - 현재 보고서 생성기는 `xgboost_fault_cause_classifier.pkl` 경로를 찾는지 확인한다.
   - `model_factory.py`가 LightGBM 우선 artifact를 만들도록 바뀐 경우, 보고서 생성기의 로딩 경로와 불일치할 수 있다.
   - 최신 보고서에서 `top_causes`가 `(normal 제외 후 항목 없음)`이거나 원인이 대부분 `normal`이면 원인분석 품질 보완 필요로 판정한다.

5. SKILL.md 저장
   - 운영 프로세스/규칙은 skill에 저장하고, 개별 진단 결과는 skill이 아니라 정비 이력/메모리 JSON에 저장한다.

6. 정비 보고서 초안 작성
   - DOCX와 JSON이 모두 생성되는지 확인한다.
   - JSON은 후속 Step7~9 입력이므로 `--out-json` 계약을 깨지 않는다.

7. Ouroboros Interview/QA/Evaluate 검토
   - 현재 구현은 `ouroboros_review_loop.py` 기반 로컬 Step7~9 검토일 수 있다.
   - 실제 MCP Ouroboros 도구 호출이 필요한 요구라면 별도 연동으로 판정한다.
   - GUI에는 `[INTERVIEW_Q1..4]`가 stdout으로 나와야 하며, Yes/No 팝업 4개가 각각 떠야 한다.

8. 과거 정비 이력/시험 로그/보고서 비교
   - `history-dir`에는 보고서 JSON만 넣는 것이 원칙이다.
   - `out` 전체를 history로 쓰면 `inspection_memory.json`이 섞여 통계가 왜곡될 수 있다.
   - 권장: `out/report_history/` 또는 `Policy/Data/reports/` 같은 전용 폴더 사용.

9. 빠진 점/근거 부족/추가 점검/우선순위 재정렬 피드백
   - `priority_reorder`, `risk_trend`, `evidence`, `coverage`, `root_cause` 피드백이 생성되는지 확인한다.
   - 원인분류가 전부 `normal`인데 QA가 pass면 QA 기준이 너무 약한 것이다.

10. 사용자 최종 진단 확정
   - `next_steps`에만 `step10_user_confirmation`이 있으면 부분 구현이다.
   - GUI 또는 래퍼에서 최종 확정 입력을 받아야 완전 구현으로 본다.
   - `run_maintenance_with_review.py`는 Step7 Yes/No 4문항 뒤에 `[FINAL_CONFIRM_Q]`/`[FINAL_CONFIRM_A]` 계약으로 최종 확정 상태를 별도 수집한다.
   - 확정 입력은 Step7 답변 배열과 섞지 않고 `approved`/`pending`/`rejected`로 정규화한다. 알 수 없는 입력과 EOF는 안전하게 `rejected`로 처리한다.

11. 최종 결과 지속 메모리/정비 이력 저장
   - Step7 답변 저장만으로는 부족하다.
   - 최종 확정 진단 JSON을 `out/final_diagnosis/` 등에 저장하고, `inspection_memory.json` history에도 확정 상태를 남겨야 한다.
   - `approved`일 때만 `final_diagnosis_*.json`, legacy `history[].final_confirmed=True`, split `verification.approvals[]`, split `episode.episodes[]`에 최종 이력을 저장한다.
   - `pending`/`rejected`는 확정 이력으로 쓰지 말고 split `verification.audit_log[]`에만 감사 기록으로 남긴다.

12. 다음 진단 때 다시 참고
   - `apply_final_confirmation_priority()`, `apply_resolved_priority()`, `apply_interview_priority()`, `build_interview_memory_note()` 등이 실제 보고서 문구/우선순위에 반영되는지 확인한다.
   - Step10/11 `approved` 최종확정 이력은 split `verification.approvals[]` 또는 legacy `history[].final_confirmed=True`에서 읽어, 같은 시험 ID(`test_ids`/`similar_tests`)나 `GLOBAL` 이력의 `recommended_actions`/`final_priority_check_order`를 다음 진단 `우선점검권고`와 `final_confirmation_note`에 반영한다. `rejected`/`pending` 감사 이력은 우선순위에 쓰지 않는다.
   - 모델 재학습까지 자동 반영되는지는 별도 판정한다.

## 반복 보완 우선순위

1. XGBoost/LightGBM 모델 artifact 이름과 보고서 로딩 경로 정합성 정리
2. 원인분류가 `normal`에 치우치는 문제 개선
3. Step8 history 전용 폴더 분리 및 `inspection_memory.json` 혼입 차단
4. Step10 사용자 최종확정과 Step11 최종 진단 이력 저장을 GUI 기본 흐름에 통합
5. 실제 MCP Ouroboros Interview/QA/Evaluate 호출이 필요한 경우 로컬 검토 스크립트와 구분해 연동

## 검증 명령 패턴

- Python 회귀 테스트: `python -m pytest -q`
- Step7→Step10→Step12 wrapper E2E 회귀 테스트: `python -m pytest tests/test_run_maintenance_with_review.py::test_wrapper_e2e_approved_final_confirmation_is_used_by_next_diagnosis -q`
  - 이 테스트는 `run_maintenance_with_review.py`에 `--memory-json`과 `--fault-exclusion-csv`를 전달해 임시 메모리로 격리 실행한다.
  - 1차 실행에서 4개 Step7 Yes/No + `approved` 최종확정을 저장하고, 2차 실행에서 이전 승인 이력이 `final_confirmation_note`와 `우선점검권고`에 반영되는지 확인한다.
- MFC 빌드(Windows bash/MSYS에서 slash 변환 주의):
  - `cmd.exe /c '"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe" OrobrosTest.sln /p:Configuration=Debug /p:Platform=x64 /m'`

MSYS bash에서 MSBuild를 직접 호출하면 `/p:...`가 경로처럼 변환될 수 있으므로 `cmd.exe /c` 래핑을 우선 사용한다.
