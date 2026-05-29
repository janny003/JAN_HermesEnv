# MFC Hermes CSV 자동저장 패턴 (JAN OrobrosTest)

## 목적
MFC Start 버튼으로 Hermes를 실행해 로그 feature 추출 결과를 즉시 CSV로 저장한다.

## 적용 위치
- C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\OrobrosTestDlg.h/.cpp
- C:\Users\yjs\Desktop\JAN\OrobrosTest\OrobrosTestDlg.h/.cpp

## 핵심 구현
1) 출력 누적 버퍼 추가
- 멤버: `CString m_capturedOutput;`
- OnPipeOutput에서 `m_capturedOutput += *text;`
- Start 직전 `m_capturedOutput.Empty();`

2) Hermes 출력 계약(프롬프트)
- 반드시 다음 마커로 감싼 CSV 출력 요구:
  - `CSV_START`
  - header,data...
  - `CSV_END`

3) 종료 후 후처리
- `OnProcessExited`에서 `SaveCsvPostprocess(m_capturedOutput, ...)` 호출
- 마커 구간만 파싱 후 UTF-8로 저장
- 저장 경로: `C:\Users\yjs\Desktop\JAN\Policy\Data\latest_features.csv`

4) 실패 처리
- `CSV_START/CSV_END` 없음, 본문 비어있음, 파일 생성/쓰기 실패를 transcript에 기록
- 메시지 예시: `[CSV SAVE SKIPPED] <원인>`

## 주의
- Hermes가 마커 없이 자연어만 출력하면 저장 실패한다. 프롬프트 계약을 유지해야 한다.
- 양쪽 프로젝트 파일이 드리프트되지 않도록 동기 복사 또는 동일 patch를 적용한다.
