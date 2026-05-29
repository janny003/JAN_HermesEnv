# SRU 후보 라벨 파이프라인 (소스 규칙 추출 + 로그 매칭 + multi-label)

## 언제 사용
- C++ 소스에서 SKIP/배제 규칙을 근거로 추출해 로그 라벨링에 연결할 때
- JAN LOG 파일명 기반으로 SRU 후보 라벨을 빠르게 자동 생성할 때

## 구현 포인트
1. 소스 규칙 추출
   - `ImportDlg.cpp`에서 아래 2개 규칙을 우선 추출
     - `rm_ate_gettestloginfo(...)` 결과 존재 시 `m_pcheck = "SKIP"` (중복 로그 배제)
     - `rm_ate_getequipinfo(...)` 결과 없음 시 `m_pcheck = "SKIP"` (장비 미일치 배제)
2. 로그 매칭
   - `C:\Users\yjs\Desktop\JAN\LOG`의 `*.TXT`를 순회
   - 파일명에서 `pass/fail` 추출, 모듈 폴더명과 결합
3. SRU 후보 라벨 생성
   - 키워드 사전 기반 multi-label 부여 (주파수/이더넷/PPS/전원/부팅/CRC 등)
4. 분류기
   - LightGBM/CatBoost가 있으면 해당 backend 메타데이터 기록
   - 패키지 없을 때도 `keyword_baseline`으로 예측 CSV를 반드시 생성

## 실행 예시
- `python tools/sru_multilabel_pipeline.py --source-root /c/Users/yjs/Desktop/JAN/ATESWR-25KA4/UAV_MAIN/UAV_MAIN/Dialog --log-root /c/Users/yjs/Desktop/JAN/LOG --out-dir out/sru_multilabel_short_term`

## 산출물
- `fault_exclusion_rules.json`: 소스 근거(파일/라인/스니펫)
- `log_rule_sru_match.csv`: 로그별 true/pred 라벨, fail candidate
- `sru_multilabel_model.json`: backend 및 라벨 통계
- `sru_multilabel_predictions.csv`: 최종 multi-label 예측

## 주의
- 파일명 라벨은 노이즈가 크므로 운영 전 SRU 코드 매핑 테이블을 별도로 검수한다.
- fallback 모드여도 산출물 형식을 동일하게 유지해 MFC/후속 파이프라인과 호환시킨다.
