# RAG 지표 스키마 차이와 엑셀 산출 규칙

## 배경
4모델 통합(3-way + RAG) 브리핑에서 `rag_model`은 `status_accuracy`, `cause_top1_accuracy`, `avg_runtime_sec` 중심으로 저장되고,
3-way(`pipeline_only`,`hybrid`,`agent_only`)처럼 confusion matrix(TP/FP/FN/TN)를 기본 제공하지 않을 수 있다.

## 핵심 규칙
1. `precision`, `fail_recall`, `f1`는 TP/FP/FN/TN가 있을 때 계산/표기한다.
2. RAG summary에 TP/FP/FN/TN가 없으면 우선 `benchmark_results_rag_model.csv`에서 `expected_status` vs `predicted_status`를 다시 집계해 TP/FP/FN/TN를 복원한다.
3. 복원 집계가 성공하면 RAG 행에도 `precision/fail_recall/f1`를 채운다. 복원 불가일 때만 `null`(JSON), `-`(표/엑셀)로 남긴다.
4. 사용자 질문(예: "왜 RAG precision이 없나")에는
   - 성능 저하가 원인이 아니라
   - 요약 스키마에 confusion matrix가 빠져 있었기 때문임을 설명하고,
   - 가능하면 결과 CSV 재집계로 즉시 채워 넣는다.

## 최종 보고 엑셀 권장 시트
- `4model_summary`: method, total_logs, status_accuracy, precision, fail_recall, f1, avg_runtime_sec, note
- `ranking`: 정확도 순위/속도 순위
- `3way_detailed`: 3-way 원본 지표(tp/fp/fn/tn 포함)

## 운영 체크
- 3-way 재실행이 끝나기 전 통합표는 `중간본`으로 표기.
- 완료 후 동일 기준 런 결과로 통합 JSON/CSV/MD/XLSX를 재생성.
- 브리핑 형식은 사용자 선호(`에이전트이름: 내용`)를 유지.