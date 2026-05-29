# LAND8116: HUMS 시험항목 누락 + CP949 안전 수정 패턴

## 증상
- 시험 트리에서 HUMS 항목이 일부만 표시됨.
- 코드상 테스트 구현은 존재하지만 UI 트리 삽입 루프가 일찍 종료됨.

## 근본 원인
- `LANDTestView.cpp`의 임시 제한 매크로:
  - `#define maintest_HUMSSW_visible_end 16`
- 트리 삽입 루프가 `for (i = maintest_tr_size; i < maintest_HUMSSW_visible_end; i++)`로 구성되어 TH01~TH02만 노출됨.

## 해결
- 매크로를 전체 범위로 복구:
  - `#define maintest_HUMSSW_visible_end maintest_name_size`

## 중요: 인코딩 안전 편집
- 같은 변경을 일반 patch로 적용 시 CP949 취약 파일에서 `C2001/C1057/C2059` 연쇄 컴파일 에러가 재발할 수 있음.
- 안전한 방식:
  1) `git checkout -- LANDTestView.cpp`로 원복
  2) `read_bytes -> decode('cp949') -> 1줄 치환 -> encode('cp949')` 방식으로 저장
  3) 즉시 Debug|Win32 빌드 검증

## 검증 포인트
- 빌드 성공(오류 0)
- 시험 화면의 HUMS Verification/HUMS SW 트리 전체 항목 표시 확인
- 런타임 실행 프로세스 확인
