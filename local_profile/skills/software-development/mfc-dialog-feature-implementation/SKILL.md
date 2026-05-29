---
name: mfc-dialog-feature-implementation
description: Use when adding or modifying GUI features in legacy MFC dialog-based apps (buttons, popup dialogs, timers, list outputs) with minimal risk to existing screens.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mfc, win32, gui, dialog, timer, legacy-modernization]
    related_skills: [systematic-debugging, requesting-code-review]
---

# Implementing Features in Legacy MFC Dialog Apps

## Overview
This skill covers safe feature delivery in older MFC projects where UI is often hard-coded in `OnInitDialog`, resources can be incomplete, and message-map wiring is brittle.

It emphasizes pragmatic implementation: add functionality without destabilizing existing screens, and prefer runtime-created controls/dialogs when `.rc` resources are missing or unreliable.

## When to Use
- Adding a new button/action to an existing MFC dialog screen.
- Adding a small utility dialog (timer, helper tool, status window).
- Wiring timer-driven UI updates (e.g., stopwatch/progress refresh).
- Working in projects with partial/broken resource setup (`resource.h` present but `.rc` unavailable).

Do not use for:
- Full UI redesigns (requires broader architecture/UX plan).
- Migration from MFC to Qt/WPF/web.

## Workflow
1) Discover real UI integration points
- Identify the active screen class (`*MainView`, `*TestView`, etc.).
- Find `DoDataExchange`, `BEGIN_MESSAGE_MAP`, and `OnInitDialog` in that class.
- Confirm project wiring in `.vcxproj` (`ClInclude`, `ClCompile`, `ResourceCompile`).

2) Choose implementation style
- Preferred when resources are unstable/missing: runtime UI creation (`Create`/`CreateEx`) in `OnInitDialog`.
- If resources are healthy: define dialog/control in `.rc` + `resource.h` and bind with DDX/message map.

3) Add control IDs safely
- Add new IDs in `resource.h` with unique numeric values.
- Bump `_APS_NEXT_CONTROL_VALUE` to avoid future collisions.

4) Wire handlers and state
- Add handler declarations in header.
- Add `ON_BN_CLICKED(...)` / related macros in message map.
- Initialize ownership pointers to `NULL` in constructor.
- Clean up in `OnDestroy` (`DestroyWindow` + `delete` + nulling).

5) For timer-based tools (stopwatch pattern)
- Use `SetTimer` on start, `KillTimer` on stop/reset/destroy.
- Keep elapsed state split into:
  - accumulated elapsed before current run
  - current run start tick
- On stop, append formatted elapsed value to list control.

6) Register build inputs
- Add new `.h/.cpp` to `.vcxproj` if project does not auto-include.
- Verify message-map symbol and control ID compile correctly.

6.5) ResourceCompile sanity check (critical in brownfield MFC)
- Inspect `.vcxproj` for `<ResourceCompile Include="...">` and `<UserProperties RESOURCE_FILE="...">`.
- If build fails with `RC1110: could not open <name>.rc`, confirm whether the file actually exists on disk.
- If `.rc` is missing but `resource.h` + `res/*.ico|*.bmp` exist, restore a **minimal** `.rc` first (icons/toolbar/doc icon) so ResourceCompile can run.
- Rebuild immediately to reveal second-order resource path errors (`RC2135 file not found`).
- If relative paths keep failing due RC working-directory ambiguity, temporarily use absolute resource paths to unblock build verification, then optionally normalize paths in a cleanup pass.

7) Policy-gated repos (important)
- If the repo has a policy folder (e.g., `C:/Users/<user>/Desktop/JAN/Policy/*.md`), read relevant policy files before final edits.
- For user-requested subagent governance, run a subagent pass to check policy compliance and regression risk before finalizing.
- Apply policy findings as concrete code changes (not just notes).

## Stopwatch Reference Pattern
- UI elements:
  - time display (`CStatic`)
  - start/stop/reset buttons (`CButton`)
  - stop-time history list (`CListBox`)
- Data model:
  - `bool isRunning`
  - `ULONGLONG startTick`
  - `ULONGLONG elapsedBeforeStart`
- Formatting: `hh:mm:ss.mmm`

See session example: `references/stopwatch-runtime-dialog-pattern.md`
Policy + stability addendum: `references/jan-policy-and-stopwatch-safety.md`
Resource compile recovery: `references/resourcecompile-rc1110-recovery.md`
KR 인코딩 민감 파일의 링크 에러 안전 복구: `references/kr-encoding-safe-linker-recovery.md`
GUI 이미지 로드 전수점검 + 한글 파일명 리스크 대응: `references/gui-image-load-audit-kr-encoding.md`
LAND8116 수동 스탑워치 통합 인코딩 가드레일: `references/land8116-stopwatch-integration-encoding-guardrails.md`
메인화면 좌상단 검은 사각형(자산 원인) 트리아지: `references/mainview-black-rectangle-background-asset.md`
LAND8116 HUMS 항목 누락 + CP949 안전 1줄 수정 패턴: `references/land8116-hums-visibility-and-cp949-safe-edit.md`
LAND8116 타이머/전원 연동 재시도 가드레일(2026-05): `references/land8116-timer-ps-retry-guardrails-2026-05.md`
LAND8116 전원공급기 GUI 제어 불능 디버깅(2026-05): `references/land8116-powersupply-gui-control-debugging-2026-05.md`
LAND8116 GUI 전부 무반응 트리아지(2026-05): `references/land8116-gui-total-nonresponse-triage-2026-05.md`
LAND8116 RC-only 버튼 가시화 + 작업표시줄 아이콘 보강 패턴: `references/land8116-rc-only-visibility-and-taskbar-icon.md`
LAND8116 타이머 미표시/무반응 ID alias 트랩 대응: `references/land8116-timer-dialog-not-opening-id-alias.md`
LAND8116 인코딩 일괄 변환 회귀 복구(2026-05): `references/land8116-encoding-mass-conversion-regression-and-recovery-2026-05.md`
LAND8116 IDC_Timer 심볼 드리프트 + 매크로 연쇄오류(2026-05): `references/land8116-idc-timer-symbol-drift-and-macro-cascade-2026-05.md`
LAND8116 CP949 손상 시 HEAD blob 직접복원 + 최소 재적용(2026-05): `references/land8116-cp949-gitblob-restore-and-timer-reapply-2026-05.md`
인터뷰 Yes/No 자동응답 stdin 파이프 안정화(종료 race 대응): `references/mfc-interview-dialog-stdin-pipe-reliability.md`
인터뷰 4문항 Yes/No 강제형 질문 설계 + 다중 chunk 파싱: `references/mfc-interview-yesno-question-design.md`
인터뷰 가변 문항 수(Top3×2 등)와 `[INTERVIEW_Qn]` 정수 파싱: `references/mfc-variable-interview-question-count.md`
인터뷰 최종확정(`[FINAL_CONFIRM_Q]`) 전용 팝업 처리: `references/mfc-interview-final-confirmation-popup.md`
MFC Start command self-healing for stale command edit boxes: `references/mfc-start-command-self-healing.md`
Child-process agent 상태 패널 패턴: `references/mfc-agent-status-panel-for-child-process.md`
Child-process agent 상태 패널 패턴: `references/mfc-agent-status-panel-for-child-process.md`
Child-process agent 상태 패널 패턴: `references/mfc-agent-status-panel-for-child-process.md`
Multi-agent workflow ListView 표시 패턴: `references/mfc-multi-agent-progress-listview.md`
Pipeline-only GUI shell runner 패턴: `references/mfc-pipeline-only-gui-shell-runner.md`

## Common Pitfalls
1. Adding handler in `.cpp` but forgetting declaration in `.h`.
2. UI regression after broad edits in CP949-heavy files (한글 깨짐, 리스트/컨트롤 미표시).
   - Symptom: user reports previously working Korean text/layout suddenly broken after feature insertion.
   - Safer recovery: immediately rollback the touched high-risk files, re-apply only minimal scoped edits (one-line macro change, isolated sidecar `.cpp`), then rebuild.
   - Avoid stacking multiple risky edits before a verification build.
2. Reusing existing control IDs and causing click-routing bugs.
3. Starting multiple timers without killing prior one.
4. Not destroying modeless popup windows on parent destroy.
5. Assuming `.rc` exists because `.vcxproj` references it.
6. Mixing ANSI/Unicode APIs inconsistently in KR locale projects.
7. Reopening a modeless dialog after user closes it via window [X] without handle validation.
   - Symptom: dangling pointer crash on `ShowWindow`/`SetForegroundWindow`.
   - Fix: on open, guard with `if (ptr && !::IsWindow(ptr->GetSafeHwnd())) { delete ptr; ptr = NULL; }`.
   - Better UX: handle `WM_CLOSE` in tool dialog with `ShowWindow(SW_HIDE)` to reuse single instance safely.
8. Relative-path asset/config load failures when app is launched from a different working directory.
   - Symptom: popup like `ERROR : Failed to load! FILE PATH: ...` even though files exist under `..\\BIN\\image`.
   - Root cause: code uses `GetCurrentDirectory()` + relative paths; launcher/IDE starts process with unexpected CWD.
   - Fix: anchor CWD at process start in `InitInstance()`:
     - `GetModuleFileName(NULL, exePath, MAX_PATH)`
     - trim to exe directory
     - `SetCurrentDirectory(exeDir)`
   - Then rebuild and verify by launching exe from both solution root and exe directory.
8.5. GUI child-process command fields can retain stale invalid text and break Start with `GetLastError=2`.
   - Symptom: transcript shows `[START] z --focus-log ...` or another non-executable token, followed by `프로세스 실행 실패. GetLastError=2`.
   - Root cause: the editable command control preserved a previous/debug command; log selection appended/replaced `--focus-log` but did not validate the executable/script prefix.
   - Fix pattern:
     1) centralize the known-good default command in a helper such as `DefaultMaintenanceCommand()` instead of duplicating a long literal in `OnInitDialog`,
     2) before applying `UpdateFocusLogArg(...)`, trim and validate the command contains the expected wrapper/script token (for JAN: `run_maintenance_with_review.py`),
     3) if not, replace the whole command with the default and append a transcript warning,
     4) then append/replace `--focus-log`.
   - Verification: after selecting a log, transcript `[START]` must begin with quoted `python.exe` + the expected wrapper path, not the stale token. Add a static regression test for the helper, validation branch, and warning string; rebuild immediately.
9. KR-encoded source files can break from direct string edits (C2001/C1057 cascades).
   - Symptom: after a small `_T("...")` edit, compiler throws `C2001: newline in constant`, `C1057: unexpected EOF in macro expansion`, or `C2059` at unrelated lines.
   - Root cause: CP949/ANSI-encoded files with already-garbled literals are fragile under automated patching.
   - Safer strategy:
     - Prefer ASCII asset names (e.g., `Debugbackimage.png`) and minimize edits inside garbled files.
     - For tiny macro/constant edits in fragile files, avoid generic text patching that may rewrite file encoding.
       Use an encoding-preserving script (`read_bytes -> decode('cp949') -> targeted replace -> encode('cp949')`) and then rebuild immediately.
     - If only linker symbols are missing, add a separate `.cpp` implementation unit instead of heavily editing a fragile file.
     - If a fragile file is touched and compile explodes, immediately `git checkout -- <file>` and re-apply via sidecar file / minimal patch.
   - LAND8116-specific addendum: when `LANDTestView.cpp` repeatedly re-breaks after timer/PS edits, freeze that file (rollback + build green), then continue integration via `.h` + sidecar `.cpp` + runtime wiring points only, with one-change-one-build discipline.
10. Hidden test items can be caused by temporary visibility macros, not runtime logic.
   - Symptom: specific test group (e.g., HUMS SW) shows only first few items in tree.
   - Fast check: inspect `*_visible_end`/range macros used in tree population loops.
   - Example: `maintest_HUMSSW_visible_end 16` limits insertion loop to TH01~TH02; set to `maintest_name_size` to restore full list.
   - In CP949-fragile files, apply this as a minimal one-line, encoding-preserving edit and verify with immediate build.
11. RC script edits can fail with `RC2104` in legacy KR projects even after restoring from ad-hoc backups.
   - Symptom: ResourceCompile fails at a specific `.rc` line with `undefined keyword or key name` after toggling button styles/visibility.
   - Root cause: mixed/broken encoding or malformed token boundaries inside `.rc`; small text rewrites can invalidate parser state.
   - Safer sequence:
     1) Avoid `.rc` churn for simple "show button" requests — prefer runtime `GetDlgItem(...)->ShowWindow(SW_SHOW)` in `OnInitDialog`.
     2) Before any `.rc` edit, make a timestamped backup and note source encoding.
     3) If `RC2104` appears, restore from known-good `.rc`, rebuild first, then re-apply minimal runtime-only UI change.
     4) Do not proceed with feature work until ResourceCompile is green again.
12. Mixed-encoding sibling files can silently break paired edits (`.h` vs `.cpp`).
   - Symptom: message-map and handler added in `.cpp`, but compiler says member/field is missing from class in `.h`.
   - Root cause: one file is UTF-8(BOM) while the other is CP949; a single-encoding patch script updates only one side.
   - Fix pattern:
     1) detect encoding per file independently (e.g., UTF-8-SIG for header, CP949 for cpp),
     2) patch each file in its own encoding,
     3) verify by searching both declaration and use-site strings before build.
12. Reusing an existing member pointer with a different dialog type can cause hard compile errors.
   - Symptom: `C2440` converting `DerivedDialog*` to unrelated pointer type (e.g., `CDialogTimer*`).
   - Fix: use a dedicated pointer of the correct type (preferred), or a function-static pointer for a minimal-risk modeless utility dialog when header churn is risky.
   - Always add stale-window guard: `if (ptr && !::IsWindow(ptr->GetSafeHwnd())) { delete ptr; ptr = NULL; }`.
13. Background/UI defect may be asset content, not rendering logic.
   - Symptom: top-left black/empty block while buttons and labels are otherwise normal.
   - Fast check: inspect loaded image file dimensions/content before touching paint code.
   - Example pattern: `OnPaint` draws `Debugbackimage.png` at `(0,0)`; if file itself is a small dark rectangle (e.g., `449x213`), the UI defect is expected.
   - Fix priority: replace/correct asset first, then adjust paint/layout code only if defect persists.
14. Timer button is wired but "click does nothing" can be a dialog-visibility or resource-definition issue, not message-map failure.
   - Fast checks (in order):
     1) confirm `ON_BN_CLICKED(IDC_BUTTON_FAILSTOP, ...)` or the active timer button ID mapping exists,
     2) confirm the intended handler (`OnBnClickedTimer`) actually contains dialog-open logic,
     3) confirm `IDD_DIALOG_TIMER` exists exactly once in `.rc` (no duplicate dialog resource IDs),
     4) if modeless opens but appears hidden/unfocused, switch to `ShowWindow(SW_SHOW)` and call `SetForegroundWindow()`.
   - Symptom of duplicate resource ID: build/link fails with `CVT1100: duplicate resource ... DIALOG, name:342`.
   - Recovery: remove the extra `IDD_DIALOG_TIMER` block and keep only one canonical definition.
15. Handler-name drift causes maintainability bugs in legacy screens.
   - Symptom: logic is added to a legacy alias handler (e.g., `OnBnClickedButtonFailstop`) while the team expects `OnBnClickedTimer` as canonical entrypoint.
   - Fix pattern: keep timer/dialog logic in `OnBnClickedTimer`, and make legacy alias handlers delegate to it during migration (`OnBnClickedButtonFailstop() { OnBnClickedTimer(); }`).
   - Verification: message map should include the real clicked control ID to `OnBnClickedTimer`, then build and runtime-click verify.
16. Encoding-sensitive files (CP949/ANSI) can be corrupted by generic patch tools even for tiny edits.
   - Symptom: after a small replace, unrelated compile errors appear (`C2001`, `C1057`, broken string literals) or Korean comments/strings become mojibake.
   - Safer edit pattern:
     1) prefer encoding-preserving scripted edits (`decode('cp949') -> targeted replace -> encode('cp949')`) or raw-byte exact-token replacement,
     2) avoid broad block replacement in fragile files,
     3) build immediately after each micro-change.
   - Recovery: if corruption appears, `git checkout -- <file>` first, then re-apply via encoding-preserving script.
17. CP949 파일에서 `WrapConfirmMessage` 같은 문자열 전처리(줄바꿈 삽입)가 한글을 바이트 경계에서 분할해 깨짐을 만들 수 있다.
   - Symptom: 확인 팝업 문구에 `폴?`, `塚?` 같은 깨진 글자가 나타나고, 긴 경로/인용부호 문장에서 재현됨.
   - Root cause: `_MBCS` 프로젝트에서 문자 수 기준 줄바꿈 로직이 멀티바이트 한글 경계를 깨뜨림.
   - Fix pattern:
     1) `OnConfirm`/`OnConfirmIndex` 계열은 원문 문자열을 그대로 전달 (`yes.m_inputText = input;`),
     2) 다이얼로그 에디트는 ANSI API(`SetWindowTextA`) 대신 TCHAR 경로 API(`SetWindowText`) 사용,
     3) 변경 직후 즉시 빌드 검증.
   - If patching introduced compile cascades (`C2001/C1057`): rollback target file and re-apply with byte-safe exact replacement, then rebuild.
18. Close-button behavior for utility dialogs must match user intent: hide vs terminate.
   - Symptom: `Close` button appears to do nothing because handler is missing, or window only hides when user expects full close.
   - Fix pattern:
     - add explicit `ON_BN_CLICKED(IDC_BUTTON_TIMER_CLOSE, &Class::OnBnClickedClose)` mapping,
     - in close/cancel handlers call `KillTimer(...)` then `EndDialog(IDCANCEL)` when modal termination is required.
   - Verification: click `Close` and confirm dialog is destroyed (not just hidden), then re-open path still works.
18. In KR-locale legacy UIs, standardize user-visible labels to ASCII English when mojibake is reported.
   - Symptom: labels/buttons/column headers render as broken glyphs depending on code page.
   - Fix pattern: replace runtime-created control captions and helper text with ASCII-safe strings (`Start/Stop/Reset`, `Elapsed Time`, etc.).
   - Verification: run app and confirm all timer-dialog texts are readable without font/codepage dependence.
19. Power-supply GUI buttons can look "dead" when command handlers run before connection is established.
   - Symptom: IP/port are valid and device responds to socket probe, but UI power ON/OFF appears to do nothing.
   - Root cause pattern: click handler sends SCPI (`eSetVolt/eSetCurr/eEnableOutput`) without pre-connection guard; connection is only established in another flow (e.g., test-start initialization).
   - Fix pattern: in button handlers, enforce `IsSimulationMode` check -> `IsLanSocketConnected`/`RefreshConnection` -> execute command -> explicit fail log/label update.
   - Verification: probe `*IDN?` externally, then test both paths (before and after test-start) and confirm UI shows connected/disconnected/sim-mode explicitly.
20. `resource.h` numeric alias can mislead click wiring for timer buttons.
   - Symptom: visible `Manual TIMER` button does nothing even though a similarly named legacy handler exists.
   - Root cause: `.rc` control uses one symbol (e.g., `IDC_Timer`) while code wires another legacy symbol/handler; aliases may share numeric ID and hide mismatch.
   - Fix pattern: treat `.rc` dialog block as click source-of-truth, wire that exact control ID to canonical handler (`OnBnClickedTimer`), and make legacy handlers delegate only.
   - Verification: one-click open, second-click close, then immediate build report.
21. Never run repository-wide encoding normalization in CP949-heavy legacy MFC trees.
   - Symptom: after "fixing Korean globally", compiler emits cascades like `C2001: newline in constant`, `C1057: unexpected EOF in macro expansion`, and user-defined-literal/parse errors far from actual edit points.
   - Root cause: mass UTF-8↔CP949 conversion rewrites string/quote boundaries or substitutes unsupported characters, corrupting literals/macros.
   - Safe recovery:
     1) restore baseline first (`git restore .` or file-level restore),
     2) re-apply only minimal scoped edits,
     3) verify escaped newlines stay as `\\n` inside literals,
     4) re-check edited tokens with search before build.
   - See: `references/land8116-encoding-mass-conversion-regression-and-recovery-2026-05.md`.
22. `IDC_Timer`/control-ID compile cascades are often resource-symbol drift, not handler logic.
   - Symptom set: `IDC_Timer undeclared`, `_messageEntries const object must be initialized`, `macro invocation improperly terminated`, followed by newline-in-constant style cascades.
   - Root cause pattern: `.rc` uses `IDC_Timer` but `resource.h` lost/never had the symbol (common after restore/merge), while message map references it.
   - Fix pattern:
     1) treat `.rc` control symbol as source-of-truth,
     2) ensure exact symbol exists in `resource.h` (aliasing to legacy numeric ID is acceptable),
     3) keep canonical handler mapping on that exact symbol,
     4) then re-check string literals for accidental real newline insertion.
   - Verification: search all three before build: `resource.h` define, `.rc` control line, `.cpp` `ON_BN_CLICKED(...)` entry.
23. Twin-repo/worktree confusion can make a "fixed" UI bug appear unchanged.
   - Symptom: user still reproduces the exact issue after a reported patch/build success.
   - Root cause: edits were applied to sibling tree A (e.g., `LAND8R-24HS4_b`) while the user runs tree B (`LAND8R-24HS4`).
   - Prevention step: before any edit, identify active run target (solution path/exe path) and patch that exact tree.
   - Verification: build the same `.sln` path the user launches, not a sibling clone.
24. In MBCS/CP949 projects, helper line-wrap functions can corrupt Korean dialog text.
   - Symptom: confirm popup shows mojibake fragments like `우?`, `�?`, `塚?` while source literals look correct.
   - Root cause pattern: byte-count-based wrapping/insertion (e.g., `WrapConfirmMessage`) splits multibyte Hangul.
   - Fix pattern: for confirm/check dialogs, pass original `CString` without manual wrapping (`m_inputText = input`), and rely on control layout/wrapping.
   - Related guardrail: avoid `SetWindowTextA` for UI text; use `SetWindowText` to preserve TCHAR path.
25. CP949-fragile files: prefer encoding-preserving targeted replacement over generic patch when high-risk files start cascading errors.
   - Symptom: after a small text patch, build explodes with `C2001`, `C1057`, or unrelated literal errors.
   - Safer pattern:
     1) restore file first if corruption appears,
     2) re-apply minimal token replacement with explicit encoding (`read_text('cp949')/write_text('cp949')` or byte-safe replacement),
     3) build immediately,
     4) if link fails with `LNK1104` on `.exe`, terminate running process and rebuild.
23. Result-confirmation fail paths can skip UI restoration if they only call `OnFail()`.
   - Symptom: after a FAIL-confirm flow ends, test buttons remain disabled or state is inconsistent with normal test end.
   - Root cause pattern: non-standard termination branch (e.g., confirm-dialog callback) bypasses the usual test-end sequence.
   - Fix pattern: ensure every termination branch calls the same end-of-test pair used by the main flow:
     - `FinalizeTestResult();`
     - `FinishTestUI();`
   - Verification: trigger PASS and FAIL confirmation branches and confirm final button state is identical (only Stop disabled, other test controls enabled).
24. Modal interview dialogs + stdin auto-answer have a race with child-process exit.
   - Symptom: UI shows "stdin pipe 전송 실패" right after Yes/No click, often near process end.
   - Root cause: stdout-triggered popup is asynchronous; by click time child may have closed stdin (`ERROR_BROKEN_PIPE` / `ERROR_INVALID_HANDLE`).
   - Fix pattern:
     1) use `WriteAnswer(answer, &err)` and return detailed Win32 error,
     2) pre-check child liveness via `WaitForSingleObject(m_pi.hProcess, 0)`,
     3) re-check liveness again immediately after user closes MessageBox (click delay race),
     4) for broken-pipe/invalid-handle class failures, downgrade to info/warn log (no hard error modal),
     5) keep manual Send fallback only for non-race errors.
   - Apply same handling to both per-question Yes/No auto-send and post-Q4 manual-send dialog.
25. Interview 질문이 한 stdout chunk에 몰려와도 각 `[INTERVIEW_Qn]`을 각각 분리해 Yes/No dialog를 띄워야 한다.
   - Symptom: 여러 질문이 출력됐는데 팝업은 1개만 뜨거나, 앞쪽 질문만 응답 처리됨.
   - Root cause: chunk 단위 문자열 전체를 단일 질문으로 취급하거나, `while (m_interviewQuestionCount < 4)` / `ch >= '1' && ch <= '4'` 같은 하드코딩으로 질문 수를 제한함.
   - Fix pattern:
     1) `[INTERVIEW_Qn]` 마커를 while 루프로 순회 파싱,
     2) `]` 앞의 전체 숫자를 `_wtoi` 등으로 정수 파싱해 `[INTERVIEW_Q6]`, `[INTERVIEW_Q10]`도 처리,
     3) 질문 번호(`n`)를 실제 state(`m_interviewQuestionCount`)와 비교해 이미 처리한 번호는 skip,
     4) 각 번호마다 MessageBox를 1회씩 호출,
     5) 안내 문구는 `[질문 n/4]`처럼 총량을 고정하지 말고 `[질문 n]`처럼 가변형으로 표시.
   - Upstream alignment:
     - Python 수집/저장/최종 payload에서도 `questions[:4]`, `answers[:4]` slicing을 제거한다.
     - Top3 후보 × 2문항처럼 요구사항이 확장될 수 있으므로 “생성된 질문 전체”를 프로토콜 기준으로 삼는다.
   - See: `references/mfc-variable-interview-question-count.md`.
26. Final confirmation markers must not fall back to generic manual-input prompts.
   - Symptom: after the 4 interview Yes/No dialogs, GUI asks whether to send manually typed input instead of showing the final decision dialog.
   - Root cause: terminal protocol marker such as `[FINAL_CONFIRM_Q]` is not parsed as its own event and leaks into generic stdin/manual-send handling.
   - Fix pattern:
     1) parse `[FINAL_CONFIRM_Q]` before generic manual-input handling,
     2) show a dedicated final-confirmation popup (`최종 진단 확정`),
     3) map buttons to stable tokens: `approved`, `rejected`, `pending`,
     4) send the token via the guarded `WriteAnswer(..., DWORD*)` path,
     5) append transcript evidence like `[DIALOG FINAL_CONFIRM] approved`.
   - Mirror-tree pitfall: if declarations/signatures/member fields changed, sync both `.cpp` and `.h` to policy/worktree copies before building; cpp-only mirroring can leave stale header errors.
   - See: `references/mfc-interview-final-confirmation-popup.md`.

27. JAN 정비/Ouroboros 인터뷰 질문은 단순한 일반 확인 질문으로 만들지 않는다.
   - Symptom: GUI에는 Yes/No 팝업 4개가 뜨지만 질문이 `재시험할까요?`, `확정할까요?`, `소스코드를 확인할까요?`처럼 추상적이거나 사용자가 소스코드를 직접 확인해야 하는 형태로 보여 실제 현장 판단에 맞지 않음.
   - User expectation: 고장/불량이 뜬 항목을 기준으로 고장배제 목록과 프로그램이 해석한 소스/설정 근거를 포함하되, 최종 질문은 "주장비/전원/케이블/통신 라인 등을 실제로 확인했는가"라는 현장 확인 여부여야 한다.
   - Fix pattern:
     1) 질문 생성기는 `focus.file`, `test_ids`, `risk`, `recommended_exclusion_items`를 읽어 불량 항목을 명시한다.
     2) 고장배제 1순위/상위 3개 조치 목록을 질문 문장에 포함한다.
     3) `fault_exclusion_master_map.csv`, `generate_maintenance_report.py`, `ouroboros_review_loop.py` 등은 사용자가 직접 확인할 대상이 아니라 프로그램의 판단 근거로 `source_action_candidates`에 저장한다.
     4) Q3류 질문은 `소스/설정 근거상 주장비 측 확인 필요 부위로 보이는 '<부위>'를 주장비에서 확인했습니까? (Yes/No)`처럼 쓴다.
     5) MFC 입력 방식과 맞게 각 문장은 반드시 `(Yes/No)`로 끝나는 폐쇄형 질문 4개를 유지한다.
   - Verification: review JSON의 `step7.interview_questions` 4개에 불량 항목, 고장배제, 소스/설정 근거, 주장비/현장 확인 문구가 모두 들어가고, "사용자가 소스코드를 확인하라"는 의미가 남지 않았는지 확인한다.

29. MFC command edit box can preserve stale debug/operator text and break Start.
   - Symptom: transcript shows `[START] z --focus-log ...` followed by `프로세스 실행 실패. GetLastError=2`.
   - Root cause: Start uses the current command edit content as the executable command; a stale token is interpreted as the executable path before Python/report generation ever starts.
   - Fix pattern:
     1) centralize the canonical wrapper command in `DefaultMaintenanceCommand()`,
     2) initialize the command edit from that helper,
     3) before `UpdateFocusLogArg(...)`, check for the expected wrapper token such as `run_maintenance_with_review.py`,
     4) if absent, restore the default command and append a visible transcript warning,
     5) then add `--focus-log` and verify the `[START]` line begins with quoted absolute `python.exe`.
   - See: `references/mfc-start-command-self-healing.md`.

30. Pipeline-only variants should preserve the proven MFC shell and swap the child-process runner, not rewrite the UI first.
   - Symptom: user asks for “기본적인 틀 GUI는 유지하고 파이프라인 구현” but the repo was cloned from a hybrid agent/review workflow.
   - Root cause pattern: old default command, self-healing token, status labels, review-output args, and final-confirm/interview paths still point at the hybrid runner.
   - Fix pattern:
     1) add a thin runner such as `tools/pipeline_only_runner.py`,
     2) repoint `DefaultMaintenanceCommand()` to the new runner and project root,
     3) update command self-healing token from the old hybrid script to the new runner,
     4) emit simple `[PIPELINE] state | detail` markers for the existing status/ListView parser,
     5) keep old parser branches harmless but ensure default execution does not invoke review/interview/final-confirmation gates,
     6) if trained model artifacts are absent and short-term baseline is acceptable, fall back deterministically and record the mode in JSON output.
   - Verification: static tests for default command/no review markers, direct pipeline smoke producing non-empty `.docx`/`.json`, then Debug x64 MFC build and launch check.
   - See: `references/mfc-pipeline-only-gui-shell-runner.md`. 

## Optional: Temporarily disable hardware-specific modules (e.g., uCAN)
When the user asks to build without a hardware DLL/module for now, do a reversible project-level disable instead of deleting code.

Recommended minimal-risk sequence:
1. Remove module library from `<AdditionalDependencies>` in all active build configs.
   - Example: remove `uCANDLL.lib` from Debug/Release link dependencies.
2. Exclude the module implementation `.cpp` from build in `.vcxproj`.
   - Example: comment out `<ClCompile Include="Resource\\CUCAN.cpp" />`.
3. Keep headers/source files in tree (do not delete) so rollback is one edit away.
4. Rebuild and verify link line no longer contains the disabled library.

Pitfall:
- Removing only `.lib` but still compiling module `.cpp` can leave unresolved externals if that `.cpp` directly calls vendor APIs.
- Removing link/build inputs alone is not enough when test flows launch vendor executables directly (e.g., `LaunchProgram("...GNCuCAN.exe")` / `TerminateProgram("GNCuCAN.exe")`). Those call sites keep runtime dependency alive unless also disabled.

Verification add-on for temporary module disable:
- Run literal content searches with multiple tokens (not a single regex) to catch all references:
  - library token: `uCANDLL.lib`
  - compile item token: `Resource\\CUCAN.cpp`
  - runtime tokens: `GNCuCAN.exe`, `GNCUCAN`, `TerminateProgram("GNCuCAN.exe")`, `LaunchProgram(`
- Patch direct call sites in test cases and utility default-path tables, then rebuild and confirm link line and touched compile units no longer include the module.

## Solution Explorer tree recovery (`.vcxproj.filters`)
If Solution Explorer grouping disappears or gets messy, regenerate/update `*.vcxproj.filters` to restore readable class-level groups.

Practical grouping pattern for large test GUIs:
- Top-level by test domain (e.g., self-check / CC test / HUMS GUI)
- Separate `공통/인프라` for shared View/Utility/Resource files
- Keep resource artifacts (`.rc`, `res/*`) under dedicated resource filter

Verification:
- Reopen solution and confirm filters render as intended.
- Rebuild to ensure filters-only changes introduced no build regression.

## Communication contract in policy-gated multi-agent repos
When the repo/user policy requires fixed subagent personas and response format:
- Keep replies in `에이전트이름: 내용` form consistently.
- Do not switch to generic assistant tone mid-task.
- Treat format/tone corrections as blocking quality issues, same priority as build/test failures.

## Verification Checklist
- [ ] For child-process/agent dialogs, a dedicated status panel exists above the transcript/log and reflects idle/start/running/input-wait/final-confirm/sending/done/error transitions.
- [ ] If the workflow has multiple logical agents/roles inside one child process, a ListView or equivalent audit area shows `Agent / State / Detail` so the user can tell which role is active.
- [ ] If logical agent names are displayed, the child process emits explicit markers such as `[AGENT] Name | detail`; GUI fallback parsing is retained only for older protocol markers.
- [ ] If the user needs to audit agent progress after the fact, every distinct status transition is also appended to the transcript/log (for example `[AGENT STATUS] state - detail`) with a last-status guard to avoid duplicate spam from frequent stdout chunks.
- [ ] If the `Agent` column represents logical roles/phases inside one child process, state that clearly; do not imply multiple OS-level agents unless the implementation actually spawns multiple processes.
- [ ] If the user needs to audit agent progress after the fact, every distinct status transition is also appended to the transcript/log (for example `[AGENT STATUS] state - detail`) with a last-status guard to avoid duplicate spam from frequent stdout chunks.
- [ ] If the user wants active agent work to be visible at a glance, add a `SysListView32`/`CListCtrl` progress list between status and transcript with simple columns such as `No`, `State`, and `Detail`; feed it from the same duplicate-guarded `SetAgentStatus` path, clear it on each new Start, and initialize common controls with `ICC_LISTVIEW_CLASSES`.
- [ ] New button is visible and clickable on target screen.
- [ ] Button opens dialog exactly once (reuses existing instance).
- [ ] Start updates time continuously.
- [ ] Stop freezes time and appends one list entry.
- [ ] Reset clears display and history list.
- [ ] Closing parent screen cleans up popup safely.
- [ ] `.vcxproj` includes new `.h/.cpp` files.
- [ ] If hardware module disabled, link dependencies and compile items are both updated.
- [ ] If filters updated, Solution Explorer tree renders correctly after reopen.
- [ ] Build verification is explicit (Debug/Win32 at minimum; include Release when requested).
- [ ] Before concluding linker failure as code issue, check for executable lock (`LNK1104 ... .exe`) and report "process-close needed" distinctly from compile errors.
- [ ] Build gate per patch: after EACH non-trivial code edit (not only at the end), run a build and report pass/fail immediately.
- [ ] If build fails, include the first blocking compiler/linker symbol and file:line in the feedback before proceeding.
- [ ] Runtime verification is explicit: launch built `.exe`, confirm process is running, then cleanly terminate test run.
- [ ] If user requests repeated verification (e.g., "두번씩 검증"), run two full consecutive cycles: build -> launch -> process-alive check -> terminate, and report each cycle separately (including PID/evidence).
- [ ] Verify non-standard test termination callbacks (e.g., confirm-dialog `OnFinalConfirm`) also execute `FinalizeTestResult()` + `FinishTestUI()` and leave final button state consistent.

## INI-backed configuration dialogs (IP/PORT/User) — round-trip validation
For legacy settings dialogs (e.g., `ipset.ini`-driven screens), validate full round-trip, not just compile success:
1. Confirm load path in code (`LoadConfiguration` → `Read*`) and concrete ini location.
2. Confirm UI binding in `OnInitDialog` (`SetAddress` / `SetWindowText`) from in-memory config structs.
3. Confirm apply handler copies control values back to config structs and calls `Write*` methods.
4. Confirm `Write*` methods persist expected keys in ini (exact section/key names).
5. Execute runtime check:
   - launch app,
   - change one representative field,
   - click apply,
   - verify ini file changed,
   - reopen dialog and verify value redisplays.

Pitfall:
- Code-path inspection alone can miss runtime dispatch/binding issues. If user asks “확인”, include build + run + persistence evidence, not only static code review.
