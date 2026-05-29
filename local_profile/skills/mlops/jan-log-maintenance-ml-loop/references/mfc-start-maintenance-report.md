# MFC Start -> 정비 Word 보고서 모드 운영 메모

## 목적
Start 버튼 1회로 전체 로그를 읽고 기존 모델(IF + XGB)로 추론하여 Word 보고서를 생성한다.

## 기본 커맨드 규칙
- `CreateProcessW`에서 PATH 의존을 피하기 위해 **절대 경로 python.exe**를 사용한다.
- 경로 인자는 모두 큰따옴표로 감싼다.

예시:
"C:\Users\yjs\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" "C:\Users\yjs\Desktop\JAN\OrobrosTest\tools\generate_maintenance_report.py" --project-root "C:\Users\yjs\Desktop\JAN\OrobrosTest" --log-root "C:\Users\yjs\Desktop\JAN\LOG" --out-doc "C:\Users\yjs\Desktop\JAN\Policy\Data\JAN_maintenance_report.docx"

## 종료 처리 규칙
- pipe close 직후 `GetExitCodeProcess`만 읽으면 `259(STILL_ACTIVE)`가 찍힐 수 있다.
- `WaitForSingleObject` 후 exit code를 읽고, 259는 미확정으로 취급한다.

## CSV 후처리와 보고서 모드 분리
- 보고서 모드에서는 CSV 계약(`CSV_START/CSV_END`)이 없으므로 CSV 저장 후처리를 강제하면 안 된다.
- `m_capturedOutput`에 CSV 마커가 있을 때만 CSV 후처리를 수행한다.

## 본문 수치 피처 추출(파일명 기반 금지)
- 파일명 토큰만으로 피처를 만들면 원인분류가 `normal`로 쏠리기 쉽다.
- 로그 본문에서 수치와 판정횟수를 추출한다.

추출 패턴:
- `Meas[...]`, `Min[...]`, `Max[...]` 수치
- `=>Failed`, `=>Passed` 라인 수
- `retry/재시도`, `crc/cable/케이블/ethernet` 키워드 빈도

모델 입력 매핑(6개):
- voltage: 측정값 평균(없으면 5V/12V 추정)
- current: 초기 측정값 절대평균 스케일
- response_time_ms: min/max/meas margin 기반 근사(없으면 retry 기반 대체)
- fail_count: Failed 라인 수(없으면 파일명 fail fallback)
- crc_error_rate: crc 관련 카운트 / (failed+passed)
- retry_count: retry 카운트

## FAIL 후보 선정 이유 표기
리포트에 FAIL 후보 표를 별도 섹션으로 두고 이유를 함께 기록:
- 본문 Failed N회
- 파일명에 FAIL 포함
- 이상탐지 점수<0
- retry 키워드 N회

## 문서 저장 주의
- 대상 .docx가 Word에서 열려 있으면 PermissionError로 저장 실패 가능.
- 실행 전 대상 문서를 닫고 재시도한다.
