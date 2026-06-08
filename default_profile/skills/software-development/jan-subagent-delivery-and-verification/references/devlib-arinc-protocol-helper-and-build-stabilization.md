# DevLib ARINC common protocol helpers and build stabilization

## When this applies
- User asks to add ARINC664, ARINC717, ARINC629, or another avionics protocol module "the same way" as an existing DevLib ARINC module.
- DevLib full build is blocked by unrelated external equipment/video/COM dependencies while the requested protocol helper code is project-neutral.

## Durable approach
1. Re-measure existing structure first.
   - Search under `DevLib\IO` for existing `Arinc*` folders and classes.
   - Confirm whether vendor headers/native DLLs exist. Do not invent P/Invoke signatures without vendor headers.
2. Keep DevLib project-neutral.
   - If no vendor SDK/header exists, add protocol helper classes rather than fake hardware wrappers.
   - Put only reusable validation/packing/parsing helpers in DevLib.
   - Keep equipment-specific ICD meanings, BIT decisions, TPSData labels, and task flow in the consuming project.
3. Recommended namespace/file shape.
   - `DevLib\IO\Arinc664\CArinc664.cs` -> `DevLib.Commu.Arinc664.CArinc664`
   - `DevLib\IO\Arinc717\CArinc717.cs` -> `DevLib.Commu.Arinc717.CArinc717`
   - `DevLib\IO\Arinc629\CArinc629.cs` -> `DevLib.Commu.Arinc629.CArinc629`
4. Smoke verification before full build.
   - Create a temporary minimal console project and link only the new/changed `.cs` files.
   - Exercise representative validation/pack/unpack calls.
   - This proves the requested common modules compile independently from external equipment dependencies.
5. Full DevLib build stabilization.
   - Prefer restoring missing vendor references when the user needs those features included.
   - If the immediate goal is to make the common library build in the current environment, conditionally exclude unrelated external-dependent folders in `DevLib.csproj` instead of adding stubs that could mask runtime behavior.
   - Known external-dependent folders that may block net6.0 builds in this repo:
     - `3ThirdParty\OpenCV\**` (`OpenCvSharp`, `Mat`, `Scalar`)
     - `Device\Advantech\**` (`Advantech.Adam`, `Adam4000Config`)
     - `Device\FrameLink\**` (`Imperx.FLExGrabber`, `VCECLB_*`)
     - `IO\CAN\UCAN\**` (UCAN vendor API)
     - `3ThirdParty\HighPrecisionTimer\**` if platform-specific timer dependencies are missing
   - For `dotnet build`, .NET Core MSBuild does not support `ResolveComReference`; condition COM references on `$(MSBuildRuntimeType) != 'Core'` and exclude COM-dependent source such as `Utiliy\WebPage\**` only for Core MSBuild.
6. Verify both build paths if available.
   - `MSYS2_ARG_CONV_EXCL='*' dotnet build DevLib/DevLib.csproj -c Debug --no-restore /v:minimal`
   - `MSYS2_ARG_CONV_EXCL='*' 'C:/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe' DevLib/DevLib.csproj /p:Configuration=Debug /m /v:minimal`
   - In Git Bash, use `MSYS2_ARG_CONV_EXCL='*'` when passing MSBuild slash switches or `/v:minimal`; otherwise MSYS path conversion can turn switches into extra project arguments.

## Reporting
- Separate "compiled successfully" from "feature included".
- If folders were excluded to pass the build, explicitly list the excluded capabilities and state that those runtime features are not included in the produced DLL until vendor dependencies are restored.
- Report the produced DLL path and the exact build command/result.

## Pitfalls
- Do not claim ARINC664/717/629 hardware wrappers were implemented unless actual native SDK signatures were verified.
- Do not place platform/project-specific BIT or ICD interpretation inside DevLib helper classes.
- Do not leave `dotnet build` broken after fixing Visual Studio MSBuild if the user asked broadly for "빌드 되게"; verify both when feasible.
