# ResourceCompile RC1110 recovery (legacy MFC)

Use when MSBuild fails at `ResourceCompile` with:
- `RC : fatal error RC1110: could not open <project>.rc`

## Fast diagnosis
1. Open `<project>.vcxproj` and locate:
   - `<ResourceCompile Include="...">`
   - `<UserProperties RESOURCE_FILE="...">`
2. Verify the referenced `.rc` file exists at that exact path.
3. If only `.rc2` exists and `.rc` is missing, build will still fail — recreate `.rc`.

## Minimal `.rc` restore template
```rc
#include "resource.h"
#define APSTUDIO_READONLY_SYMBOLS
#include "afxres.h"
#undef APSTUDIO_READONLY_SYMBOLS

IDR_MAINFRAME      ICON    "C:\\...\\res\\LAND8116.ico"
IDR_MAINFRAME_256  ICON    "C:\\...\\res\\LAND8116.ico"
IDR_LAND8116TYPE   ICON    "C:\\...\\res\\LAND8116Doc.ico"
IDR_TOOLBAR        BITMAP  "C:\\...\\res\\Toolbar.bmp"
IDR_TOOLBAR256     BITMAP  "C:\\...\\res\\Toolbar256.bmp"
```

## Notes
- In some brownfield layouts, RC resolves relative paths unexpectedly (solution root vs project root mismatch).
- If relative `res\...` fails with `RC2135`, switch to absolute paths to unblock verification.
- After build is green, you can refactor resource paths back to stable relative paths in a dedicated cleanup change.
