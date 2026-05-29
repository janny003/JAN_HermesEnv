---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

### 3.4 MFC Resource/DDX Integrity Check (Windows GUI builds)

When you see MFC assert messages like:
- `AppMsg - Error: no data exchange control with ID 0x....`
- `dlgdata.cpp` assertion during dialog initialization

Treat this as a **resource-to-code binding mismatch** first, not a runtime logic bug.

Checklist:
1. Convert the hex ID to decimal and map it in `resource.h` (e.g., `0x0443` -> `1091` -> `IDC_STATIC_PERCENT`).
2. Inspect the specific dialog block in `.rc` (e.g., `IDD_*`) and verify that control ID actually exists.
3. Compare against `DoDataExchange()` `DDX_Control` bindings for that dialog class.
4. Restore missing control declarations in `.rc` (minimal change) instead of removing DDX bindings blindly.
5. Rebuild immediately to confirm assertion is gone.

Related pitfall:
- If `.rc` is UTF-8 encoded with non-ASCII strings, add `#pragma code_page(65001)` near the top to avoid RC parsing errors like `RC2104 undefined keyword or key name` caused by code-page mismatch.

### 3.5 Verify File/Process Locks (Windows GUI builds)

- If linker/build fails with `LNK1104` on the output `.exe`, treat it as a lock issue first.
- Confirm whether the app/debugger is still running before retrying the same build command.
- Close the running process (or stop debugger), then rebuild.
- Do **not** loop identical build retries without changing lock state.

Example check:

```bash
# Git-bash / MSYS
ps -W | grep -i LAND8116.exe
# then terminate from debugger or task manager, or:
taskkill //F //IM LAND8116.exe
```

### 3.6 Visual Studio IDE Crash Triage (Windows/MFC work)

When Visual Studio itself closes or crashes while working on a C++/MFC solution, separate IDE health from project health before changing source code.

Checklist:
1. Check Windows Application event logs for `devenv.exe` crashes and note fault module / exception code (common evidence: `VCRUNTIME140.dll`, `0xc0000005`).
2. Read `%APPDATA%\Microsoft\VisualStudio\<instance>\ActivityLog.xml` and `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache\*.err` for MEF/component load failures.
3. If logs show MEF/component-cache errors, close Visual Studio, back up `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache`, then recreate it empty.
4. Reopen Visual Studio and the solution. If it still crashes, test `devenv.exe /SafeMode`.
5. Safe Mode succeeds but normal mode fails → extension/cache/MEF issue. Safe Mode also fails → run Visual Studio Installer Repair before touching the project.

Reference: `references/visual-studio-crash-cache-reset.md` contains a concise evidence pattern and safe reset commands.

### 3.6 Visual Studio IDE Crash Triage (Windows C++/MFC)

When Visual Studio exits/crashes while opening a solution or even a new project, isolate IDE health from project health before editing code.

Checklist:
1. Build the solution outside Visual Studio with MSBuild. In Git Bash/MSYS, set `MSYS2_ARG_CONV_EXCL='*'` so `/p:` and `/m` arguments are not path-converted.
2. If MSBuild succeeds but `devenv.exe` crashes, treat this as a Visual Studio profile/cache/extension/install issue, not a source-code failure.
3. Check Windows Application events for `devenv.exe`, `PerfWatson`, `.NET Runtime`, `VCRUNTIME140.dll`, `KERNELBASE`, and exception codes such as `0xc0000005`.
4. Inspect `%APPDATA%\Microsoft\VisualStudio\<instance>\ActivityLog.xml` and `%LOCALAPPDATA%\Microsoft\VisualStudio\<instance>\ComponentModelCache\Microsoft.VisualStudio.Default.err` for MEF/component load failures.
5. For one-solution failures, back up and remove the solution-local `.vs` folder. Move backups outside the repo so git status stays clean.
6. For all-project/new-project failures, test `devenv.exe /SafeMode`. If Safe Mode is stable, suspect user profile/extensions/MEF cache. If Safe Mode crashes too, suspect installation/runtime damage.
7. Escalate in non-destructive order: clear `ComponentModelCache`, clear solution `.vs`, ask before `devenv /ResetUserData`, then Visual Studio Installer Repair.

See `references/visual-studio-crash-triage.md` for a compact reproduction and evidence-gathering playbook.

### 3.7 Encoding + Partial-Read Safety (legacy C++/MFC files)

When editing large legacy source files (often CP949/EUC-KR mixed comments), avoid corruption from partial context edits.

Checklist:
1. If tooling warns a file was read with offset/limit pagination, **do not** broad-replace near other string literals/macros until you re-read full file context.
2. Prefer changing the narrowest shared function (e.g., device abstraction layer) instead of touching many high-risk UI files.
3. After each patch, rebuild immediately and watch for parser errors like `C2001` (newline in constant), `C2059`, `C1057`.
4. If those appear right after a patch, rollback the touched file first, then re-apply via a safer location/smaller diff.

This prevents introducing encoding/quote breakage while debugging an unrelated runtime issue.

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**
