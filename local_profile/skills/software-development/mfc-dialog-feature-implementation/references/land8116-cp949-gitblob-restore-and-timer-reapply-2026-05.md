# LAND8116: CP949 손상 복구 + TIMER 재적용 (2026-05)

## Trigger
- 에러가 한 번에 다발 발생: `C2059 user-defined literal`, `C2001 상수에 줄 바꿈`, `C1057 macro EOF`.
- 동시에 "`CloseTimerDialog` 중복 선언/정의" 류 오진이 섞여 나옴.

## Root Cause Pattern
1) CP949 기반 대형 파일(`LANDTestView.cpp`)에 광범위 인코딩/치환이 들어가 문자열 경계가 깨짐.
2) 그 상태에서 부분 패치를 반복하면 실제 중복 여부와 무관하게 파싱 붕괴로 중복 에러가 연쇄 표출됨.
3) `git restore`만으로 기대 상태가 안 돌아오는 경우가 있어(작업 경로/경로 지정 혼선), blob 직접 복원이 더 안전함.

## Proven Recovery Sequence
1. **HEAD blob 직접 복원** (고위험 파일 우선)
   - `LAND8116/LANDTestView.cpp`, `LAND8116/LANDTestView.h`, `LAND8116/resource.h`
   - 방식: `git show HEAD:<repo-relative-path>` 바이트를 파일로 직접 write.
2. **CP949 보존 최소 재적용**
   - 메시지맵 1줄(`ON_BN_CLICKED(IDC_Timer, &...OnBnClickedTimer)`) +
   - handler 선언/구현 최소 블록 +
   - `resource.h` 심볼 alias(`IDC_Timer`) 및 누락 리소스 심볼 보강.
3. 문자열 리터럴 재검증
   - 실제 개행이 아니라 `\n` escape인지 확인.
4. 빌드 게이트
   - Release|Win32 MSBuild 실행.
   - 첫 blocker를 즉시 해결 후 재빌드.

## Build Evidence (session)
- 초기 blocker: `LANDTestView.cpp`의 문자열 붕괴(C2001/C2059/C1057).
- 복구 후 blocker: `RC2104 undefined keyword IDC_BUTTON_PS_REFRESH`.
- `resource.h`에 `IDC_BUTTON_PS_REFRESH`, `IDC_STATIC_PS_STATUS` 보강 후 **오류 0 빌드 성공**.

## Guardrails
- CP949 대형 파일에는 범위 치환/일괄 인코딩 변환 금지.
- 실패 시 먼저 원복, 그다음 최소 수정 + 즉시 빌드(한 번에 하나).
- "중복 정의" 에러를 곧바로 구조 문제로 단정하지 말고, 선행 문자열/매크로 붕괴 여부부터 확인.