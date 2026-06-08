# TIU_2 BIT 시험 추가 체크리스트 (ATESWLIB)

목적: 기존 TIU_2(1~7번) 프로젝트에 BIT 시험을 신규 추가할 때 코드/프로젝트/데이터 불일치를 방지한다.

## 1) 사전 확인
- `TIU_2Main_UUT01.cs`의 AddTask 등록 목록을 확인한다.
- `TIU_2.csproj`의 `<Compile Include="UUT01_TaskNN.cs" />` 목록을 확인한다.
- `BIN/TPSData/TIU_2.json`의 Task 개수/번호를 확인한다(기본 1~7).

## 2) 코드 추가 (3점 동기화)
1. `UUT01_Task08.cs` 생성
   - 전원 인가/통신 연결/초기화 대기/요청 프레임 송수신/판정/연결해제의 순서로 구성
   - 초기화 대기: `IBITRequest` 전 최소 30초 대기(`OnWaitMessage` + `Sleep(30000)` + `OffWaitMessage`)를 기본값으로 둔다.
   - 송수신 짝맞춤: `IBIT/CBIT/CBITDetail` 각각 `CommSend` 직후 `CommReceive`를 1:1로 붙인다.
   - 응답 검증: 세 응답 중 하나라도 미수신(`null` 또는 `Length==0`)이면 즉시 불량 처리 후 종료한다.
2. `TIU_2Main_UUT01.cs`
   - `AddTask(UUT01_Task08); // 8. BIT 시험` 등록
3. `TIU_2.csproj`
   - `<Compile Include="UUT01_Task08.cs" />` 추가

## 3) 데이터 추가 (TPSData 동기화)
- `BIN/TPSData/TIU_2.json`
  - Task Number 8 (`BIT 시험`) 추가
  - Tests[1] 기준/판정값(`양호`) 추가
  - 필요 시 `ImageData`에 `8.5` 안내 문구 추가

## 4) 판정 방식 선택 규칙
- 사용자 요구가 "동일하게 시험 추가"이면 1차는 기존 TIU_2 흐름을 유지해 PASS/FAIL 입력형으로 추가 가능.
- 사용자가 자동판정을 명시하면 이후 단계에서 `RunMainThread` 기반 데이터 폴링 판정으로 전환한다.

## 5) 검증
- `TIU_2.csproj` 단독 빌드(Debug|AnyCPU) 실행
- 보고 항목:
  - 성공/실패
  - 에러 개수
  - 기존 경고와 신규 경고 구분
- 빌드 로그에 `UUT01_Task08.cs`가 실제 컴파일 라인에 포함되었는지 확인한다.

## 6) 흔한 실수
- AddTask만 넣고 csproj Include 누락
- 코드/JSON 중 한쪽만 8번 추가
- 안내 ID(`8.5`)는 만들었는데 실제 Task에서 해당 UserInput 키를 호출하지 않음
- "동일 적용" 요청을 자동판정으로 과해석해 기존 흐름과 충돌
