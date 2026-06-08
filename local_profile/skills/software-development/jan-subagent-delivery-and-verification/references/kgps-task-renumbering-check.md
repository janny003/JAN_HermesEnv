# KGPS Task Renumbering Check (session pattern)

## Scope
KGPS_1 BIT 시험 번호를 38에서 37로 이동할 때 발생한 정합 포인트 요약.

## Why this matters
번호만 바꾸고 파일/등록을 일부 그대로 두면 실행은 되더라도 유지보수자가 시험 번호를 오해하기 쉽다.

## Minimal verification sequence
1. 대상 `*Main_UUT01.cs`에서 `AddTask(UUT01_Task37)` 활성화 여부 확인
2. 기존 번호 연결(`AddTask(UUT01_Task38)`)의 의도(비활성/대체)를 주석까지 점검
3. Task 파일 내부에서 다음 3개가 37로 일치하는지 확인
   - 메서드명: `UUT01_Task37`
   - 입력 키: `37.1`, `37.2`, `37.3`
   - 판정 인덱스: `CheckByStringValue(37, ... )`
4. `dotnet build <project>.csproj -c Debug` 실행 후 오류 0 확인
5. 가능하면 파일명과 csproj include도 `Task37`로 정리해 번호-파일 불일치 제거

## Reporting snippet
- Jangli : 변경 범위: 메서드/입력키/판정인덱스/AddTask를 37로 통일
- Jangli : 빌드 검증: 오류 0, 경고 N (기존 경고)
