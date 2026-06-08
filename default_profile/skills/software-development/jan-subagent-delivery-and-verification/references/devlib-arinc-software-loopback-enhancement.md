# DevLib ARINC629/664/717 software-loopback enhancement

## When this applies
- User asks to raise ARINC629, ARINC664/AFDX, or ARINC717 completeness to be closer to ARINC429 in DevLib.
- Vendor SDK/header/API documentation is not available for those protocols.
- The goal is to make consuming JAN projects able to validate Open/Enable/Load/Read flow and parser integration without claiming real hardware communication.

## Durable approach
1. Re-measure protocol files first.
   - Check `DevLib\IO\Arinc629\CArinc629.cs`, `Arinc664\CArinc664.cs`, and `Arinc717\CArinc717.cs`.
   - Confirm whether native SDK/header/DLL exists. Do not invent P/Invoke signatures without vendor signatures.
2. If no vendor SDK is present, implement a deterministic software-loopback channel rather than fake hardware wrappers.
   - Add 429-like API shape: `Open`, `Close`, `EnableTx`, `EnableRx`, `GetRxQueueStatus`, queue load, queue read, and `ClearQueues`.
   - Keep return policy simple and explicit: `0` success for command-like methods, positive read/count for queue methods, `-1` for invalid state/input where appropriate.
   - Preserve protocol helper functions already present.
3. Protocol-specific helper scope.
   - ARINC629: 20-bit word normalize/validate, label/data build/extract, 3-byte pack/unpack, terminal-id guarded software queue.
   - ARINC664/AFDX: VL-id guarded software queue, Ethernet frame build/parse/validate, multicast MAC build/VL extraction, sequence next/expected-next helpers.
   - ARINC717: stream-id guarded software queue, 12-bit word pack/unpack/sign extend, sync word helpers, subframe build/split helpers.
4. Documentation.
   - Update each `Read.txt` to clearly state the current scope: software loopback + project-neutral helper.
   - Explicitly state that real card/NIC/stream open/read/write still requires vendor adapter integration.
5. Verification.
   - Run `dotnet build DevLib.sln -c Debug --no-restore /v:minimal`.
   - Run Visual Studio MSBuild if available.
   - Create a temporary console smoke that references `DevLib.csproj` and exercises:
     - ARINC629 `Open -> EnableTx/Rx -> LoadTxQueueOne -> GetRxQueueStatus -> ReadRxQueueOne` plus build/extract/pack/unpack.
     - ARINC664 `Open -> EnableTx/Rx -> LoadTxPayload/Frame -> ReadRxFrame` plus frame parse, VL extraction, sequence helper.
     - ARINC717 `Open -> EnableTx/Rx -> BuildSubframe -> LoadTxWords -> ReadRxWords` plus split subframe, pack/unpack, sign extension.
   - Include negative checks where possible: wrong id, disabled TX, empty read, close mismatch.
6. QA reporting.
   - If the user asks for Lucy, run or delegate an independent smoke check and report `Lucy : ...` with normal flow and edge/failure checks.

## Pitfalls
- Do not describe ARINC629/664/717 as real hardware wrappers unless real vendor signatures were verified and integrated.
- Software loopback raises testability and API completeness but does not prove card-level bus communication.
- Keep equipment-specific ICD meaning, payload scaling, BAG/redundancy, terminal scheduling, and frame maps outside DevLib unless the user provides project-specific requirements.
- After adding loopback APIs, verify both compile and behavior; compile-only is insufficient for this class of change.
