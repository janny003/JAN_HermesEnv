# Child-process agent 진행상황 ListView 표시 패턴

## Trigger
MFC dialog에서 Python/Ouroboros 같은 child process를 실행하고, 사용자가 "agent가 켜지고 작업 진행 중인 것"을 UI에서 한눈에 보길 원할 때 사용한다.

## Pattern
1. 기존 단일 `CStatic` 상태 패널은 유지한다.
2. 상태 패널 아래, transcript 위에 `SysListView32` / `CListCtrl`을 추가한다.
3. 컬럼은 과도하게 늘리지 말고 기본적으로 다음 3개로 둔다.
   - `No`
   - `State`
   - `Detail`
4. `InitCommonControlsEx`에 `ICC_LISTVIEW_CLASSES`를 포함한다.
5. `DoDataExchange`에 `DDX_Control(..., CListCtrl member)`를 추가한다.
6. `OnInitDialog`에서 `InitializeAgentProgressList()`를 호출해 extended style과 컬럼을 세팅한다.
7. `SetAgentStatus(state, detail)`가 상태 중복을 거른 뒤, transcript 누적과 ListView row 추가를 함께 수행하게 한다.
8. Start 재실행 시에는 `DeleteAllItems()`, sequence reset, last status reset을 수행해 새 작업 흐름만 보이게 한다.

## Minimal implementation sketch
```cpp
void CMyDlg::InitializeAgentProgressList()
{
    m_agentProgressList.SetExtendedStyle(LVS_EX_FULLROWSELECT | LVS_EX_GRIDLINES | LVS_EX_DOUBLEBUFFER);
    m_agentProgressList.InsertColumn(0, L"No", LVCFMT_LEFT, 45);
    m_agentProgressList.InsertColumn(1, L"State", LVCFMT_LEFT, 110);
    m_agentProgressList.InsertColumn(2, L"Detail", LVCFMT_LEFT, 565);
}

void CMyDlg::AddAgentProgress(const CString& state, const CString& detail)
{
    if (!::IsWindow(m_agentProgressList.GetSafeHwnd())) return;
    CString seq;
    seq.Format(L"%d", ++m_agentProgressSeq);
    int row = m_agentProgressList.InsertItem(m_agentProgressList.GetItemCount(), seq);
    m_agentProgressList.SetItemText(row, 1, state);
    m_agentProgressList.SetItemText(row, 2, detail);
    m_agentProgressList.EnsureVisible(row, FALSE);
}
```

## Static regression checks
Add tests that verify:
- `IDC_LIST_AGENT_PROGRESS` exists in `resource.h` and `.rc`.
- `.rc` uses `SysListView32`.
- header declares `CListCtrl m_agentProgressList` and sequence state.
- `.cpp` binds the control with `DDX_Control`.
- `.cpp` inserts `No/State/Detail` columns.
- `SetAgentStatus` calls `AddAgentProgress(state, detail)` after duplicate filtering.
- Start path clears ListView and resets sequence.
- app init includes `ICC_LISTVIEW_CLASSES`.

## Runtime verification
After build, launch the exe, programmatically or manually press Start, then verify:
- the main dialog exists,
- `SysListView32` child exists,
- `LVM_GETITEMCOUNT` returns one or more rows while the agent is active.

## Pitfalls
- Forgetting `ICC_LISTVIEW_CLASSES` can make the ListView control fail or behave inconsistently.
- Adding every stdout chunk directly to ListView creates noisy UI. Use status transitions, not raw stream chunks.
- If `SetAgentStatus` already has duplicate suppression, put ListView insertion inside that same guard.
- Reset the list on each new Start; otherwise prior runs mix with current evidence.
- Keep transcript logging as an audit trail even after adding ListView; ListView is for glanceable progress, transcript is for detail.
