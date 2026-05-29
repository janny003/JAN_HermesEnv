# JAN-style Two-Pass Review Notes (Reusable)

## Trigger pattern
Use when user asks for: final manuscript review, citation validity check, or "꼼꼼히" verification.

## Pass 1 (logic pass)
1. Confirm claim boundary:
   - RAG as status-inference engine
   - PMF-Agent as operational safety/governance framework
2. Ensure no unsupported automation claim.
3. Check section continuity from methods -> results -> interpretation -> limits.

## Pass 2 (integrity pass)
1. Metric consistency matrix:
   - Abstract Results
   - Main result table(s)
   - Results text
   - Conclusion summary
2. Citation grounding matrix:
   - For each high-impact claim, list citation and source type (paper/standard/gov guide).
   - Flag bibliography-only entries (not cited in body).
3. Figure/table/equation integrity:
   - Numbering continuity
   - In-text first mention before display object
   - Equation variable definitions immediately after equation

## Fast insertion templates

### A) Protocol separation sentence
"본 연구는 상태 판정 평가와 원인/조치 추천 평가를 서로 다른 실험 조건으로 분리하여 보고하며, 각 결과는 동일 표에서 병합 해석하지 않는다."

### B) Governance gate justification sentence
"고위험 조치의 경우 모델 점수와 독립된 승인·차단 규칙을 적용하여 안전성 및 책임성을 확보한다."

### C) Citation caveat sentence
"해당 결과는 본 파일럿의 라벨 체계와 데이터 조건에서 관찰된 범위로 해석되어야 한다."
