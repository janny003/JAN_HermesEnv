# MFC Pipeline-only GUI shell runner pattern

Use this when a legacy MFC dialog app should keep its proven GUI shell but switch from a hybrid/agent workflow to a pure pipeline workflow.

## Trigger
- User asks to keep the existing GUI frame/layout but implement a pipeline program.
- Existing app already has command/context/transcript/status controls and child-process pipe handling.
- The old default command points to an agent/review/interview runner, but the new variant should run without review, interview, or final-confirmation gates.

## Implementation pattern
1. Keep the MFC dialog/resource structure intact first.
   - Do not redesign the GUI before the runner path is stable.
   - Preserve Start/Stop/Send/log-load/transcript/status/ListView controls if they already work.
2. Add a thin pipeline runner, for example `tools/pipeline_only_runner.py`.
   - It should call the existing core report/pipeline script.
   - It should emit simple status markers such as `[PIPELINE] state | detail` so the existing transcript/status parser can display progress.
   - It should not emit `[INTERVIEW_Qn]` or `[FINAL_CONFIRM_Q]` unless the pipeline-only product explicitly requires operator gates.
3. Repoint `DefaultMaintenanceCommand()` to the new runner and the correct project root.
   - Remove obsolete review-output args such as `--review-out-dir` from the default command.
   - Use output names that identify the variant, e.g. `JAN_pipeline_only_report_ui.docx`.
4. Update command self-healing.
   - Change the validation token from the old hybrid script name to the new runner name.
   - If the command edit box contains stale text, restore the pipeline-only default before applying `--focus-log`.
5. Keep old parser branches harmless.
   - It is acceptable for old `[AGENT]`, `[INTERVIEW_Q]`, or `[FINAL_CONFIRM_Q]` handling code to remain if default execution cannot reach it.
   - Ensure `[PIPELINE]` updates the current displayed role/name to something like `Pipeline Core`.
6. If trained model artifacts are not present and the user prefers a short-term realistic baseline, provide a deterministic baseline fallback.
   - Record the model mode in JSON, for example `model_paths.mode = deterministic_baseline`.
   - Do not make missing model artifacts block GUI smoke testing unless the task explicitly requires trained-model-only behavior.
7. Normalize GUI close semantics for tool-runner logs.
   - MFC modal dialogs closed via X/Cancel can surface `IDCANCEL`/exit code 2 in background-process logs, even when the GUI closed normally.
   - If that creates false error reports in the agent runner, force clean process status after normal `DoModal()` return, e.g. call `::ExitProcess(0);` after the modal dialog closes.

## Verification checklist
- Static tests assert the default GUI command points to the pipeline-only runner and no review args remain.
- Static tests assert the runner contains `[PIPELINE]` markers and does not contain interview/final-confirmation markers.
- Direct CLI smoke run produces non-empty `.docx` and `.json` outputs.
- JSON output confirms the expected model mode, especially when using deterministic fallback.
- MFC Debug x64 build succeeds with 0 errors.
- Launch the built exe, confirm the process starts, then close it and confirm normal close is not reported as a pipeline failure.

## Pitfalls
- A cloned hybrid repository may still contain the old project/exe name. Do not confuse executable naming with runner behavior; first verify the default command and output paths.
- Updating the runner without changing the command self-healing token can silently restore the old hybrid command after log selection.
- Treat exit code 2 after closing a modal MFC dialog as a possible GUI-close status, not immediate evidence that the pipeline failed. Check whether output files were generated and whether the process was simply closed by the user.
- Do not record missing local model artifacts as a permanent environment limitation. Capture the fallback pattern instead.
