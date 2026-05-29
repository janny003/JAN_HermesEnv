# benchmark ground truth + TRD vector DB reuse

## Scope
JAN 3-way benchmark(Pipeline Only / Hybrid / Agent Only)에서 재실행 비용 없이 지표를 확장할 때 쓰는 절차.

## Input artifacts
- `C:\Users\yjs\Desktop\JAN\comparison_eval\benchmark_results.csv`
- (optional baseline) `benchmark_summary.csv/json`

## Ground truth generation policy
1. `benchmark_results.csv`의 unique `log_id`(194개)를 기준으로 `LOG` 원문을 다시 읽는다.
2. 상태 라벨(`gt_status`): 본문/파일명에서 `Failed|FAIL|불량|고장` 패턴 우선.
3. 원인 라벨(`gt_cause_top1`): 통신/전원/RF/시험실패 규칙 우선 매핑, PASS면 `normal`.
4. 조치 라벨(`gt_action_top1/top3`): 원인별 canonical action map 사용.
5. 산출물: `ground_truth.csv`.

주의: 위 라벨은 "임시 일관비교용"이다. 현장 확정 라벨이 있으면 동일 컬럼 스키마로 교체 후 동일 평가 로직을 재실행한다.

## Metrics to compute
Per method:
- 상태: TP/FN/FP/TN, status_accuracy, precision, fail_recall, FPR, F1
- 원인: cause_top1_accuracy, cause_top3_inclusion
- 조치: action_top1_accuracy, action_top3_inclusion
- 운영: avg_runtime_sec, avg_questions, approval_rate

## Output artifacts
- `benchmark_summary_with_ground_truth.csv`
- `benchmark_summary_with_ground_truth.json`
- `JAN_three_way_performance_with_ground_truth.md`

## Known existing vector DB (reuse first)
TRD 문서용 벡터DB가 이미 존재함:
- `C:\Users\yjs\Desktop\JAN\01. TRD 문서_이전 사업\vector_db\trd_chunks.sqlite`
- `C:\Users\yjs\Desktop\JAN\01. TRD 문서_이전 사업\vector_db\tfidf_vectorizer.joblib`
- `C:\Users\yjs\Desktop\JAN\01. TRD 문서_이전 사업\vector_db\tfidf_matrix.npz`
- `manifest.json` 기준 22 docs / 424 chunks

권장 연결 순서:
1. MRGA retriever에서 기존 TF-IDF 저장소 adapter를 먼저 붙인다.
2. Chroma는 "대체"가 아니라 "추가 backend"로 나중에 병행 지원한다.
3. 동일 query에 대해 TF-IDF vs Chroma 결과를 A/B 로깅해 품질 비교 후 기본 backend를 결정한다.
