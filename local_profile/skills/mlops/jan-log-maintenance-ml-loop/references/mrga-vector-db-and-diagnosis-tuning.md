# MRGA vector DB 연결 + 진단 점수화 튜닝 메모

## 배경
- MRGA 저장소: https://github.com/janny003/RAGMaintenanceArchitecture
- 기존 JAN 자산 재사용: `C:\Users\yjs\Desktop\JAN\01. TRD 문서_이전 사업\vector_db`

## 벡터 DB 연결 규칙
- 우선 사용 파일
  - `trd_chunks.sqlite`
  - `tfidf_vectorizer.joblib`
  - `tfidf_matrix.npz`
- retriever 동작
  1) TF-IDF vector DB 검색 우선
  2) 결과가 비거나 초기화 실패 시 keyword fallback
- 기본 목적: 기존 TRD 지식베이스를 그대로 활용하면서, 런타임 실패 복원력을 유지

## ground_truth 기반 평가 산출물 규약
- 입력: `benchmark_results.csv`의 `log_id` 집합(예: 194개)
- 출력 권장
  - `ground_truth.csv`
  - `benchmark_summary_with_ground_truth.csv`
  - `benchmark_summary_with_ground_truth.json`
  - `JAN_three_way_performance_with_ground_truth.md`
- 필수 지표
  - status: `status_accuracy`, `precision`, `fail_recall`, `false_positive_rate`, `f1`
  - cause: `cause_top1_accuracy`, `cause_top3_inclusion`
  - action: `action_top1_accuracy`, `action_top3_inclusion`

## DiagnosisAgent 튜닝 규칙
- 단순 if-else 분기 대신 점수합 기반 분류
- 점수 구성
  - query/context 매칭: 가장 큰 가중치(강한 prior)
  - evidence 매칭: source 가중치 반영
- source 가중치 예시
  - FMEA > 절차서 > ICD > 정비이력
- 회귀 고정 케이스
  - `IFCC 통신 CRC fail` 질의는 `communication_path`로 분류되는 테스트를 유지

## 구현 체크포인트
- 질의 키워드가 전원 키워드가 많은 문서 증거에 덮이지 않도록 query 가중치 우선
- confidence는 trust gate 임계치와 일관되게 정규화
- 회귀 테스트를 먼저 추가한 뒤 튜닝 변경 반영