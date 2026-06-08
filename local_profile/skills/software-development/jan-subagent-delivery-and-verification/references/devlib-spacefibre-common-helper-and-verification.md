# DevLib SpaceFibre common helper implementation and verification

Use this reference when the user asks to add SpaceFibre support to JAN DevLib or asks to implement another SpaceWire-adjacent protocol in the same vendor-free helper style.

## Durable lesson

For SpaceFibre in DevLib, do not invent real controller/link APIs unless the user provides a concrete FPGA/card/vendor SDK target. Keep the first reusable implementation as a project-neutral common helper: virtual-channel metadata, frame containers, packet segmentation/reassembly, broadcast payload helpers, sequence validation, hex utilities, and CRC helpers.

## Recommended implementation shape

Location:
- `DevLib/IO/SpaceFibre/`

Namespace:
- `DevLib.IO.SpaceFibre`

Recommended files/classes:
- `SpaceFibreEnums.cs`
  - `SpaceFibreFrameType`: `Data`, `Broadcast`, `FlowControl`, `LinkManagement`
  - `SpaceFibreFrameFlags`: `StartOfPacket`, `EndOfPacket`, `ErrorEnd`
- `SpaceFibreFrameHeader.cs`
  - virtual channel validation, sequence number, frame type, flags, payload length
  - helper byte encoding/parse for DevLib-internal verification metadata
- `SpaceFibreFrame.cs`
  - immutable frame container with cloned payload and `ToBytes()` round-trip support
- `SpaceFibreBroadcastMessage.cs`
  - event code + length + data payload helper
- `SpaceFibrePacketCodec.cs`
  - data frame creation, frame parse/try-parse
  - packet segmentation/reassembly
  - sequence wrap validation (`0xFE -> 0xFF -> 0x00`)
  - hex encode/decode helpers
- `SpaceFibreCrc.cs`
  - generic CRC-16/CCITT-FALSE utility for higher-level payloads
- `Read.txt`
  - communication characteristics, code map, usage example, and explicit hardware-scope caveat

## Scope boundaries

Allowed in DevLib common helper:
- virtual channel validation, normally 0..31
- frame metadata representation
- packet segmentation/reassembly
- sequence continuity and wrap checks
- broadcast/event payload helper
- deterministic helper byte encoding for smoke tests
- hex conversion
- generic CRC helpers for higher-level payload protection

Avoid unless a concrete project/vendor requirement exists:
- SpaceFibre controller open/close wrappers
- lane configuration, link startup, DMA, interrupt callbacks
- FDIR/QoS scheduling implementation
- FPGA register maps
- vendor SDK references (`Kaya`, `STAR-Dundee`, `4Links`, `NI`, native DLLs)
- mission-specific logical-address meanings or payload ICD rules

## Smoke verification pattern

Create a temporary console app referencing DevLib and verify:
- packet segmentation into multiple frames
- first/middle/last StartOfPacket and EndOfPacket flags
- sequence wrap, e.g. initial `0xFE` produces `0xFE, 0xFF, 0x00`
- reassembly returns the original packet bytes
- frame `ToBytes()` / `ParseFrame()` round-trip
- `TryParseFrame()` failure path returns `false + error`
- broadcast payload create/parse round-trip
- CRC-16/CCITT-FALSE known vector: ASCII `123456789` should be `0x29B1`
- invalid virtual channel such as `32` throws

Run both DevLib build styles:
- `dotnet build DevLib/DevLib.csproj -c Debug --no-restore /v:minimal`
- Visual Studio MSBuild on `DevLib/DevLib.csproj`

Also search the SpaceFibre folder for accidental native/vendor dependencies:
- `DllImport|Kaya|STAR|4Links|NationalInstruments|vendor|\.dll|PInvoke|Extern`

## Reporting pattern for this user

Separate the report into:
- implemented paths
- measured verification result: dotnet build, MSBuild, smoke test
- vendor/native dependency search result
- existing repository changes not caused by the current task
- residual risk: helper only; real SpaceFibre hardware/link/vendor integration is not implemented

Use the user's preferred `subagent 이름 : 내용` format, with Jangli for technical verification and Yuno for concise overall status.
