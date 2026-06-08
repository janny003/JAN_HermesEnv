# LAND8R/LAND8116 dialog close blocking and Manual Stopwatch timing

Use this note when modifying LAND8R/LAND8116 MFC dialogs, especially manual test confirmation dialogs and `Utility/CManualStopwatchDialog`.

## Durable lessons

- LAND8116 is CP949/MBCS-sensitive. When touching legacy `.cpp/.h` files that contain garbled or mixed-encoding comments, prefer byte-level ASCII-only patching or decode/encode with the known-safe encoding per file. Do not blindly rewrite the whole file through UTF-8.
- If MSBuild emits `warning C4819` after a small ASCII logic change, check whether the edited file now contains UTF-8 replacement bytes (`EF BF BD`) or mixed UTF-8 text. Remove/replace nonessential broken comments or restore the file before reapplying changes byte-wise.
- Header casing matters in this repo: `ConfirmView.cpp` includes `ConfirmView.h`, while git tracked the header as `ConFirmView.h` in the observed workspace. Use the actually tracked path when running git operations.

## X/ESC close blocking pattern

For modal manual/confirmation dialogs where the user wants interruption only through the main Stop button:

1. Add `ON_WM_CLOSE()` to the message map.
2. Add declarations:
   - `virtual void OnCancel() override;`
   - `afx_msg void OnClose();`
3. Implement both as no-ops:
   - `OnCancel()` blocks ESC and some system-close paths.
   - `OnClose()` blocks title-bar X.
4. Keep explicit button handlers intact. For example, Yes/No buttons may still call `CDialogEx::OnOK()` / `CDialogEx::OnCancel()` if FAIL selection is still a valid test response. The no-op override should not disable the intended FAIL button unless the user explicitly requests that.

Observed target files:
- `LAND8116/CSelectTrueFalse.cpp`
- `LAND8116/CSelectTrueFalse.h`
- `LAND8116/ConfirmView.cpp`
- `LAND8116/ConFirmView.h`

## Manual Stopwatch start/end display pattern

For `LAND8116/Utility/CManualStopwatchDialog`:

1. Add a member such as `CTime m_currentRunStartTime;`.
2. On Start:
   - save `m_startTick = ::GetTickCount64();`
   - save `m_currentRunStartTime = CTime::GetCurrentTime();`
3. On Stop:
   - save `const CTime stopTime = CTime::GetCurrentTime();`
   - update elapsed milliseconds before changing display.
   - create stable `CString` temporaries before `CString::Format`, then cast with `(LPCTSTR)`.
4. Example history format:
   - `%02d  Start:%s  End:%s  Elapsed:%s`
5. Widen the dialog/listbox or enable `WS_HSCROLL` if the new history line is too long.

## Verification checklist

- Build with LAND8R standard command:
  - `MSBuild.exe LAND.sln -t:Build -p:Configuration=Release -p:Platform=Win32 -v:minimal`
- Confirm output copy:
  - `LAND8116.vcxproj -> ...\LAND8116\LAND8116.exe`
  - `1개 파일이 복사되었습니다.`
- Run `git diff --check` for the edited files.
- Check edited files for `EF BF BD` replacement bytes and CP949 decodability when applicable.
- Report whether C4819 is absent or limited to pre-existing unrelated files; do not leave a new C4819 warning introduced by the edit.
