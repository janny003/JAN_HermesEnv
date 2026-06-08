# DevLib vendor reference and native DLL build stabilization

Use when DevLib builds fail after re-enabling hardware/vendor folders such as Advantech, FrameLink, UCAN, OpenCV, ARINC429, or when runtime native DLLs are not copied beside `DevLib.dll`.

## Durable pattern

1. Reproduce with both build paths:
   - `dotnet build DevLib/DevLib.csproj -c Debug --no-restore /v:minimal`
   - Visual Studio MSBuild, for example `MSBuild.exe DevLib/DevLib.csproj /p:Configuration=Debug /m /v:minimal`
2. Search the repository for vendor DLLs before excluding source folders. In this codebase, many hardware SDK DLLs are already checked in under `DevLib/DevLib/.../bin` or `Lib` folders.
3. Add managed wrapper DLLs as `<Reference Include=...><HintPath>...</HintPath></Reference>`.
4. Add native dependency DLLs as `<None Include=... CopyToOutputDirectory="PreserveNewest" TargetPath="file.dll" />` so they land at the output root beside `DevLib.dll`, not nested under their source path.
5. Re-run both build paths and grep logs for unresolved references/errors, not only exit code.
6. Verify output root contains required native DLLs.

## Managed references recovered in the session

These were needed when restoring previously excluded folders:

- `Advantech.Adam` -> `Device\Advantech\bin\Advantech.Adam.DLL`
- `Advantech.Common` -> `Device\Advantech\bin\Advantech.Common.DLL`
- `Advantech.Graph` -> `Device\Advantech\bin\Advantech.Graph.dll`
- `Advantech.Protocol` -> `Device\Advantech\bin\Advantech.Protocol.DLL`
- `Automation.BDaq4` -> `Device\Advantech\bin\Automation.BDaq4.dll`
- `FLExGrabber` -> `Device\FrameLink\bin\x64\Release\FLExGrabber.dll`
- `OpenCvSharp` -> `3ThirdParty\OpenCV\Bin\x64\OpenCvSharp.dll`
- `OpenCvSharp.Extensions` -> `3ThirdParty\OpenCV\Bin\x64\OpenCvSharp.Extensions.dll`

## Native DLLs that must be copied to output root

Use explicit `TargetPath` to avoid nested output locations:

```xml
<ItemGroup>
  <None Include="IO\CAN\bin\uCANDLL.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="uCANDLL.dll" />
  <None Include="IO\Arinc429\Lib\x64\Release\DD42992.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="DD42992.dll" />
  <None Include="3ThirdParty\OpenCV\Bin\x64\OpenCvSharpExtern.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="OpenCvSharpExtern.dll" />
  <None Include="Device\FrameLink\bin\x64\Release\VCECLB.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="VCECLB.dll" />
  <None Include="Device\FrameLink\bin\x64\Release\IpxTrueSense.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="IpxTrueSense.dll" />
  <None Include="Device\FrameLink\bin\x64\Release\ippLib.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="ippLib.dll" />
  <None Include="Device\FrameLink\bin\x64\Release\ipxdemosaicing.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="ipxdemosaicing.dll" />
  <None Include="Device\FrameLink\bin\x64\Release\libiomp5md.dll" CopyToOutputDirectory="PreserveNewest" TargetPath="libiomp5md.dll" />
</ItemGroup>
```

## Core MSBuild compatibility notes

- COM references such as `SHDocVw` should be conditioned out for `MSBuildRuntimeType == Core` when using `dotnet build`.
- WebBrowser/COM dependent source folders such as `Utiliy\WebPage\**` may need to be removed only for Core MSBuild while staying available for Visual Studio MSBuild.
- Avoid broad permanent exclusion of hardware folders simply to silence missing references; first locate and add the vendor DLLs.

## Verification checklist

After the fix, confirm:

- `dotnet build` exits 0 and shows `오류 0개`.
- Visual Studio MSBuild exits 0 and emits `DevLib -> ...\DevLib.dll`.
- No `MSB3245`, `could not resolve`, `확인할 수 없습니다`, `not found`, or `error` lines remain in build logs.
- Output root contains `uCANDLL.dll`, `DD42992.dll`, `OpenCvSharpExtern.dll`, and FrameLink native DLL dependencies.
