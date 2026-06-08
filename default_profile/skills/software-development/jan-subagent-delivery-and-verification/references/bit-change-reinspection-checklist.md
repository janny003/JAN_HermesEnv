# BIT 변경분 재확인 체크리스트

## Trigger
사용자가 JAN/ATESWLIB에서 `수정한 부분 다시 확인`, `BIT 부분 다시 봐`, `빌드 말고 수정 경로 확인`처럼 이전 BIT 수정분의 정합성 재검토를 요청할 때 사용한다.

## Scope anchor
- 기본 경로는 별도 지시가 없으면 `C:\Users\yjs\Desktop\JAN\ATESWLIB`이다.
- K2 BIT 작업은 보통 `K2\TestProgram` 아래의 각 장비 프로젝트를 기준으로 확인한다.

## Required verification sequence
1. 최근 커밋/작업트리 기준 확인
   - `git status --short`
   - `git log -1 --oneline --stat -- K2/TestProgram`
   - 필요 시 `git diff --name-only HEAD^ HEAD -- K2/TestProgram`으로 변경 파일 목록을 추린다.
2. BIT 변경 핵심 파일만 필터링
   - `*Main_UUT01.cs`
   - `UUT01_TaskNN.cs`
   - `*.csproj`
   - 관련 파서/ICD 파일: 예) `Core/Data/**/1553BICD.cs`
   - 관련 TPSData JSON이 변경되었는지도 확인한다.
3. 각 모듈별 3점 동기화 확인
   - Task 파일 존재
   - Main의 `AddTask(UUT01_TaskNN)` 등록
   - csproj의 `<Compile Include="UUT01_TaskNN.cs" />` 등록
4. 번호/판정 정합성 확인
   - `CheckByStringValue(big, small, ...)`의 big 번호가 파일명/Task 번호와 일치하는지 확인한다.
   - KGPS 계열은 특히 `KGPS_1 = Task37`, `KGPS_2 = Task38`을 유지한다.
   - CESU/GESU/MFU/KGPS 등 자동 판정 전개 대상은 `UserInput(...PASSFAIL)` 잔존 여부를 별도로 표시한다.
5. 자동/수동 판정 분리 보고
   - 수동 시작 확인용 `UserInput(...CONFIRM)`과 최종 수동 판정용 `UserInput(...PASSFAIL)`을 구분한다.
   - 사용자의 선호상 BIT 최종 판정은 가능한 `RunMainThread`/수신 데이터 기반 자동 판정이어야 하므로, `PASSFAIL` 잔존은 개선 후보로 보고한다.
6. 즉시 빌드 검증
   - 단독 프로젝트 검증은 이 코드베이스에서 `Debug|AnyCPU`가 안전하다.
   - 최소 주요 BIT 대상 프로젝트를 전수 빌드하고 `PASS/FAIL`, `errors`, `warnings`를 표기한다.
7. 마무리 상태 확인
   - 빌드 후 `git status --short`로 검증 산출/의도치 않은 변경이 남았는지 확인한다.

## Reporting shape
- `Jangli :`로 정합성 근거를 간결하게 보고한다.
- `Lucy :`로 빌드 검증 결과를 프로젝트별로 정리한다.
- 결론에는 반드시 다음을 포함한다:
  - Task 등록 정상/비정상
  - csproj 포함 정상/비정상
  - 번호 매핑 정상/비정상
  - 수동 PASSFAIL 잔존 여부
  - 빌드 결과

## Pitfalls
- `search_files`가 인코딩/정규식 문제로 0건을 반환할 수 있으므로, 필요하면 Python으로 UTF-8-SIG/CP949를 모두 시도해 파일을 직접 스캔한다.
- `UserInput` 문자열이 있다고 해서 무조건 수동 판정은 아니다. `CONFIRM`은 시작/절차 확인일 수 있고, `PASSFAIL`은 최종 수동 판정일 가능성이 높다.
- 빌드 산출물이 커밋에 포함된 상태라면 변경 규모가 커 보여도 실제 BIT 소스 변경은 필터링해서 판단해야 한다.
