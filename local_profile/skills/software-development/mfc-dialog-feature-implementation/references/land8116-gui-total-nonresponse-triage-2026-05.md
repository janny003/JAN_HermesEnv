# LAND8116 GUI 전부 무반응 트리아지 (2026-05)

상황
- 사용자 보고: 시험 화면에서 현재 전압/전류 미표시 + 전원 ON/OFF 포함 GUI 제어 전체 무반응.
- 기존 수정: PowerSupply 소켓 재연결/재전송 로직은 있었으나 GUI 체감 개선이 부족.

확인 포인트
1) 메시지맵/핸들러
- `LANDTestView.cpp`에서 전원 버튼 `ON_BN_CLICKED(...)` 바인딩 존재 확인.
- `OnTimer`에서 `TIMER_NOWVOL1` 분기 존재 확인.

2) 타이머 기동 경로
- `SetTimer(TIMER_NOWVOL1, ...)`가 `OnStartTimer(WM_USER+100)` 안에 있음.
- 시험 화면 진입 시 `WM_START_TIMER`가 실제 전송되지 않으면 측정값 갱신이 시작되지 않음.

3) 장비 모드/명령 전달
- `eEnableOutput()` 전에 `RemoteSetting()` 선행 필요.
- SCPI 명령 끝 개행(`\n`) 보정 필요.
- read 실패 시 재연결 + 1회 재시도 유효.

적용 패턴
- 진입 시 타이머 강제 기동
  - `LANDMainView::OnBnClickedButtonTest()`에서
    - `pTestView->ShowWindow(SW_SHOW);`
    - `pTestView->SendMessage(WM_USER + 100, 0, 0);`
- 전원 출력 전 원격모드 보장
  - `CPowerSupply::eEnableOutput()`에서 `RemoteSetting()` 호출 후 `OUTP ON`.
- 통신 안정화
  - `sendCommand()`에서 자동 개행 추가 및 실패 시 재연결 후 재전송.
  - `eMeasureVolt/eMeasureCurr` read 실패 시 1회 재시도.

검증
- Debug|Win32 빌드 성공 확인.
- 런타임에서 다음 순서로 확인:
  1. 시험 화면 진입 직후 전압/전류 1초 갱신 여부
  2. CC/HUMS 전원 ON/OFF 버튼 반응
  3. 둘 다 같은 IP:PORT 사용 시 세션 충돌 가능성(장비 단일 세션 정책) 점검

주의
- `LANDTestView.cpp` 같은 CP949 민감 파일은 부분 읽기 상태에서 블록 패치 시 인코딩 깨짐으로 `C2001/C1057` 연쇄 가능.
- 안전 순서: (a) 파일 원복로 빌드 그린 확보 → (b) 최소 변경(가능하면 sidecar/ASCII only) → (c) 즉시 재빌드.
