# DevLib SPI/I2C common helper and verification

## When this applies
Use this note when the user asks to add SPI/I2C communication support to `C:\Users\yjs\Desktop\JAN\DevLib` in the same style as other DevLib IO protocol helpers.

## Durable implementation boundary
- Keep SPI/I2C additions project-neutral and vendor-free unless the user provides a specific controller/adapter SDK.
- Do not invent `DllImport`, native DLL names, or controller-specific open/read/write APIs for SPI/I2C.
- Put reusable protocol metadata, transfer containers, frame builders, address validation, bit/hex utilities under:
  - `DevLib\IO\SPI`
  - `DevLib\IO\I2C`
- Actual SPI controller transfer, I2C repeated-start execution, ACK/NACK retry, clock stretching, and device-specific register semantics belong in a controller-specific adapter or project ICD layer.

## Recommended file shape
SPI:
- `SpiEnums.cs`: mode, bit order, chip-select polarity.
- `SpiBusConfiguration.cs`: immutable clock/mode/bit order/CS/bits-per-word metadata.
- `SpiTransfer.cs`: immutable Tx data, read length, chip-select hold flag.
- `SpiCodec.cs`: create write/read/write-read transfers, register frame helpers, bit reverse, hex conversion.

I2C:
- `I2cEnums.cs`: address format and direction.
- `I2cTransfer.cs`: immutable slave address, direction, data, address format.
- `I2cCodec.cs`: 7-bit/10-bit address validation, address byte builders, read/write transfer builders, register frame helpers, hex conversion.

## Read.txt documentation pattern
For each protocol folder, provide `Read.txt` with:
1. 통신 특성
2. 주요 코드
3. 사용 예
4. 주의사항

For SPI/I2C specifically, state clearly that the implementation is a project-neutral helper and that real hardware bus operations must be supplied by a vendor/controller adapter.

## Verification pattern
Run and report all of these when practical:
1. `dotnet build DevLib/DevLib.csproj -c Debug --no-restore /v:minimal`
2. Visual Studio MSBuild for `DevLib/DevLib.csproj`, because JAN work often expects VS build confirmation too.
3. A temporary smoke console project that references DevLib and asserts:
   - SPI config and transfer creation.
   - SPI register read frame and bit-reverse behavior.
   - SPI hex round-trip.
   - I2C 7-bit address byte and 10-bit address bytes.
   - I2C register write/read-prefix helpers.
   - I2C read transfer and hex round-trip.
4. Search SPI/I2C source for `DllImport`, vendor names, and `.dll` to confirm no accidental native dependency was introduced.

## Reporting notes
- Separate existing DevLib warnings from new SPI/I2C compile errors.
- If the build succeeds with existing warnings, report `오류 0개` and summarize the warning class briefly rather than over-explaining all warnings.
- Include exact changed paths and the smoke-test result (`SPI/I2C smoke PASS`) in the final briefing.
