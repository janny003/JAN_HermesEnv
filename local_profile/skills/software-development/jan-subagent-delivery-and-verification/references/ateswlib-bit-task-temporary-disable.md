# ATESWLIB BIT Task 임시 비활성화 패턴

Use when the user asks to temporarily comment out or disable selected JAN/ATESWLIB BIT tests without deleting the implementation.

## Core rule
Do not only comment out the task method body. Disable both execution registration and compilation inclusion so the task is clearly out of the active path while the source file remains recoverable.

## Required 2-point disable per module
For each selected module:

1. Main task registration
   - File: `K2/TestProgram/<MODULE>/<MODULE>Main_UUT01.cs`
   - Change `AddTask(UUT01_TaskNN);` to a comment, preserving the task number and reason.
   - Example:
     ```csharp
     // AddTask(UUT01_TaskNN);           // NN.BIT 시험 - 임시 주석 처리
     ```

2. Project compile include
   - File: `K2/TestProgram/<MODULE>/<MODULE>.csproj`
   - Comment out the matching compile include.
   - Example:
     ```xml
     <!-- <Compile Include="UUT01_TaskNN.cs" /> 임시 주석 처리 -->
     ```

Keep `UUT01_TaskNN.cs` on disk unless the user explicitly asks to delete it.

## Verified mapping from session
- `MFU_1` BIT: `UUT01_Task10`
  - `MFU_1Main_UUT01.cs`: `AddTask(UUT01_Task10)`
  - `MFU_1.csproj`: `<Compile Include="UUT01_Task10.cs" />`
- `MFU_2` BIT: `UUT01_Task10`
  - `MFU_2Main_UUT01.cs`: `AddTask(UUT01_Task10)`
  - `MFU_2.csproj`: `<Compile Include="UUT01_Task10.cs" />`
- `PA_2` BIT: `UUT01_Task18`
  - `PA_2Main_UUT01.cs`: `AddTask(UUT01_Task18)`
  - `PA_2.csproj`: `<Compile Include="UUT01_Task18.cs" />`

## Verification
1. Re-scan the edited files and confirm each target line is commented in both places.
2. For individual TPS project builds, inspect the csproj configuration before choosing Platform. Many ATESWLIB TPS csproj files define `OutputPath` only for `Debug|AnyCPU`; direct `Debug|x86` csproj builds can fail with BaseOutputPath/OutputPath even though the code is fine.
   - Direct project build: prefer `/p:Configuration=Debug /p:Platform=AnyCPU` when the csproj defines that condition.
   - Solution build: still verify `K2/K2.sln /p:Configuration=Debug /p:Platform=x86` when the change affects overall K2 delivery.
3. Report individual project results separately from solution build results.

## Pitfalls
- If only `AddTask` is commented, the task file still compiles and can break the build if it references stale helpers.
- If only the csproj include is commented, an existing compiled method may no longer be built, but the task registration can become a compile error if the main file still references `UUT01_TaskNN`.
- Do not treat `BaseOutputPath/OutputPath` on direct `Debug|x86` csproj build as a source regression. Check the csproj `PropertyGroup` platform conditions and retry with the defined platform, then run the full solution build separately.
- Build-generated `BIN/*`, `obj/*`, `.cache`, `.pdb`, and `.dll` noise should not be confused with the intentional source changes when preparing a report or commit.
