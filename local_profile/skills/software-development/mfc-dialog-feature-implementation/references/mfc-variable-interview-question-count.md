# MFC interview dialogs with variable question counts

Use this when a Python/CLI review loop emits `[INTERVIEW_Qn]` markers and the MFC GUI auto-opens Yes/No dialogs and writes answers to child stdin.

## Durable lesson
Do not hard-code the GUI and persistence path to exactly four interview questions when upstream requirements can expand from a single focus item to Top-N candidates.

A robust flow should preserve one protocol rule instead:

- each emitted marker `[INTERVIEW_Qn]` produces exactly one Yes/No dialog;
- question numbers are parsed as integers, not a single digit range;
- all generated questions and answers are collected and persisted without slicing.

## Python-side pattern
When generating Top3 candidate questions:

1. Sort `fail_candidates` by risk descending.
2. Take at most the top 3.
3. Emit two closed Yes/No questions per candidate:
   - one for the candidate-specific fault-exclusion/check item;
   - one for main-equipment / same-condition retest / maintenance-history confirmation.
4. Keep each question ending with `(Yes/No)` so the MFC dialog can map buttons safely.

Avoid:

```python
for i, q in enumerate(questions[:4], 1): ...
record = {"questions": questions[:4], "answers": answers[:4]}
```

Prefer:

```python
for i, q in enumerate(questions, 1):
    print(f"[INTERVIEW_Q{i}] {q}", flush=True)
    user_input = input()
    answers.append(normalize_yes_no(user_input))

record = {"questions": questions, "answers": answers}
```

Also remove `[:4]` from final-diagnosis payload fields such as `step7_questions` and `step7_answers`.

## MFC-side parsing pattern
The GUI should parse `[INTERVIEW_Q` markers in a loop, then parse the full integer before `]`.

Core idea:

```cpp
while (true) {
    int marker = trimmed.Find(L"[INTERVIEW_Q", scanPos);
    if (marker < 0) break;

    int qNumPos = marker + static_cast<int>(wcslen(L"[INTERVIEW_Q"));
    int closeBracket = trimmed.Find(L"]", qNumPos);
    if (closeBracket < 0) break;

    CString qNumText = trimmed.Mid(qNumPos, closeBracket - qNumPos);
    qNumText.Trim();
    int qNum = _wtoi(qNumText);
    if (qNum <= 0 || qNum <= m_interviewQuestionCount) {
        scanPos = closeBracket + 1;
        continue;
    }

    // extract the current line, show one MessageBox, write one answer
    m_interviewQuestionCount = qNum;
    qGuide.Format(L"\r\n\r\n[질문 %d] 예=\"예\", 아니요=\"아니요\"를 전송합니다.", qNum);
}
```

Avoid:

```cpp
while (m_interviewQuestionCount < 4) { ... }
if (ch < L'1' || ch > L'4') continue;
qGuide.Format(L"[질문 %d/4] ...");
```

Those patterns silently drop `[INTERVIEW_Q5]`, `[INTERVIEW_Q6]`, or two-digit markers.

## TDD regression shape
Add tests before changing production code:

1. `build_interview` returns 6 questions for Top3 × 2 and excludes lower-risk candidates.
2. `_collect_interview_answers` prints/collects all generated markers, not just four.
3. Persistence/final payload preserve all Step7 questions and answers without truncation.
4. Full Python suite passes.
5. MFC solution builds cleanly after marker parser changes.

## Verification evidence to report
- RED: new tests fail because legacy code emits/collects/persists only 4 items.
- GREEN: targeted tests pass.
- Regression: full `pytest` passes.
- GUI compile: MSBuild succeeds with 0 errors and 0 warnings.
