# DevLib SpaceWire common helper implementation and verification

Use this reference when the user asks to add SpaceWire support to JAN DevLib or a similar project-neutral protocol helper.

## Durable lesson

For DevLib protocol additions, keep the boundary as a reusable common helper unless a real vendor SDK/integration target is explicitly provided. Do not invent hardware Open/Close, Tx/Rx, DMA, interrupt, or P/Invoke APIs for SpaceWire.

## Recommended implementation shape

Location:
- `DevLib/IO/SpaceWire/`

Namespace:
- `DevLib.IO.SpaceWire`

Recommended files/classes:
- `SpaceWireEnums.cs`
  - `SpaceWirePacketEndMarker`: `None`, `Eop`, `Eep`
  - `SpaceWireControlCode`: abstract helper identifiers for `Fct`, `Eop`, `Eep`, `Escape`, `Null`, `TimeCode`
  - `SpaceWireControlCodes`: classification/conversion helpers
- `SpaceWireToken.cs`
  - distinguish payload data bytes from abstract control tokens so data byte values `0x00..0xFF` do not collide with EOP/EEP semantics
- `SpaceWirePacket.cs`
  - immutable payload container with cloned byte arrays and end marker state
- `SpaceWirePacketCodec.cs`
  - encode/decode packet tokens
  - parse multiple packet frames from a token stream
  - `TryParse` path that returns `false + error` rather than throwing
  - address/cargo join/split helpers
  - hex encode/decode helpers accepting spacing separators if desired
- `SpaceWireCrc.cs`
  - generic CRC-8 utility only; document that SpaceWire packet framing itself has no universal packet-level CRC
- `SpaceWireTimeCode.cs`
  - six-bit time value `0..63` plus two control flags

## Scope boundaries

Allowed in DevLib common helper:
- packet framing representation
- EOP/EEP handling
- token stream parsing
- byte payload round-trip
- path/logical address utility functions
- hex conversion
- CRC-8 utility for higher-level protocols such as RMAP
- time-code encode/decode representation

Avoid unless a concrete project/vendor requirement exists:
- SpaceWire card/link open-close wrappers
- link speed configuration
- DMA/interrupt callbacks
- vendor SDK references (`Kaya`, `STAR-Dundee`, `4Links`, `NI`, native DLLs)
- mission-specific ICD address meanings
- RMAP transaction scheduling/retry/device register semantics

## Smoke verification pattern

Run both build styles when DevLib is involved:
- `dotnet build DevLib/DevLib.csproj -c Debug --no-restore /v:minimal`
- Visual Studio MSBuild on `DevLib/DevLib.csproj`

Also create or run a small independent smoke app referencing DevLib and check:
- EOP frame round-trip
- EEP frame round-trip
- full byte range payload `0x00..0xFF` round-trip
- multiple packet stream parse, including recovery after EEP
- missing terminator rejected by `TryParse`
- address/cargo split correctness
- hex encode/decode deterministic output
- CRC-8 known vector: ASCII `123456789` with polynomial `0x07`, initial `0x00`, xorOut `0x00` should be `0xF4`
- time-code round-trip at boundary value `63`

## Reporting pattern for this user

When reporting, separate:
- implemented paths
- measured verification result: dotnet build, MSBuild, smoke test
- existing repository changes not caused by the current task
- residual risk: helper only, hardware/vendor integration not implemented

Keep the response concise and in the user's preferred subagent-name format when applicable.
