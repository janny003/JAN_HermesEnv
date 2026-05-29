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
9. KR-encoded source files can break from direct string edits (C2001/C1057 cascades).
   - Symptom: after a small `_T("...")` edit, compiler throws `C2001: newline in constant`, `C1057: unexpected EOF in macro expansion`, or `C2059` at unrelated lines.
   - Root cause: CP949/ANSI-encoded files with already-garbled literals are fragile under automated patching.
   - Safer strategy:
     - Prefer ASCII asset names (e.g., `Debugbackimage.png`) and minimize edits inside garbled files.
     - For tiny macro/constant edits in fragile files, avoid generic text patching that may rewrite file encoding.
       Use an encoding-preserving script (`read_bytes -> decode('cp949') -> targeted replace -> encode('cp949')`) and then rebuild immediately.
     - If only linker symbols are missing, add a separate `.cpp` implementation unit instead of heavily editing a fragile file.
     - If a fragile file is touched and compile explodes, immediately `git checkout -- <file>` and re-apply via sidecar file / minimal patch.
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
