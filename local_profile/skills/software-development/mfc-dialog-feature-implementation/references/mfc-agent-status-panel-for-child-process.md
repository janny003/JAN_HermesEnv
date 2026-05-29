# MFC child-process agent status panel pattern

Use this when an MFC dialog launches an external agent/process and the user needs visible progress instead of only transcript text.

## Problem signal
- GUI has transcript/output, but user cannot tell whether the agent is idle, running, waiting for Yes/No input, sending an answer, confirming final diagnosis, completed, or errored.
- Interview-style protocols emit markers such as `[RUN]`, `[INTERVIEW_Qn]`, `[FINAL_CONFIRM_Q]` and the dialog already reads stdout asynchronously.

## Implementation pattern
1. Add a small read-only status area between the initial context/input region and the transcript/log region.
   - Prefer a calm label such as `Agent Status` plus a single dynamic `CStatic` value.
   - Keep it visually stable and avoid moving existing answer/send controls unless necessary.
2. Add one helper method such as `SetAgentStatus(const CString& status)` so every state transition uses one path.
3. Update status at lifecycle boundaries:
   - startup: `대기 중` / idle
   - log loaded: `로그 선택됨`
   - start clicked/process creation: `시작 중`
   - stdout processing: `실행 중`
   - `[RUN]` or file/log checking: `확인 중`
   - `[INTERVIEW_Qn]` parsed or Yes/No popup shown: `입력 대기`
   - `[FINAL_CONFIRM_Q]`: `최종확정 대기`
   - Send/auto-answer write: `답변 전송 중`
   - normal process exit/pipe EOF: `완료`
   - CreateProcess/pipe/write failure or non-zero exit: `오류`
4. Keep status updates next to the code that detects the event, not in a separate timer-only inference layer. This makes the UI reflect the protocol boundary accurately.
5. When the dialog has async stdout + modal MessageBox prompts, update to `입력 대기` before showing the popup and `답변 전송 중` immediately before guarded stdin write.

## Static test recipe
For brownfield MFC projects where UI automation is heavy, add lightweight source-level tests first:
- `resource.h` contains the new status control IDs.
- `.rc` contains the `Agent Status` label/static controls in the expected dialog block.
- header declares the `CStatic` member and `SetAgentStatus` helper.
- cpp calls `SetAgentStatus` on the major lifecycle/protocol branches.

Then run full Python tests plus MSBuild and, when possible, launch the built `.exe` and confirm process-alive evidence.

## Verification checklist
- Static tests fail before implementation and pass after implementation.
- `python -m pytest -q` remains green.
- MSBuild succeeds with 0 errors.
- Built exe launches.
- Manual visual check: status panel appears above transcript and changes after Start / interview markers / completion.

## Pitfalls
- Do not make the transcript itself the only status signal; users can miss state transitions in long logs.
- Do not overload answer text boxes or buttons as status indicators; a dedicated static label is clearer and less risky.
- In CP949/MBCS projects, prefer ASCII labels for newly added fixed UI text if Korean rendering risk is high, or verify Korean captions after build/run.