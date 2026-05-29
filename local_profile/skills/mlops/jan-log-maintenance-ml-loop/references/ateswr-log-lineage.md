# ATESWR 로그 계보(원천→DB→내보내기) 메모

목적: `C:\Users\yjs\Desktop\JAN\ATESWR-25KA4` 코드에서 JAN LOG의 생성 경로를 빠르게 재확인하기 위한 참조.

## 1) 시험 결과 저장(원천)
- 파일: `UAV_MAIN/UAV_MAIN/Dialog/TestDlg_UserDefineFunc.cpp`
- 함수: `Ctestdlg::savetestresult(...)`
- 동작:
  1. `Typeinserttestlogparam` 구성
  2. `rm_ate_inserttestlog(inserttestlogparam, "")` 호출
  3. 상세 측정치는 `rm_ate_insertequiptestdetail(...)`로 별도 저장

## 2) DB 입력 필드
- 파일: `UAV_MAIN/ATE_DB/ATE_DB.cpp`
- 함수: `rm_ate_inserttestlog(...)`
- INSERT 대상 컬럼:
  - `TL_ID, E_ID, U_ID, TL_RSLT, TL_DATE, TL_TIME, TL_MEMO, TL_FAULT, TL_NO, TL_ARMY, TL_CAUSE, TL_INPUT`

## 3) 조회/내보내기
- 파일: `UAV_MAIN/UAV_MAIN/Dialog/LogDlg.cpp`
  - `OnBnClickedBtnExport()` -> `exportstart(...)`
- 파일: `UAV_MAIN/UAV_MAIN/Dialog/LogDlg_UserDefineFunc.cpp`
  - `savetextfile(...)` : TXT 저장
  - `saveexcelfile(...)` : XLS 저장
  - `exportstart(...)` : XML 저장 (`<TESTLOG><SEARCH>...`)

## 4) ML 적용 시 우선순위
1. 가능하면 DB 원천(TEST_LOG + DETAIL)에서 ETL
2. TXT/XLS/XML은 보조 입력/백필(backfill)로 사용
3. 원인 라벨은 `TL_CAUSE`, `TL_FAULT`, `TL_MEMO`를 우선 사용
4. 시계열 키는 `E_ID` + `TL_DATE/TL_TIME` 기반으로 생성
