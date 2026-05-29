# LAND8116 main screen black rectangle: asset-vs-code triage

Symptom
- Main screen showed a dark rectangle in the top-left while buttons/text looked normal.

Fast diagnosis path
1. Check `OnPaint` background load path and draw coordinates in target view (`LANDMainView.cpp`).
2. Verify actual file loaded (`...\BIN\image\Debugbackimage.png`).
3. Inspect image dimensions/content directly before changing code.

Observed root cause in this case
- `OnPaint` loaded `Debugbackimage.png` and drew at `(0,0)`.
- The image file itself was only `449x213` and visually a dark rectangle.
- Therefore rendering was technically correct; resource content was wrong for full-screen background use.

Fix strategy
- Replace the asset with the intended full-size background (same filename), OR
- Change code to load the correct background filename.

Why this matters
- Avoids unnecessary code edits in fragile KR-encoded files.
- Prevents introducing new compile issues when the defect is in the resource asset, not logic.
