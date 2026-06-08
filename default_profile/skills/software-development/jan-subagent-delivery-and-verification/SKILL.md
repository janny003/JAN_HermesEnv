---
name: jan-subagent-delivery-and-verification
description: JAN 코드 작업에서 서브에이전트 응답 형식과 수정 후 즉시 빌드 검증을 일관 적용하는 실행 스킬
version: 1.0.0
author: Hermes Agent
license: MIT
---

# JAN Subagent Delivery and Verification

## Reference notes
- `references/devlib-spacewire-common-helper-and-verification.md` captures the DevLib SpaceWire common-helper boundary, implementation shape, smoke tests, and reporting pattern.
- `references/devlib-spi-i2c-common-helper-and-verification.md` captures the DevLib SPI/I2C vendor-free helper boundary, recommended file shape, Read.txt documentation pattern, and dual-build/smoke verification steps.
- `references/devlib-spacefibre-common-helper-and-verification.md` captures the DevLib SpaceFibre vendor-free helper boundary, frame/segmentation model, Read.txt documentation pattern, dual-build/smoke verification, and native dependency search steps.
- `references/devlib-arinc-software-loopback-enhancement.md` captures the ARINC629/664/717 software-loopback API pattern for raising completeness safely when vendor SDK signatures are unavailable.
- `references/devlib-full-build-and-warning-summary.md` captures the concise DevLib full-build health-check pattern: dotnet + Visual Studio MSBuild, warning-code summarization, and user-facing "전체적으로 빌드 됩니다" reporting.
- `references/devlib-wpf-io-and-instrument-validation.md` captures the split WPF pattern: `DevLibGUI` for IO/protocol common-helper validation and `DevLibInstrument` for instrument performance validation, including API-name pitfalls and dual WPF build/launch checks.
- `references/devlib-wpf-dll-reference-conversion.md` captures the user-corrected pattern for making DevLibGUI/DevLibInstrument reference the built `DevLib.dll` instead of direct-linking DevLib `.cs` files, including structural checks and direct DLL API smoke verification.
- `references/devlibinstrument-separated-tabs-and-scope-graph.md` captures the DevLibInstrument pattern for splitting combined instrument tabs into device-specific tabs and adding a WPF Canvas/Polyline oscilloscope data graph, including DevLib API boundary notes and Git-Bash `taskkill.exe //PID` build-lock handling.
- `references/devlib-multi-protocol-reinspection-smoke.md` captures the multi-protocol DevLib reinspection pattern for I2C/SPI/SpaceWire/SpaceFibre/CCSDS/CAN and DevLibGUI communication-type coverage extension, including boundary classification, Git-Bash MSBuild switch handling, deterministic smoke checks, vendor-wrapper separation, and Korean UI text checks.
- `references/devlib-communication-helper-git-delivery.md` captures the DevLib communication-helper delivery pattern: RemoteAccess/IO helper boundary, root README update, temporary smoke cleanup, JAN git identity, staged diff hygiene, and remote SHA verification.
- `references/devlib-remoteaccess-ssh-telnet-helper.md` captures the DevLib RemoteAccess SSH/Telnet helper boundary, implementation shape, documentation expectations, namespace-shadowing pitfall, and isolated smoke verification pattern.
- `references/devlibgui-real-connection-input-validation.md` captures the DevLibGUI pattern for turning static communication API coverage into real parameterized TCP/UDP/Serial/CAN/ARINC429 input flows, while separating hardware/vendor dependency risks from actual PASS claims.
- `references/devlibinstrument-real-instrument-input-validation.md` captures the DevLibInstrument WPF pattern for adding real instrument connection/control inputs, safe hardware-call gating, DevLib.dll API mapping, and session-boundary reporting.
- `references/devlib-log-ini-store.md` captures the DevLib Log utility pattern for pure .NET INI save/load, UTF-8 BOM Korean safety, Entry round-trip support, and isolated smoke verification.
- `references/devlib-core-cross-platform-primitives.md` captures the DevLib Core cross-platform primitive pattern: preserve Windows named behavior, add non-Windows fallbacks, use file-backed shared memory, and verify with full build plus isolated Core smoke.
- `references/land8r-bin-runtime-baseline-compare.md` captures the LAND8R/LAND8116 runtime BIN comparison pattern: recursive hash comparison, deployed `BIN\\LAND8116.exe` presence check, line-ending-normalized INI comparison, and reporting of UI config deltas separately from launch blockers.
- `references/land8r-rc-resource-and-vs-cache-recovery.md` captures the LAND8R/LAND8116 pattern for restoring a truncated `.rc`, normalizing a malformed `LAND.sln` first line, verifying Release output copied to `BIN`, and separating Visual Studio `devenv.exe` cache/profile crashes from project build health. Reusable helper: `scripts/normalize_land_sln.py`.
- `references/land8r-dialog-close-and-manual-stopwatch.md` captures the LAND8R/LAND8116 pattern for blocking dialog X/ESC while preserving explicit buttons, adding Manual Stopwatch start/end time history, and avoiding CP949/C4819 regressions with byte-safe edits.
- `references/land8r-git-commit-hygiene-and-msbuild-env.md` captures LAND8R/LAND8116 commit hygiene: stage only intentional source/resource files, remove `.APS`/`.vcxproj.user` noise, clean accidental `.rc` whitespace churn by reapplying intended CP949 hunks from HEAD, retry MSBuild with `env -u tmp` when Git-Bash exposes duplicate `tmp`/`TMP`, and report UNC push blockers separately from local commit success.
- `references/land8r-program-ini-power-supply-settings.md` captures the LAND8R/LAND8116 pattern for making CC/HUMS power-supply voltage/current configurable from `Program.ini` while preserving the existing e* power-control path, encoding checks, Debug|Win32 build, and launch-smoke reporting.
- `references/land8r-stop-final-result-display.md` captures the LAND8R/LAND8116 pattern for preserving final result/lead-time display after 시험 중지, including STOP-vs-FAIL aggregation and result-column index verification.

## When to use
- JAN/ATESWLIB/OrobrosTest 계열 코드 분석, 수정, 검증 요청
- 사용자가 서브에이전트 페르소나 기반 보고를 기대하는 세션
- 기능 수정 직후 빌드 성공/실패를 즉시 확인해야 하는 세션

## Required output contract
1. 모든 사용자 응답(분석/진행보고/메타 안내 포함)은 기본적으로 다음 형식을 사용한다.
   - `subagent 이름 : 대답내용`
2. 사용자가 특정 서브에이전트를 직접 호명한 경우(예: "장리야"), 해당 응답은 우선적으로 Jangli 단일 화자로 시작하고 필요 시 다른 에이전트를 보조로 추가한다.
3. 기술 분석/수정 보고는 Jangli 톤으로 간결·근거 중심으로 작성한다.
4. 사용자에게 전달하는 결론에는 항상 실제 실행 근거(빌드/검증 결과)를 포함한다.

## Sub-agent roster maintenance (policy-only requests)
사용자가 "서브 에이전트 추가/수정"만 요청한 경우에는 코드 빌드 작업보다 정책 일관성 반영을 우선한다.

1. 정책 파일 생성/수정
   - 경로: `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\policies\subagent_<role>_<name>.md`
   - 기존 정책 포맷(Identity/Tone/Behavioral Policy/Working Style/Example Voice)을 유지해 추가한다.
2. 정책 인덱스 동기화
   - `C:\Users\yjs\Desktop\JAN\Policy\OrobrosTest\README.md`의 `Sub-agent policy applied` 목록에 새 파일을 반드시 추가한다.
3. 환경 저장소(JAN_HermesEnv) 동기화
   - 사용자 요청에 따라 `https://github.com/janny003/JAN_HermesEnv.git`에도 동일 정책 파일을 반영한다.
   - 반영 위치는 두 프로필을 모두 포함한다:
     - `default_profile/policies/subagent_<role>_<name>.md`
     - `local_profile/policies/subagent_<role>_<name>.md`
   - `subagent-driven-development` 스킬 목록에도 신규 정책 파일 경로를 추가해 정책 참조 드리프트를 방지한다.
   - 커밋 후 `main` 브랜치 push 성공까지 확인한다.
4. 응답 형식 유지
   - 사용자 보고는 계속 `subagent 이름 : 대답내용` 형식을 사용한다.
4. 검증
   - 생성한 정책 파일을 재열람해 섹션 누락/오탈자를 확인하고, README 반영 여부까지 함께 확인한다.

## Execution steps (code analysis or change)
1. 대상 솔루션/프로젝트 식별
   - 예: `AteMgr_K2.sln`, `K2.sln`, `KDTP_*` 프로젝트
2. 변경 전 호출 경로 확인
   - AddTask 등록 여부, 실제 실행 태스크 연결, UserInput 키 매핑 확인
   - 사용자가 "코드 분석"을 먼저 요청하면, 수정 전에 기준선(baseline) 검증을 선행한다:
     1) 현재 솔루션 기준 빌드 1회(Debug|x86)
     2) 오류/경고 개수와 첫 핵심 경고 유형 정리
     3) 분석 범위 파일(메인 UUT, Task, csproj, TPSData JSON)을 먼저 지정
3. 최소 수정 적용
   - 동작 경로 정합성(AddTask/핸들러/리소스 키)부터 우선
   - 신규 UUT 태스크 추가 시 3점 동기화 필수:
     1) `UUTxx_TaskNN.cs` 파일 생성/수정
     2) 메인 절차 파일(`*Main_UUT01.cs`)에 `AddTask(UUTxx_TaskNN);` 등록
     3) 해당 `*.csproj`의 `<Compile Include="UUTxx_TaskNN.cs" />` 등록
   - 기존 시험 번호를 변경(예: 38→37)할 때는 "번호 4점 동기화"를 추가로 강제한다:
     1) 메서드명(`UUT01_TaskNN`)과 내부 UserInput 키(`NN.1` 등)
     2) 결과 판정 인덱스(`CheckByStringValue(NN, ...)`)
     3) 메인 `AddTask` 연결 대상 번호
     4) 파일명/`csproj Include` 일치(동작만 맞고 파일명이 어긋난 상태를 남기지 않기)
   - 위 항목 중 하나라도 누락되면 "실행 번호와 UI 번호 불일치" 또는 "유지보수 시 오판"이 발생한다.
   - 사용자가 "A도 했으니 B/C도 동일 적용"을 요청하면, 복제 적용 체크리스트를 사용해 sibling 프로젝트를 동기화한다.
     - 코드 4점 동기화: `AddTask` 등록, 시험 개수 배열 크기(`arrayTestNum`) 확장, 메인 수신 루프의 프레임 생성/수신/파싱 연결, 신규 Task 파일 구현
     - 프로젝트 동기화: 각 sibling `*.csproj`에 `<Compile Include="UUTxx_TaskNN.cs" />` 추가
     - 데이터 동기화: 각 sibling `BIN/TPSData/*.json`에 동일 Task 번호/제목/Tests를 추가하고 JSON 문법 검증
     - 검증 동기화: 전체 `K2.sln` 빌드 로그에서 sibling 프로젝트(`KCPS_1.csproj`, `KCPS_2.csproj` 등) 실제 컴파일 라인 포함 여부까지 확인
   - 사용자가 특정 BIT Task를 "일단 주석처리"하라고 요청하면 `references/ateswlib-bit-task-temporary-disable.md`를 적용한다.
     - 실행 제외: `*Main_UUT01.cs`의 해당 `AddTask(UUT01_TaskNN);`를 주석 처리한다.
     - 컴파일 제외: 같은 프로젝트 `*.csproj`의 `<Compile Include="UUT01_TaskNN.cs" />`도 함께 XML 주석 처리한다.
     - 파일 삭제는 명시 요청이 없으면 하지 않는다.
     - 직접 csproj 빌드는 프로젝트에 정의된 플랫폼(`Debug|AnyCPU` 등)을 확인하고, 전체 납품 검증은 별도로 `K2.sln Debug|x86`로 수행한다.
   - 사용자 정정("아니, X가 맞고 Y가 맞다")이 들어오면 즉시 번호/경로 정합성 재실측 후 수정한다.
     - 최소 재검증 순서: `*.csproj Compile Include` → 실제 `UUTxx_TaskNN.cs` 내용 → `*Main_UUT01.cs` AddTask 매핑 → 재빌드.
     - 정정 보고 시에는 "기존 주장"이 아니라 "재실측 결과" 기준으로만 결론을 갱신한다.
   - BIT 수신 로직 수정 시에는 메시지 채널별로 수신/파싱/판정을 분리해 연결한다.
   - ATESWLIB 1553B 구현을 DevLib 재사용 모듈로 옮기는 요청에서는 기존 장비 제어 클래스(`CEXC1553B.cs`)를 먼저 건드리지 말고, 하드웨어 DLL 의존이 없는 순수 계산/ICD/비트 판정/문자열 변환 로직을 `IO/1553B/Common`, `IO/1553B/K2`, `IO/1553B/Excalibur` 책임으로 나누어 추가한다. 세부 절차는 `references/devlib-1553b-reusable-codec-extraction.md`를 따른다.
   - ICD/TPSData와 BIT 로직을 재대조할 때는 `references/ateswlib-bit-subtest-label-reconciliation.md` 절차를 사용해 TPSData subtest 라벨, `CheckByStringValue` 슬롯, 메인 수신/파서 배선을 함께 맞춘다.
   - 장비군 간 "같은 방식으로 적용" 요청에서는 BIT 시험 번호를 고정 가정하지 말고, sibling별 실제 Task 매핑을 먼저 확인한다.
     - 예: CESU/GESU는 `UUT01_Task07`, MFU_1/MFU_2는 `UUT01_Task10`이 BIT 시험일 수 있다.
     - 적용 순서: `*.csproj`의 Compile Include 확인 -> 해당 Task 파일에서 `UserInput(...PASSFAIL)` 여부 확인 -> 메인 `AddTask`/수신루프 연결 확인 후 수정.
     - 프로젝트 ICD 용어를 우선으로 네이밍을 맞춘다. 예: `(4,4,1)`이 Power-On BIT이면 코드/로그/패널 라벨을 `POBIT`로 통일하고 `PBIT`/`CBIT`와 절대 혼용하지 않는다.
     - `(4,5,1)=IBIT`, `(4,6,1)=PBIT`처럼 프레임별 저장 배열과 판정 대상을 1:1로 고정한다.
     - 사용자가 "분리"를 요구하면 호출 경로 분리(예: `GetPOBIT/GetIBIT/GetPBIT`)를 먼저 적용하고, 기존 공용 함수(`GetPowerOnBIT`)는 하위호환 래퍼로 유지해 회귀 위험을 줄인다.
     - 분리 후에는 CESU 메인 수신부 호출을 반드시 전환한다. 예: `pobitBit <- GetPOBIT`, `ibitBit <- GetIBIT`, `pbitBit <- GetPBIT`.
   - 네이밍 리팩터 후에는 사용처 전수 치환을 반드시 수행한다.
     - 선언/수신/파싱/Task 판정/패널 전송 라벨/기존 Task(UUT01_Task04 등) 참조를 모두 확인해 컴파일 잔오류(`name does not exist`)를 제거한다.
   - DevLib 공통 라이브러리 수정 시에는 `references/devlib-common-library-boundary.md`를 적용한다.
     - DevLib에는 여러 프로젝트에서 그대로 재사용 가능한 공통 함수만 둔다.
     - DevLib `Core`의 shared memory/event/semaphore/mutex/thread/time 같은 OS-adjacent primitive를 Windows/Linux 호환으로 수정할 때는 `references/devlib-core-cross-platform-primitives.md`를 적용한다.
      - Windows에서는 기존 named primitive 동작을 보존하고, 비Windows에서는 안전 fallback을 둔다.
      - Linux 실기동 환경이 없으면 Docker/WSL 미설치 같은 환경 상태를 영구 제약으로 남기지 말고, full build + isolated Core smoke + Linux runtime 미검증을 분리 보고한다.
    - DevLib `Utiliy\\Log`에 INI 저장/읽기 기능을 추가할 때는 `references/devlib-log-ini-store.md`를 적용한다. Win32 P/Invoke보다 순수 .NET 구현을 우선하고, UTF-8 BOM 저장/한글 표시/Entry round-trip smoke를 함께 검증한다.
     - K2/KGPS/KCPS ICD codec, POBIT/IBIT/PBIT 같은 BIT 파서/판정 규칙, `TPSManager.RscDo` 문자열/래퍼, Task/TPSData 종속 로직은 DevLib에서 제외하고 각 프로젝트 Core/Data 또는 TPS 계층에 둔다.
     - 전체 DevLib 빌드가 외부 장비/영상 의존성으로 실패하면, 수정한 공통 `.cs` 파일만 링크한 임시 smoke project로 별도 컴파일/동작 검증을 수행하고 full build 실패와 isolated smoke 성공을 분리 보고한다.
     - DevLib 통신 helper 작업을 git에 올릴 때는 `references/devlib-communication-helper-git-delivery.md`를 추가 적용한다. 루트 `README.md` 진행사항 업데이트, smoke 산출물 미포함, 기존 `.gitignore` 보존, JAN 로컬 git identity, `git diff --cached --check`, push 후 local/remote SHA 일치 확인까지 수행한다.
   - DevLib ARINC429/DDC wrapper 수정 시에는 `references/devlib-arinc429-wrapper-safety.md`를 추가 적용한다.
     - vendor header와 P/Invoke signature를 먼저 대조하고, `DDCAPI`/`WINAPI` 계열은 `CallingConvention.StdCall` 명시를 우선 검토한다.
     - `ReadRxQueueIrigMore`/`LoadTxQueueMore`처럼 native가 배열 포인터와 count를 받는 함수는 단일 필드 주소를 넘기지 말고, `s16N` 길이 검증 후 배열을 pin한다.
     - `Open`, `Close`, queue read/load 계열은 native status/count/error를 버리지 말고 public API에 맞게 보존·전달한다.
   - DevLibGUI 또는 DevLibInstrument를 WPF로 분리/확장하는 요청에서는 `references/devlib-wpf-io-and-instrument-validation.md`를 적용한다.
     - `DevLibGUI`는 IO/protocol 공통 helper 검증 전용으로 둔다.
     - DevLibGUI 또는 DevLibInstrument를 WPF로 분리/확장하는 요청에서는 `references/devlib-wpf-io-and-instrument-validation.md`를 적용한다.
       - 기본 방향은 `DevLibGUI`를 IO/protocol 공통 helper 검증 전용으로 두고, 외부 장비 의존성을 피하기 위해 필요한 vendor-free `.cs` 파일만 링크하는 것이다.
       - 단, 사용자가 명시적으로 "DevLib.dll 참조" 또는 "DLL 안의 함수가 동작"을 요구하면 기본 링크 방식보다 사용자 지시를 우선하고 `references/devlib-wpf-dll-reference-conversion.md`를 적용한다. 이때 WPF `.csproj`에는 `<Reference Include="DevLib">` + `HintPath`를 두고, 직접 DevLib `.cs` 링크가 남아 있지 않은지 확인한다.
       - `DevLibInstrument`는 기존 C++/DLL 소스 폴더를 보존한 채 별도 root-level WPF 프로젝트/솔루션을 추가한다.
       - 계측기 성능 검증은 먼저 기준값/측정값/허용오차 기반의 deterministic UI 판정으로 만들고, 재사용 판정 로직은 가능하면 `DevLib.Instrument` 같은 DLL public API에 둔 뒤 WPF에서 호출한다.
       - 사용자가 DevLibInstrument도 DevLibGUI처럼 `connection에 필요한 입력 인자`를 받으라고 요청하면 `references/devlibinstrument-real-instrument-input-validation.md`를 적용한다. VISA Resource/Channel/Frequency/Level/Range/Resolution/Marker 같은 실제 입력을 노출하고, 기본은 API 매핑 확인으로 두며, 실제 장비 호출은 `실제 장비 호출 허용` 같은 명시적 체크박스로 gate한다. `COscilloscope`/`CNetworkAnalyzer`처럼 public `Open(resource)`가 없는 class는 Resource를 입력받더라도 실제 연결 완료로 과장하지 말고 세션 전제/adapter 후속 필요성을 보고한다.
- DevLibGUI 또는 DevLib 신규 공통 프로토콜 모듈(CCSDS 등)을 작업할 때는 `references/devlib-gui-wpf-validator-and-ccsds.md`를 적용한다.
     - DevLibGUI 교체 요청은 기존 MFC/InstrumentControl 유지보다 WPF 기반 공통함수 검증 앱으로 정리하는 방향을 우선한다.
     - DevLibGUI는 전체 DevLib 프로젝트 참조 대신 검증 대상 공통 `.cs` 파일만 링크해 외부 장비/영상 의존성으로부터 분리한다.
     - `DevLib\IO\CCSDS`에는 primary header, packet create/parse, byte/hex, CRC-16 같은 표준 공통 helper만 두고 APID 의미/장비별 TMTC/secondary header mission format은 각 프로젝트 계층에 둔다.
   - DevLibGUI를 DevLib 검증 GUI로 재작성할 때는 `references/devlibgui-wpf-common-validator.md`를 적용한다.
     - 기존 MFC/InstrumentControl 구조를 삭제하되 `.git`은 보존한다.
     - 전체 DevLib 프로젝트를 참조하지 말고 검증 대상 공통 `.cs` 파일만 WPF 프로젝트에 링크한다.
     - WPF 화면은 Command Word, Word/Hex codec, SignExtend, pack/split 같은 공통 함수 검증 중심으로 구성한다.
     - `dotnet build DevLibGUI.sln -c Debug`, 한글 깨짐 검색, `git diff --cached --check`, 커밋까지 확인한다.
   - DevLib ARINC429/DD42992 wrapper를 점검하거나 수정할 때는 `references/devlib-arinc429-wrapper-verification.md`를 적용한다.
     - 실제 경로/명칭(`Arinc429`)과 vendor header signature를 먼저 재실측한다.
     - native 반환값을 고정 `true/false`로 덮어쓰지 말고 wrapper 반환 정책을 정상화한다.
     - `ReadRxQueueIrigMore`/`LoadTxQueueMore`처럼 N개 buffer를 받는 함수는 배열 길이 검증과 반환값 보존을 우선한다.
     - 전체 DevLib 빌드가 COMReference 등 unrelated infrastructure 문제로 막히면 isolated smoke project 결과와 full build 실패를 분리 보고한다.
   - DevLib에 ARINC664/717/629 같은 신규 공통 항공 프로토콜 모듈을 "동일하게" 추가하거나, 외부 장비/영상/COM 의존성 때문에 전체 빌드가 막힐 때는 `references/devlib-arinc-protocol-helper-and-build-stabilization.md`를 적용한다.
     - vendor header/native DLL이 없으면 P/Invoke wrapper를 임의 생성하지 말고 reusable validation/packing/parsing helper로 구현한다.
     - `DevLib.Commu.Arinc664/Arinc717/Arinc629` namespace와 `CArincXXX.cs` 파일 구조를 맞춘다.
     - 빌드 통과를 위해 외부 의존 폴더를 제외한 경우, 해당 기능이 산출 DLL에 포함되지 않는다는 점을 반드시 보고한다.
     - "빌드 되게" 요청은 가능하면 `dotnet build`와 Visual Studio MSBuild 양쪽을 모두 검증한다.
   - 사용자가 ARINC629/664/717을 "429 정도로" 완성도를 올리라고 요청하면 `references/devlib-arinc-software-loopback-enhancement.md`를 적용한다.
     - 실제 vendor SDK/header가 없을 때는 429 같은 real hardware wrapper라고 주장하지 말고, `Open/Close/EnableTx/EnableRx/Load/Read/GetRxQueueStatus` 형태의 deterministic software-loopback API로 consuming project 검증성을 올린다.
     - ARINC629은 terminal-id queue + 20-bit word helper, ARINC664은 VL-id queue + Ethernet/VL/sequence helper, ARINC717은 stream-id queue + 12-bit/sync/subframe helper로 확장한다.
     - 수정 후에는 compile-only가 아니라 임시 console smoke로 정상 flow와 wrong id/disabled TX/empty read/close mismatch 같은 엣지 조건을 함께 확인한다.
   - DevLib에 SPI/I2C 같은 신규 공통 IO 프로토콜 모듈을 "동일한 방식"으로 추가할 때는 `references/devlib-spi-i2c-common-helper-and-verification.md`를 적용한다.
     - 특정 SPI/I2C controller SDK가 제시되지 않으면 native wrapper를 임의 생성하지 말고 vendor-free metadata/transfer/frame/address/hex helper로 구현한다.
     - 실제 SPI transfer, I2C repeated-start, ACK/NACK retry, clock stretching은 controller adapter 또는 프로젝트 계층 책임으로 명시한다.
     - `Read.txt`는 통신 특성/주요 코드/사용 예/주의사항 구조로 작성하고, 실제 bus open/read/write가 포함되지 않았음을 분명히 적는다.
     - 검증은 DevLib `dotnet build`, Visual Studio MSBuild, 임시 smoke console, SPI/I2C source 내 `DllImport`/vendor dependency 검색을 함께 수행한다.
   - 사용자가 I2C/SPI/SpaceWire/SpaceFibre/CCSDS/CAN처럼 여러 DevLib IO 프로토콜을 한 번에 "다시 확인"하라고 하면 `references/devlib-multi-protocol-reinspection-smoke.md`를 적용한다.
     - 폴더/파일 존재만 보지 말고 API shape, vendor-free/helper boundary, full build, deterministic smoke 결과를 함께 확인한다.
     - CAN은 Kvaser/uCANDLL 기반 real vendor wrapper 영역이므로 vendor-free helper 모듈들과 분리해 보고한다.
     - Git-Bash에서 Visual Studio MSBuild를 실행할 때 `/p:`/`/v:`가 MSYS path 변환으로 깨질 수 있으므로 `-p:`/`-v:` 스위치를 사용한다.
     - 임시 smoke 프로젝트는 repo 밖 temp 경로에 만들고, hardware 통신 검증과 common helper 검증을 혼동하지 않는다.
   - DevLib에 SpaceFibre 같은 SpaceWire-adjacent 신규 공통 프로토콜 모듈을 추가할 때는 `references/devlib-spacefibre-common-helper-and-verification.md`를 적용한다.
     - 구체적인 FPGA/card/vendor SDK가 제시되지 않으면 real link open/close, lane configuration, DMA, interrupt, FDIR/QoS scheduling wrapper를 만들지 않는다.
     - 우선 vendor-free virtual-channel frame metadata, packet segmentation/reassembly, broadcast payload, sequence validation, hex/CRC helper로 구현한다.
     - frame byte encoding이 실제 wire frame이 아니라 DevLib 내부 helper 검증용 metadata encoding임을 `Read.txt`와 보고서에 명시한다.
     - 검증은 DevLib `dotnet build`, Visual Studio MSBuild, 임시 smoke console, SpaceFibre source 내 native/vendor dependency 검색을 함께 수행한다.
   - 사용자가 DevLibGUI에서 DevLib IO 코드를 통신별로 모두 검증 가능하게 하라고 요청하면 `references/devlib-multi-protocol-reinspection-smoke.md`의 DevLibGUI coverage-extension pattern을 적용한다.
     - 기존 deterministic helper 탭(1553B/CCSDS/SPI/I2C/SpaceWire/SpaceFibre/ARINC629/664/717)은 유지한다.
     - TCP/UDP/Serial/CAN/ARINC429은 별도 탭 또는 그룹으로 분리해 API coverage와 vendor/hardware dependency boundary를 명확히 표시한다.
     - 사용자가 "connection에 필요한 입력 인자"나 "DLL 함수가 실제 동작"을 지적하면 `references/devlibgui-real-connection-input-validation.md`를 추가 적용한다. Host/Port/Message, Serial Port/Baud/DataBits/Parity/StopBits, CAN Channel/ID/Hex/Filter/Virtual, ARINC429 Card/Tx/Rx/Data Word 같은 실제 호출 인자를 UI에 노출하고 가능한 DevLib public API 호출에 연결한다.
     - CAN(Kvaser/UCAN)과 ARINC429는 실제 통신 PASS로 과장하지 말고, 장비/DLL/드라이버가 필요한 영역임을 UI와 보고서에 함께 남긴다.
     - 수정 후 `DevLib` 빌드, `DevLibGUI` 빌드, GUI launch smoke, 한글 replacement character 검색까지 수행한다.
   - DevLib `RemoteAccess`에 SSH/Telnet 같은 원격 접속 공통 helper를 추가할 때는 `references/devlib-remoteaccess-ssh-telnet-helper.md`를 적용한다.
     - SSH는 비밀번호 저장/자동입력보다 OpenSSH key/ssh-agent/config 기반 command wrapper로 제한하고, 장비별 login/판정 스크립트는 프로젝트 계층에 둔다.
     - Telnet은 범용 text TCP session helper(connect/write/read-until/close)와 기본 IAC negotiation byte 필터링까지만 둔다.
     - `README.md`와 주변 DevLib 관례에 맞춘 `Read.txt`에 보안 주의사항, 사용 예, 구현 범위를 함께 적는다.
     - full DevLib build, RemoteAccess-only isolated smoke, 프로젝트 종속 키워드/native dependency 검색을 분리 검증한다.
4. 수정 직후 즉시 빌드 검증
   - 성공/실패와 핵심 에러 1~3개를 바로 보고
5. 사용자의 재빌드 요청("다시 빌드")은 동일 조건으로 즉시 재실행
   - 직전 실패 이력이 있어도 가정하지 말고, 같은 구성(Debug|x86 등)으로 실제 재검증
   - 결과가 바뀌면(실패→성공) 이전 원인 메시지를 고정 사실처럼 유지하지 말고 최신 결과로 교체 보고
6. 사용자가 커밋을 요청하면 빌드 산출물과 obj/cache 노이즈를 분리한다.
   - 먼저 `git status --short`와 `git diff --stat`으로 변경 범위를 확인한다.
   - 의도한 소스/필요한 `BIN/TPS/*.dll|*.pdb`만 선별 stage하고, `K2/TestProgram/*/obj/Debug/*` 캐시·중간산출물은 커밋하지 않는다.
   - LAND8R/LAND8116에서는 `*.APS`, `*.vcxproj.user` 같은 Visual Studio 로컬 생성물도 커밋하지 않는다.
   - LAND8R/LAND8116에서 CC/HUMS 전원 전압·전류를 하드코딩에서 설정값으로 옮기는 요청은 `references/land8r-program-ini-power-supply-settings.md`를 적용한다. `BIN\\Config\\Program.ini`의 `[PowerSupplyOutput]` 키를 읽고, 기존 `PowerSupply.cpp` e* 함수 경로를 유지하며, missing/invalid 값은 안전한 기본값으로 fallback한다.
   - LAND8R/LAND8116에서 시험 중지 후 결과값/소요시간이 사라지는 문제는 `references/land8r-stop-final-result-display.md`를 적용한다. Stop finalization 분기에서 결과 필드를 빈 문자열로 지우지 말고, 현재까지의 결과 리스트 기준 FAIL 우선/없으면 STOP으로 표시하며, 결과 컬럼 인덱스가 실제 UI 컬럼과 맞는지 재확인한다.
   - `.rc` 파일 diff가 기능 변경보다 훨씬 크고 trailing whitespace/EOF 노이즈가 많으면, staged check 전에 HEAD blob에서 CP949로 다시 읽어 의도한 resource hunk만 재적용한다.
   - `git diff --cached --check`를 통과시킨 뒤 커밋한다.
   - 커밋 후 남은 obj/cache 또는 부수 빌드 산출물이 있으면 `git restore .` 등으로 작업트리를 정리하고, 마지막에 `git status --short`가 clean인지 확인해 보고한다.
   - 세부 LAND8R/LAND8116 commit hygiene는 `references/land8r-git-commit-hygiene-and-msbuild-env.md`를 따른다.
7. 회귀 위험 요약
   - 스레드 중단(Thread.Abort), 포트 연결/해제, 프로세스 Kill 키 불일치 등

## Pitfalls
- 코드가 파일에 존재해도 AddTask 미등록이면 실행되지 않는다.
- 문서 비교 결과에 OOXML 원문 태그(`w:rsidR`, `w:fldChar`, `w:webHidden` 등)를 그대로 노출하면 사용자가 변경점을 해석하기 어렵다. DOCX는 `python-docx` 문단 텍스트, PDF는 PyMuPDF 텍스트로 정리한 `clean context` 기준 매핑으로 보고한다.
- C# 로컬 함수 문법(`bool Foo(){}`를 메서드 내부에 선언) 사용 시, 이 코드베이스의 일부 프로젝트/컴파일러 설정에서는 파싱 오류(CS1513/CS1520 연쇄)로 실패할 수 있다. BIT 판정 헬퍼는 우선 클래스 레벨 `private` 메서드로 분리해 호환성을 확보한다.
- `*.csproj` 단독 빌드 시 `Debug|x86`가 아니라 `Debug|AnyCPU` 조건에만 `OutputPath`가 정의된 프로젝트가 있다. 단독 검증은 `Platform=AnyCPU`로 수행하고, 솔루션 전체 검증은 별도로 `K2.sln` 기준 상태를 분리 보고한다.
- 데이터 파서 API와 참조 어셈블리 상태가 프로젝트별로 다르다. BIT 3종 분리 구현 시 먼저 Core/Data 네임스페이스의 실제 메서드 가용성을 확인한 뒤 호출 경로를 정한다. 단, 소스 파일에 `GetPOBIT/GetIBIT/GetPBIT`가 존재해도 의존 TPS 프로젝트가 stale/mismatched `BIN/TPS/Core.dll`을 참조하면 CS1061이 계속 날 수 있으므로, `Core.csproj` 단독 빌드 플랫폼(`Debug|AnyCPU`)과 dependent TPS 프로젝트/solution 빌드를 분리 검증한다.
- 사용자 입력 키(예: `"4.2"`, `"9.10"`) 재사용은 검증 항목 오매핑을 유발할 수 있다.
- BIT 시험을 `UserInput(...PASSFAIL)` 수동 판정에만 의존하면 ICD 정합성이 약해진다. 가능하면 `RunMainThread` 갱신 데이터(예: `powerBit`)를 폴링해 자동 판정한다.
- BIT subtest 순서는 장비별 TPSData 라벨을 먼저 확인한다. CESU는 `1:IBIT, 2:POBIT, 3:PBIT`일 수 있고, GESU/KGPS/MFU/KDTP_2는 `1:POBIT, 2:IBIT, 3:PBIT`일 수 있다. `CheckByStringValue(task, subNo, ...)`를 공통 순서로 가정해 일괄 치환하지 말고 JSON 라벨과 1:1로 맞춘다.
- GESU처럼 legacy 코드가 `pobitBit/ibitBit/pbitBit` 모두를 `GetPowerOnBIT`로 파싱하는 경우가 있다. 분리 파서가 존재하면 `GetPOBIT/GetIBIT/GetPBIT`로 각각 전환하고, 수정 후 `(ibitBit|pbitBit) = *.GetPowerOnBIT` 잔여 패턴을 검색한다.
- `C1553B` 호출부에서 `GetPOBIT/GetIBIT/GetPBIT` CS1061이 발생하면, 메서드가 Core 소스 어딘가에 있다는 사실만으로 해결됐다고 보지 않는다. 실제 receiver 타입(`C1553B` vs `C1553B1`)을 확인한 뒤, 우선 `references/ateswlib-core-bit-parser-preferred-path.md`에 따라 Core parser 파일(`Core/Data/KGPS_2/1553BICD.cs` 또는 `Core/Data/KCPS_2/1553BICD.cs`)에 구현하고 Core.dll을 재빌드한다. project-local `C1553BBitExtensions.cs` shim은 사용자가 명시적으로 임시 우회를 허용한 경우에만 fallback으로 사용한다.
- 사용자가 "공통이라 Core 있는 함수로 대체"라고 정정하면 즉시 Core preferred path로 전환한다. 기존 shim 파일을 삭제하고 `.csproj` include를 제거하되, `.csproj`는 BOM/CRLF 보존 byte-level 편집을 우선해 인접 `AssemblyInfo.cs`나 첫 Task include 라인을 잃지 않게 한다. 이후 Core/K2/AteMgr 빌드까지 실제 수행한다.
- DevLib 공통 helper에서 `Thread.Sleep` 같은 BCL API가 `DevLib.Thread` 등 내부 namespace와 충돌할 수 있다. 이런 경우 using 조정만으로 끝내지 말고 `global::System.Threading.Thread.Sleep(...)`처럼 fully qualified BCL 경로를 사용해 재빌드한다.
- DevLib 임시 smoke project 생성 시 `dotnet new console` 뒤 임의의 두 번째 `.csproj`를 같은 폴더에 만들면 `dotnet run`이 “둘 이상의 프로젝트 파일” 오류로 실패한다. 생성된 csproj를 덮어쓰거나 `dotnet run --project <csproj>`를 명시한다.
- TIU_2 BIT(Task08)에서는 `IBITRequest`를 전원 인가 직후 바로 보내지 말고, 초기화 대기(기본 30초) 후 송신한다.
- TIU_2 BIT(Task08)에서는 `IBIT/CBIT/CBITDetail` 각각에 대해 `CommSend` 다음 `CommReceive`를 1:1로 연결해 응답 존재를 검증한다. 하나라도 미수신이면 즉시 불량 처리 후 종료한다.
- TIU_2 BIT(Task08)의 최종 판정은 수동 `UserInput(...PASSFAIL)`보다 ICD 기반 자동 판정을 우선한다. `StTermalResponse.GetTermalResponse`로 파싱해 `pbitresult == 0`, `cbitresult == 0`, detail 응답 유효성을 모두 만족할 때만 양호 처리한다.
- KDTP_2 BIT(Task11)에서는 PO-BIT 수신 데이터를 P-BIT 판정에 재사용하지 않는다. P-BIT는 별도 `receiveP_BIT` 버퍼로 독립 수신하고 `GetP_BIT_Report`로 판정한다.
- BIT 수신 루프는 장비 미응답 시 무한 대기하지 않도록 클래스 레벨 timeout helper로 감싼다. 구형 C# 설정을 고려해 로컬 함수보다 `private` 메서드를 우선한다.
- ATESWLIB BIT 파서에서 사용자가 `inputData[0] >> 7` 같은 시프트식을 질문하면, 먼저 "ICD 1-based bit 번호"인지 "C/C# zero-based bit index"인지 구분해 답한다. Core `GetPOBIT/GetIBIT/GetPBIT` helper가 ICD bitNo `1..9`를 받는 경로라면 `bitNo - 1`이 맞다. 예: ICD bit7은 `>> 6`, C/C# index bit7은 `>> 7`. 자세한 재검증 절차는 `references/ateswlib-bit-icd-reverification.md`와 `references/ateswlib-legacy-gps-cps-bit-crosscheck.md`를 따른다.
- CESU BIT 구현 시 ICD 비트 판정 규칙을 혼동하지 말 것(전차장 조준경 1형/2형 ICD 기준):
  - PowerBIT: 1번 비트(bit[0])는 완료 플래그이므로 `1`이어야 정상, 2~9번 비트(bit[1..8])는 고장정보이므로 모두 `0`이어야 정상.
  - IBIT: 1번 비트(bit[0])는 완료 플래그이므로 `1`이어야 정상, 2~9번 비트(bit[1..8])는 고장정보이므로 모두 `0`이어야 정상.
  - PBIT: 1~9번 비트(bit[0..8])가 모두 `0`이어야 정상.
- 변수명과 프레임 의미가 어긋나면 판정 오류를 부른다. 예: `(4,4,1)` PowerBIT 프레임을 `cbitBit`처럼 저장하면 유지보수자가 CBIT로 오해하기 쉽다. 수신 프레임명과 판정 배열명을 일치시켜라(`powerBitStatus/ibitStatus/pbitStatus`).
- 프로세스 종료 식별자(`NameOFDTPFrame`, `PathDTPFrameexe`, `NAMEOFDTP`) 혼용 시 잔존 프로세스 리스크가 크다.
- 분석만 요청받아도 최종 보고는 실행 경로 기준으로 “실행됨/미실행 가능성”을 분리해 전달한다.
- 사용자가 "분석해"라고 요청한 턴에서는 이전 세션 요약 복기만으로 답하지 말고, 최소 1회 실측(예: 기준선 빌드 또는 대상 파일 재독) 결과를 포함해 현재 상태를 재확인한다.
- LAND8R/LAND8116에서 빌드 성공 후 `BIN` 실행이 실패하거나 기준 배포 폴더와 비교하라는 요청이 오면 `references/land8r-bin-runtime-baseline-compare.md`를 적용한다. `Debug\\LAND8116.exe` 존재와 `BIN\\LAND8116.exe` 존재를 분리하고, INI 파일은 줄바꿈 차이를 정규화해 실제 설정값 차이만 보고한다.
- LAND8R/LAND8116에서 `.sln`이 자꾸 닫히거나 Visual Studio가 크래시되면 `references/land8r-rc-resource-and-vs-cache-recovery.md`를 적용한다. 먼저 MSBuild로 프로젝트 빌드 건강성을 분리 확인하고, `.rc`가 truncate/minimal 상태인지 비교한 뒤, `devenv.exe` APPCRASH는 `.vs`/ComponentModelCache/SafeMode 순서로 검증한다.

## Verification reporting template
- `Jangli : 빌드 검증 결과: 성공/실패`
- `Jangli : 대상: <sln/csproj>, 구성: <Debug|x86 등>`
- `Jangli : 핵심 로그: <첫 에러 또는 성공 근거>`
- `Jangli : 영향 범위: <태스크/뷰모델/장비연동>`

## References
- `references/msbuild-gitbash-and-dual-sln-check.md` : Git-Bash MSBuild 실행 안전패턴과 K2/AteMgr 이중 솔루션 빌드 보고 기준.
- `references/pdf-docx-clean-mapping.md` : PDF↔DOCX 비교 시 OOXML 태그 노이즈를 배제하고 clean context 기반 1:1 매핑 엑셀을 만드는 절차.
- `references/cesu-bit-icd-bit-criteria.md` : CESU BIT(PowerBIT/IBIT/PBIT) ICD 비트 판정 기준과 네이밍/매핑 주의사항.
- `references/kcps-bit-rollout-checklist.md` : PA/CESU에서 확정한 BIT 변경을 KCPS_1/KCPS_2 sibling에 동일 전개할 때의 코드·csproj·JSON·빌드 동기화 체크리스트.
- `references/kgps-task-renumbering-check.md` : KGPS 계열에서 시험 번호 재배치(예: 38→37) 시 번호-메서드-입력키-AddTask-파일명 정합 확인 순서.
- `references/mfu-bit-task-mapping.md` : CESU/GESU/MFU sibling 간 BIT 시험 Task 번호 차이(Task07 vs Task10) 확인 절차와 자동판정 전개 체크리스트.
- `references/tiu2-bit-test-addition-checklist.md` : TIU_2에 BIT 시험(Task08) 신규 추가 시 AddTask/csproj/TPSData/빌드까지 한 번에 맞추는 체크리스트.
- `references/kdtp-tiu-bit-build-stabilization.md` : KDTP_2 Task11 P-BIT 독립 수신, TIU_2 ICD 자동판정, KGPS/MFU BIT 파서 분리, K2 11-project 빌드 안정화 패턴.
- `references/ateswlib-bit-icd-reverification.md` : ATESWLIB BIT 수정 후 ICD 문서와 재대조할 때 빌드/Task 연결/ICD 자동판정 기준을 분리해 확인하는 체크리스트.
- `references/ateswlib-bit-subtest-label-reconciliation.md` : TPSData BIT subtest 라벨, `CheckByStringValue` 슬롯, POBIT/IBIT/PBIT 파서 배선을 함께 대조하는 절차.
- `references/ateswlib-lrf-and-core-reference-verification.md` : LRF/BIT 인접 변경에서 Core 파서 소스와 `BIN/TPS/Core.dll` 참조 상태가 어긋날 때의 CS1061 재검증 절차.
- `references/ateswlib-core-bit-parser-preferred-path.md` : ATESWLIB 1553B BIT 파서(`GetPOBIT/GetIBIT/GetPBIT`)는 project-local extension 파일보다 Core parser 파일(`KGPS_2/1553BICD.cs`, `KCPS_2/1553BICD.cs`)에 구현하는 것을 우선하는 사용자 교정 반영 절차.
- `references/ateswlib-legacy-gps-cps-bit-crosscheck.md` : legacy GPS/CPS `JoystickDlg.cpp::DecodeBiteInfo` 기준으로 POBIT/IBIT/PBIT 수신 버퍼와 ICD bit1=LSB 매핑을 대조하고 Core/K2/AteMgr까지 검증하는 절차.
- `references/ateswlib-bit-task-temporary-disable.md` : MFU_1/MFU_2/PA_2처럼 특정 BIT Task를 삭제하지 않고 임시 비활성화할 때 `AddTask`와 `*.csproj Compile Include`를 함께 주석 처리하고, 개별 `AnyCPU`/솔루션 `x86` 빌드를 분리 검증하는 절차.
- `references/ateswlib-c1553b-bit-extension-shim.md` : `C1553B.GetPOBIT/GetIBIT/GetPBIT` CS1061 발생 시 임시 fallback으로만 사용하는 project-local extension shim 절차. 기본 durable fix는 Core parser preferred path를 먼저 따른다.
- `references/devlib-common-library-boundary.md` : DevLib 공통 라이브러리에 프로젝트 종속 BIT/ICD/RscDo 로직을 넣지 않고, 공통 함수만 유지하며 isolated smoke project로 검증하는 절차.
- `references/devlib-arinc429-wrapper-safety.md` : DevLib ARINC429/DDC P/Invoke wrapper 수정 시 native header 대조, 반환값 보존, 배열 포인터 안전성, isolated smoke/full build 분리 검증 절차.
- `references/devlib-gui-wpf-validator-and-ccsds.md` : DevLibGUI를 WPF 공통함수 검증 앱으로 교체하거나 `DevLib\IO\CCSDS` 같은 DLL-friendly 공통 프로토콜 모듈을 추가할 때의 설계/검증/커밋 절차.
- `references/devlib-1553b-reusable-codec-extraction.md` : ATESWLIB 1553B 순수 계산/ICD/BIT/hex 변환 로직을 DevLib 재사용 모듈로 분리할 때의 책임 분리와 검증 절차.
- `references/devlib-arinc429-wrapper-verification.md` : DevLib ARINC429/DD42992 P/Invoke wrapper의 반환값, buffer safety, DLL deployment, isolated smoke 검증 절차.
- `references/devlib-arinc-protocol-helper-and-build-stabilization.md` : DevLib에 ARINC664/717/629 같은 공통 프로토콜 helper를 추가하고 외부 장비/영상/COM 의존성을 분리해 `dotnet build`와 Visual Studio MSBuild를 통과시키는 절차.
- `references/devlib-spi-i2c-common-helper-and-verification.md` : DevLib에 SPI/I2C 공통 helper를 vendor-free로 추가하고 Read.txt, dual-build, smoke test, native dependency 검색까지 검증하는 절차.
- `references/devlib-multi-protocol-reinspection-smoke.md` : DevLib에서 I2C/SPI/SpaceWire/SpaceFibre/CCSDS/CAN을 한 번에 재점검할 때 API shape, vendor boundary, dual-build, deterministic smoke, CAN hardware-risk 분리 보고까지 수행하는 절차.
- `references/devlib-vendor-reference-and-native-dll-build-stabilization.md` : DevLib에서 Advantech/FrameLink/UCAN/OpenCV 같은 vendor SDK 폴더를 복구할 때 repo 내부 DLL을 찾아 `<Reference>`와 native DLL `TargetPath` 출력 루트 복사로 빌드/런타임 의존성을 안정화하는 절차.
- `references/subagent-policy-roster-update.md` : JAN 서브에이전트 정책 추가/변경 시 정책 파일 생성과 README 인덱스 동기화를 빠짐없이 수행하는 체크리스트.
- `references/devlib-wpf-dll-reference-conversion.md` : DevLibGUI/DevLibInstrument가 DevLib 소스 링크가 아니라 빌드된 `DevLib.dll`을 직접 참조해야 할 때의 전환·검증 절차.
- `references/devlibgui-real-connection-input-validation.md` : DevLibGUI 통신 검증 화면에서 TCP/UDP/Serial/CAN/ARINC429 실제 연결 인자 입력 UI와 호출 매핑을 구현·보고하는 절차.
- `references/devlib-log-ini-store.md` : DevLib `Utiliy\\Log`에 INI 저장/읽기 기능을 추가할 때 순수 .NET 구현, UTF-8 BOM 저장, Entry round-trip smoke, 한글 표시 확인을 수행하는 절차.
## Notes
- 환경 이슈(타기팅팩 미설치 등)는 영구 제약으로 저장하지 말고, 해당 세션의 빌드 불가 원인으로만 보고한다.
- 한글 표시/인코딩 민감도가 높으므로 문자열/리소스 변경 시 인코딩 일관성 점검을 포함한다.
