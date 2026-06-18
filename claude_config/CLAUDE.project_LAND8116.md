# LAND8116 프로젝트 설정

## 프로젝트 개요
- **프로젝트명**: LAND8116 (HUMS 시험장비 관리 시스템)
- **기술스택**: C++/MFC, Visual Studio 2010 호환
- **파일 인코딩**: cp949 (EUC-KR) — S01_LK_POWERSUPPLY.cpp만 UTF-16LE
- **줄바꿈**: CRLF

## 워크스페이스
`/Users/jaeinyi/Documents/WorkSpace/LAND8R-24HS4_202606181008/`

## 핵심 파일
- `LAND8116/Define.h` — 전체 구조체 정의
- `LAND8116/LANDTestView.cpp/.h` — 시험 항목 트리, 자체진단
- `LAND8116/LANDEQManageView.cpp` — 계측기 관리
- `LAND8116/LANDConfigureView.cpp/.h` — 환경설정 UI
- `LAND8116/S01_LK_POWERSUPPLY.cpp` — 전원공급 자체진단
- `BIN/Config/Program.ini` — 시험 항목별 전원 설정

## 파일 수정 규칙
- cp949 파일은 Python `decode('cp949')` / `encode('cp949')` 사용
- S01_LK_POWERSUPPLY.cpp는 `decode('utf-16')` / `encode('utf-16')` 사용
- Edit 도구 직접 사용 시 인코딩 불일치 주의

## 서브에이전트 역할 (상위 CLAUDE.md 참조)
글로벌 JAN 서브에이전트 설정 적용 중.
코드 수정은 Jangli 규칙 준수 필수.
