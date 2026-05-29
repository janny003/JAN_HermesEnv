# MFC에서 Ouroboros Step7 질문이 안 보일 때 점검 절차

## 증상
- DOCX/JSON 리포트는 생성되는데, GUI transcript에 Interview 질문이 보이지 않음.
- 사용자 체감상 `ouroboros_review_loop.py`가 실행되지 않은 것처럼 보임.

## 원인 패턴
1. 리뷰 스크립트가 질문을 파일(JSON/MD)로만 저장하고 stdout에는 내보내지 않음.
2. MFC `MaybeShowQuestionDialog`가 command 문자열의 `ouroboros`만 검사하여, 래퍼 스크립트 실행 시 질문 감지를 건너뜀.
3. Start 기본 커맨드가 6단계 리포트 스크립트만 실행하고 7~9단계를 연결하지 않음.

## 권장 구현 패턴
1. 브리지 스크립트(`run_maintenance_with_review.py`)를 사용해:
   - 1차: `generate_maintenance_report.py`
   - 2차: `ouroboros_review_loop.py`
   를 순차 실행한다.
2. 브리지 스크립트가 리뷰 JSON을 다시 읽어 stdout에 아래 형식으로 출력한다.
   - `[REVIEW] score=<num> verdict=<ready|needs_review|...> qa_checks=<n>`
   - `[INTERVIEW_Q1] ...`
   - `[INTERVIEW_Q2] ...`
3. MFC 질문 팝업 감지 조건을 확장한다.
   - `ouroboros` 또는 `run_maintenance_with_review.py` 포함 시 질문 감지 로직 허용.

## 검증 체크리스트
- [ ] transcript에 `[RUN] ... ouroboros_review_loop.py ...` 라인이 보이는가?
- [ ] transcript에 `[INTERVIEW_Q1..]` 라인이 보이는가?
- [ ] transcript에 `[REVIEW] score=... verdict=...` 라인이 보이는가?
- [ ] 결과 파일이 생성되는가?
  - `out/ouroboros_review_*/ouroboros_review_result.json`
  - `out/ouroboros_review_*/ouroboros_review_result.md`

## 주의
- `history-dir`로 `out/` 전체를 쓰면 `inspection_memory.json` 등 비보고서 JSON이 비교에 섞일 수 있다. 가능하면 보고서 JSON 전용 폴더를 쓰거나 필터링을 추가한다.
