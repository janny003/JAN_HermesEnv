# ATESWLIB 1553B BIT legacy GPS/CPS cross-check

Use this when modifying or verifying ATESWLIB K2 `GetPOBIT/GetIBIT/GetPBIT` parsing for GPS/CPS-family projects.

## Legacy reference locations
- GPS reference: `C:\Users\yjs\Desktop\JAN\GPS\JoystickDlg.cpp`
- CPS reference: `C:\Users\yjs\Desktop\JAN\CPS\JoystickDlg.cpp`
- Main function: `DecodeBiteInfo(USHORT data)`
- Header members: `JoystickDlg.h`

## Channel mapping observed in legacy MFC code
- Power-On BIT / POBIT: `rb4[0]`
- IBIT: `rb5[0]`
- PBIT: `rb6[0]`
- The receive loop stores `msgptr->words[2]` into these `rb*` buffers for the corresponding RT-to-BC subaddress.

## Bit numbering rule
Legacy GPS/CPS treats ICD bit1 as the received word LSB:

```cpp
m_intBite0 = data & 0x0001;
m_intBite1 = (data >> 1) & 0x0001;
```

Therefore Core parser helpers that accept `bitNo` in ICD terms must read:

```csharp
return (ushort)((inputData[0] >> (bitNo - 1)) & 0x0001);
```

Do not use `inputData[0] >> bitNo` for ICD bit1~bit9; that shifts every reported BIT value by one position compared with the legacy GPS/CPS reference.

## Preferred ATESWLIB Core locations
- GPS-family Core parser: `K2/TestProgram/Core/Data/KGPS_2/1553BICD.cs`
- CPS-family Core parser: `K2/TestProgram/Core/Data/KCPS_2/1553BICD.cs`
- Keep `GetPowerOnBIT(...)` as a backward-compatible wrapper to `GetPOBIT(...)` if callers still exist.

## Verification sequence
1. Search the legacy GPS/CPS folders for `DecodeBiteInfo`, `rb4[0]`, `rb5[0]`, `rb6[0]`, `m_intBite0`, and `m_intBite1` before changing Core assumptions.
2. Build Core directly:
   - `MSBuild.exe K2/TestProgram/Core/Core.csproj /p:Configuration=Debug /p:Platform=AnyCPU`
3. Build K2 solution:
   - `MSBuild.exe K2/K2.sln /p:Configuration=Debug /p:Platform=x86`
4. Build AteMgr using the actual solution path:
   - `MSBuild.exe AteMgr/AteMgr_K2.sln /p:Configuration=Debug /p:Platform=x86`
5. Report warnings separately from errors. Existing warnings about unused variables/platform mismatch are not equivalent to build failure.
