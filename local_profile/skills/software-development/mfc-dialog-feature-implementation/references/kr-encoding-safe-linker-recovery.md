# KR 인코딩 민감 MFC 파일에서 링크 에러 안전 복구 패턴

상황:
- `LANDTestView.cpp` 같은 CP949/혼합 인코딩 대형 파일에서 직접 문자열/함수 패치 시
  - `C2001: 상수에 줄 바꿈 문자가 있습니다`
  - `C1057: 매크로 확장에서 예기치 않은 파일의 끝`
  - `C2059: user-defined literal` 연쇄 발생 가능.

안전 복구 순서:
1. 깨진 파일은 먼저 원복(`git checkout -- <file>`)해 컴파일 문법 붕괴를 제거.
2. 누락 심볼이 있으면 원본 대형 파일을 다시 크게 건드리지 말고, 새 `.cpp`에 함수 정의를 분리 추가.
   - 예: `LANDTestView_PowerSupplyStatus.cpp`에 `RefreshPowerSupplyStatus`/`UpdatePowerSupplyStatus` 구현.
3. `.vcxproj`에 새 `.cpp`를 `<ClCompile Include="..." />`로 등록.
4. 중복 정의 발생 시(예: `LNK2005`) 기존 정의가 있는 함수는 분리 파일에서 제거.
5. 매 수정마다 즉시 빌드하고, 실패 시 첫 blocking 심볼/파일:라인부터 보고.
6. 빌드 성공 후 실행 검증(프로세스 실행 확인 + 종료 정리)까지 수행.

체크포인트:
- 링크 에러(`LNK2019`) 해결 과정에서 컴파일 에러(`C2001`)를 재도입하지 않는 것이 우선.
- 인코딩 민감 파일 직접 편집은 최소화하고, sidecar `.cpp` 전략을 우선 고려.