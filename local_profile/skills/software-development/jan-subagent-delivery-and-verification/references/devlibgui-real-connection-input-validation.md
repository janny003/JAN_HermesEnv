# DevLibGUI real connection input validation

Use this note when DevLibGUI is being used as a real `DevLib.dll` communication validation screen, not only as a static API coverage display.

## Session learning
A DevLibGUI communication screen that only lists API names is insufficient when the user asks whether the DLL functions actually work. The UI must expose the runtime parameters needed by each protocol and connect those parameters to the corresponding `DevLib.dll` public calls where safe.

## Required UI/input coverage
- TCP: Host, Port, Message
  - Map to `CTCPClient.Instance.Connect(host, port)`, `SendData(message)`, `Close()`.
- UDP: Host, Port, Message
  - Map to `CUDPClient.Instance.Open(host, port)`, `SendMessage(message)`.
- Serial: Port, Baud, DataBits, Parity, StopBits
  - Map to `CSerial.Instance.OpenPort(portName, baud, parity, dataBits, stopBits)`, `ClosePort()`.
- CAN: Kvaser Channel, CAN ID, Data Hex, Filter, Virtual
  - Show the intended `Open(channel, filter, virtualPort)` and `Send((int)canId, data)` mapping.
  - Do not report this as a hardware communication PASS unless the Kvaser/UCAN driver and device/virtual channel are actually available and exercised.
- ARINC429: Card, Tx, Rx, Data Word
  - Map attempted flow to `Open(card)`, `DOEnableTx(card, tx, 1)`, `DOEnableRx(card, rx, 1)`, `DOLoadTxQueueOne(card, tx, word)`, `DOReadRxQueueIrigOne(card, rx)`, `DOFreeCard(card)`.
  - Do not overstate success without the DDC/native hardware environment.

## Implementation guidance
1. Keep deterministic helper validation tabs/blocks intact; add real-connection input groups separately for hardware-facing communication types.
2. Prefer clear `TryParse`/validation messages for host/port/channel/hex inputs before calling DevLib APIs.
3. For hardware/vendor-bound protocols, distinguish these states in both UI and report:
   - API mapping/input validation confirmed
   - call attempted but device/driver unavailable
   - actual hardware communication passed
4. Keep Korean labels intact and verify no replacement characters after editing.

## Verification checklist
- Build `DevLib`.
- Build `DevLibGUI`.
- Launch-smoke the WPF app and confirm it does not immediately crash.
- Search edited XAML/C# for replacement characters (`�`).
- Report the changed files, exact callable mappings, build result, launch-smoke result, and any remaining hardware dependency risk.
