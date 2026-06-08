# LAND8R/LAND8116 Stop Final Result Display

## Trigger
Use this note when the user asks that LAND8R/LAND8116 should still show a result value after pressing 시험 중지 / Stop, or when the final result field is blank after an interrupted test.

## Durable lesson
In `LAND8116/LANDTestView.cpp`, the Stop/interrupted branch of finalization must not clear the displayed lead time or result fields. Earlier logic blanked them with calls like:

```cpp
m_leadtime.SetWindowText("");
m_testresult.SetWindowText("");
```

That makes a user-visible result disappear exactly when the operator needs an interrupted-test summary.

## Preferred behavior
- Normal completion: continue displaying PASS/FAIL using the existing completed-test result rules.
- Stop/interrupted with any completed row already marked FAIL: display `FAIL`.
- Stop/interrupted with no completed FAIL: display `STOP`.
- Stop/interrupted should still show elapsed/lead time.
  - Prefer the timer dialog's elapsed value if available.
  - Otherwise calculate from recorded start/end time.
- Stop/interrupted should also leave a visible result-list row for the interrupted item, not only the final summary label.
  - Add a `STOP` row to `IDC_LIST_TESTRESULT`/`m_ctrllist` when a real test selection had started (`self_progressAllcnt > 0 || j > 0`).
  - Fill the visible columns with current group/item, result `STOP`, measured value like `시험 중지`, and `-` for unavailable values.
  - Increment the same row counters used by save/report (`j`, `self_progresscnt`) so the stop row is included in saved history/report data.

## Important index pitfall
Do not assume the old `RESULT_INDEX` value is correct. In the observed LAND8116 list layout, the result text was in column index `2`, while an older constant used `7`, which pointed at the unit column and made result scanning unreliable.

Before changing result aggregation, re-check the list column order in the current source/resource, then align the constant with the actual result column.

## Verification checklist
1. Confirm the Stop branch no longer calls `m_leadtime.SetWindowText("")` or `m_testresult.SetWindowText("")`.
2. Confirm the Stop branch sets a non-empty result: `FAIL` if any current row failed, otherwise `STOP`.
3. Confirm the Stop branch appends a visible `STOP` row to the result list for the interrupted item, guarded so an invalid/no-selection start does not create a misleading row.
4. Confirm saved history/report aggregation includes the stop row and treats `STOP` distinctly from `PASS`.
5. Confirm elapsed time is still written during Stop finalization.
6. Confirm result scanning uses the actual result column, not the unit column, and handles both ASCII `FAIL` and Korean `불량` result text.
7. Preserve CP949/MBCS encoding; avoid C4819 regressions.
8. Build `LAND8116` with Visual Studio MSBuild, typically `Configuration=Debug`, `Platform=Win32` for this tree.
9. If launch-smoke is performed, clean up any lingering `LAND8116.exe` processes after verification.

## Reporting pattern
Report the behavior contract explicitly:
- 정상 완료: PASS/FAIL
- 시험 중지 + 이전 FAIL 있음: FAIL
- 시험 중지 + FAIL 없음: STOP
- 시험 중지해도 소요시간 표시
