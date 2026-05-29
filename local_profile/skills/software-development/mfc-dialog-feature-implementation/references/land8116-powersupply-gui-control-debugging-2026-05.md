# LAND8116 전원공급기 GUI 제어 불능 디버깅 (2026-05)

상황
- 사용자 제보: GUI에서 전원 ON/OFF 제어가 안 됨.
- 설정 IP: `192.168.10.188`, 포트 `8003`.

확인 순서(재현 가능한 최소 절차)
1) 장비 네트워크 직접 확인 (앱 밖에서)
   - TCP connect to `192.168.10.188:8003`
   - `*IDN?` 전송 후 응답 확인
   - 실제 응답 예: `TDK-LAMBDA,Z36-6-LAN,...`
2) 코드 경로 확인
   - `LANDTestView.cpp`의 전원 버튼 핸들러는 `ApplyPowerSupplyOutput()` 경유
   - 내부에서 `eSetVolt/eSetCurr/eEnableOutput` 호출
   - 호출 전 `RefreshConnection()` 또는 연결 상태 보장 로직 없음
3) 연결 생성 타이밍 확인
   - 실질적인 연결 시도는 `OnBnClickedButtonTestStart()` -> `InitializeInstrumentsForTest()` -> `RefreshPowerSupplyConnections(FALSE)` 경로
   - 즉, 테스트 시작 전 전원 버튼 클릭 시 미연결 상태 가능
4) 무반응처럼 보이는 이유 확인
   - `eSetVolt/eSetCurr/eEnableOutput`가 `void` 기반으로 실패를 상위에 전달하지 않음
   - `sendCommand()` 실패가 UI 메시지로 노출되지 않아 사용자 체감은 "버튼이 안 먹음"
5) 시뮬레이션 모드 확인
   - `ApplyPowerSupplyOutput()`는 `IsSimulationMode()` true일 때 실제 명령을 스킵
   - `ipset.ini`의 `MODE` 및 런타임 모드 읽기값 동시 확인

핵심 원인 패턴
- 네트워크 단절이 아니라, "연결 보장 없는 버튼 실행 + 실패 전파 부재 + 모드 스킵 가능성"의 조합.

권장 수정 패턴
- 전원 버튼 핸들러에서 아래 순서 강제:
  1. `pPowerSupply != NULL` 확인
  2. `IsSimulationMode()` 분기 로그 명시
  3. `IsLanSocketConnected()` 아니면 `RefreshConnection()` 시도
  4. 실패 시 즉시 UI/로그에 원인 출력 후 return
  5. 성공 시 `eSetVolt/eSetCurr/eEnableOutput` 실행
- 가능하면 `eSetVolt/eSetCurr/eEnableOutput`를 bool 반환형으로 개선해 전송 실패를 상위로 전달.

빠른 현장 진단 체크리스트
- [ ] `ipset.ini`의 PS IP/PORT가 실제 장비와 일치
- [ ] 테스트 시작 전에 전원 버튼을 누르는 경우 자동 reconnect 수행
- [ ] simulation mode가 0(실장비)인지 확인
- [ ] 실패 시 사용자에게 명확한 문구 표시(connected/disconnected/sim mode)
