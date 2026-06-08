# PDF↔DOCX 1:1 매핑(사람이 읽을 수 있는 형태) 체크리스트

목적: JAN 문서 비교에서 OOXML 내부 태그(`w:rsidR`, `w:fldChar`, `w:webHidden` 등) 노이즈를 제거하고, 사용자가 바로 판단 가능한 문장 컨텍스트 기준으로 변경점을 제시한다.

## 왜 필요한가
- `word/document.xml` 원문 비교는 내부 제어 태그가 많아 수정 의도를 파악하기 어렵다.
- 사용자 요구는 "무엇이 바뀌었는지"이므로, 최종 산출물은 문장/문단 맥락 중심이어야 한다.

## 권장 추출 방식
1. DOCX: `python-docx`의 `Document(...).paragraphs`로 텍스트 추출
2. PDF: PyMuPDF(`fitz`)로 페이지 텍스트 추출
3. 공통 정규화: 공백 정리(`\s+ -> single space`), 너무 짧은 라인 제외

## 1:1 매핑 규칙
1. 문서쌍은 코드 기준으로 고정 매칭: `SDD/SPS/SRS/STD/STR`
2. ID 패턴 중심으로 인덱싱
   - 예: `T-ATE-SFR-###`, `CSCI-REQ-####`, `RQ-####`, `1.2.3` 계층 번호
3. 상태 분류
   - `same_or_near`: 유사도 임계치 이상
   - `changed`: 같은 ID인데 문맥 차이 존재
   - `added_in_docx`: DOCX에만 존재
   - `missing_in_docx`: PDF에만 존재
4. 각 행에는 반드시 `pdf_context(clean)`와 `docx_context(clean)`를 함께 넣는다.

## 산출물 형식(필수)
- `pdf_docx_1to1_mapping_clean.xlsx`
  - `summary_clean` 시트: 문서쌍별 집계(common/same/changed/added/missing)
  - 코드별 시트(`SDD`, `SPS`, `SRS`, `STD`, `STR`): ID 단위 상세행

## Pitfall
- XML 원문(`<w:r ...>`)을 그대로 결과에 넣지 말 것. 사용자는 수정 포인트를 읽을 수 없다.
- 날짜/버전 숫자를 ID로 과도 매칭하면 잡음이 증가한다. ID 패턴은 요구사항/시험항목 중심으로 좁힌다.
- 대용량 문서는 전체 문자열 LCS보다 "ID+근접 컨텍스트" 매핑이 훨씬 안정적이다.
