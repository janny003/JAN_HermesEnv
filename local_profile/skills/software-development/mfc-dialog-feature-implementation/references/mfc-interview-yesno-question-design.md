# MFC 인터뷰 Yes/No 4문항 설계 + 다중 chunk 파싱 패턴

## 적용 상황
- child 프로세스 stdout에서 `[INTERVIEW_Q1]..[INTERVIEW_Q4]` 질문을 받아 MFC MessageBox(Yes/No)로 응답할 때.
- 한 번의 ReadFile chunk에 질문 여러 개가 함께 들어올 수 있는 구조.

## 관찰된 실패 패턴
1. 질문 4개 출력인데 팝업은 1개만 뜸.
2. `trimmed == m_lastQuestionPopup` 중복방지 때문에 나머지 질문이 스킵됨.
3. 질문 문구가 서술형(주관식)이라 Yes/No 응답과 의미가 어긋남.

## 권장 구현
1) 질문 생성기(파이썬 등)에서 질문을 항상 4개 생성.
2) 4개 모두 Yes/No 폐쇄형 문장으로 작성 (문구 끝에 `(Yes/No)` 명시 권장).
3) MFC 측에서 chunk 전체를 단일 질문으로 처리하지 말고, `[INTERVIEW_Qn]` 마커를 while 루프로 순회.
4) `n`(1~4)을 파싱해 `m_interviewQuestionCount`와 비교:
   - `n <= current`면 이미 처리한 질문으로 간주하고 skip.
   - `n > current`면 해당 질문 팝업 1회 실행 후 count를 n으로 갱신.
5) 총 4문항이면 Yes/No 창 4개가 순차적으로 뜨는지 transcript로 검증.

## race 방어 결합 (필수)
- MessageBox에서 사용자 클릭 대기 중 child가 종료될 수 있음.
- 클릭 직후 다시 생존 확인:
  - `m_running && m_childStdInWr && (WaitForSingleObject(m_pi.hProcess,0)==WAIT_TIMEOUT)`
- 종료 상태면 자동전송 생략(info 로그) 처리.

## 검증 체크
- transcript에 `[DIALOG ANSWER Q1]` ~ `[DIALOG ANSWER Q4]` 순서대로 남는지 확인.
- 종료 직후 클릭 시 `ERROR_INVALID_HANDLE(6)` 팝업 대신 생략 로그로 처리되는지 확인.
- 빌드 검증: 수정 후 즉시 MSBuild 성공(경고/오류) 보고.
