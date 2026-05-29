# DOCX 최종제출형(양식 유지) 패턴

## 언제 쓰는가
- 기존 논문/보고서 템플릿의 폰트, 크기, 문단 스타일을 반드시 유지해야 할 때
- 내용은 대폭 갱신해야 하지만 레이아웃/스타일은 변경하면 안 될 때

## 안전한 수정 방식
1. `Document(template_path)`로 기존 파일을 연다.
2. 기존 문단 수를 먼저 확인한다: `len(doc.paragraphs)`.
3. 신규 본문은 문단 단위 리스트로 준비한다.
4. `for i, p in enumerate(doc.paragraphs): p.text = new_lines[i]` 방식으로 **기존 문단 텍스트만 치환**한다.
5. `len(new_lines) > len(doc.paragraphs)`이면:
   - 새 문단 삽입을 먼저 시도하지 말고,
   - 문단 압축/통합 또는 장별 핵심문장 재매핑으로 길이를 맞춘다.
6. 저장 후 문단/장 번호/참고문헌 위치를 샘플 검증한다.

## 이번 세션에서 확인된 실패 패턴
- bash heredoc 긴 본문에서 quote mismatch로 `unexpected EOF` 발생
- 문단 객체를 파일 핸들처럼 잘못 넘겨 `AttributeError: 'Paragraph' object has no attribute 'write'`
- 신규 문단 수가 기존보다 많아 `AssertionError (new_lines, paragraphs)` 유발

## 권장 가드
- 본문 치환 스크립트에 사전 검증 추가:
  - paragraph count check
  - 섹션 키워드(예: 7.1~7.4, 참고문헌) 포함 여부 check
- 최종본 파일명은 버전 suffix(v6/v7 등)로 저장하고, 마지막에 1개 파일로 확정 공지한다.
