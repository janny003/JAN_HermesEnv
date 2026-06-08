# BIT 파서 분리 패턴 (POBIT/IBIT/PBIT)

## 언제 적용
- 사용자가 `GetControlCommand1처럼 나눠달라`고 요청할 때
- 의미가 다른 신호(POBIT/IBIT/PBIT)를 동일 파서/루프로 처리해 가독성·추적성이 떨어질 때

## 핵심 원칙
1. 호출부(CESUMain)에서 비트 1~9를 길게 나열하지 않는다.
2. 파서 함수 내부에서 비트별 로컬 변수로 분해한 뒤 `returnData[index]`에 명시 매핑한다.
3. 함수 이름과 도메인 의미를 일치시킨다 (`GetPOBIT`, `GetIBIT`, `GetPBIT`).
4. 하위호환 함수(`GetPowerOnBIT`)는 유지하되 신규 경로는 분리 함수 사용을 우선한다.

## 권장 구현 형태
- `GetPOBIT(inputData)`
  - `completedBit`, `gyroFaultBit`, ... `reservedBit` 로컬 변수 선언
  - `returnData[0..8]`에 순서대로 명시 대입
- `GetIBIT(inputData)`
  - 동일 스타일로 명시 대입
- `GetPBIT(inputData)`
  - `bit1..bit9` 명시 대입

## 피해야 할 패턴
- 호출부에서 `pobit1..9`, `ibit1..9`, `pbit1..9`를 모두 전개 후 배열 재조립
  - 리뷰성/유지보수성이 떨어지고 변경 비용이 커짐
- 도메인 다른 신호를 단일 이름(`GetPowerOnBIT`)으로만 계속 처리

## 검증 체크리스트
- `K2.sln` `Debug|x86` 빌드 성공(오류 0) 확인
- `CESUMain_UUT01.cs`에서 호출은 간결하게 유지:
  - `pobitBit = myd1.GetPOBIT(...)`
  - `ibitBit = myd1.GetIBIT(...)`
  - `pbitBit = myd1.GetPBIT(...)`
- `1553BICD.cs` 내부에서 함수별 비트 매핑이 명시적으로 보이는지 확인
