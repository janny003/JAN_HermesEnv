# MFC interview final-confirmation popup pattern

Use this when a console/agent child process emits a terminal confirmation marker after the normal interview questions, and the MFC GUI must turn it into a user-facing dialog instead of leaving the user to type in an input box.

## Durable pattern

1. Treat the final confirmation marker as a distinct protocol event.
   - Example marker: `[FINAL_CONFIRM_Q]`.
   - Do not route it through the generic manual-input prompt.

2. Show a dedicated confirmation dialog with clear intent.
   - Suggested title: `최종 진단 확정`.
   - Keep this separate from earlier per-question Yes/No interview popups.

3. Map UI choices to stable machine tokens.
   - Yes / 예 -> `approved`
   - No / 아니요 -> `rejected`
   - Cancel / 취소 -> `pending`

4. Send the token to the child process stdin through the same guarded answer-writing path used by interview auto-answers.
   - Reuse `WriteAnswer(answer, &err)` if available.
   - Keep child-liveness and broken-pipe race handling from the interview stdin reliability pattern.

5. Record an explicit transcript breadcrumb.
   - Example: `[DIALOG FINAL_CONFIRM] approved`
   - This makes later review/debugging distinguish final approval from the earlier 4 interview questions.

6. Mirror paired files together in policy/worktree copies.
   - If the implementation changes both declarations and definitions (`.h` + `.cpp`), copy both to policy mirror trees before building.
   - A cpp-only mirror can fail with missing members or stale signatures, even when the main tree builds.

## Verification

- Build the active MFC solution after the change.
- Run the Python/unit test suite if the workflow has one.
- Build any policy mirror/tree that the user expects to stay in sync.
- Inspect transcript output to confirm the final confirmation line appears as `[DIALOG FINAL_CONFIRM] <token>`.
- Confirm the user no longer needs to type the final decision manually.

## Pitfalls

- Do not combine the final confirmation with the Step7/Q1~Q4 interview question loop. It is a separate terminal decision.
- Do not show a generic “send manual input?” prompt for `[FINAL_CONFIRM_Q]`; that hides the workflow state and weakens UX clarity.
- Do not mirror only the `.cpp` file when function signatures or member fields changed in the header.