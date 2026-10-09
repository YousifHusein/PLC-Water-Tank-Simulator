
import struct
import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=1502)

if not client.connect():
    raise SystemExit("Connection failed")

try:
    # Convert 85.0 to two 16-bit registers
    value = 85.0
    registers = list(
        struct.unpack(">HH", struct.pack(">f", value))
    )

    print("Sending water level:", value)
    print("Register values:", registers)

    # Write to %MD0 using the simplified mapping
    write = client.write_registers(
        address=0,
        values=registers,
        device_id=1
    )

    print("Write response:", write)

    if write.isError():
        raise RuntimeError("Modbus write failed")

    time.sleep(1)

    # Read the same registers back
    read = client.read_holding_registers(
        address=0,
        count=2,
        device_id=1
    )

    if read.isError():
        raise RuntimeError(f"Read failed: {read}")

    print("Registers received:", read.registers)

    # Decode with both possible word orders
    high_first = struct.unpack(
        ">f", struct.pack(">HH", *read.registers)
    )[0]

    low_first = struct.unpack(
        ">f", struct.pack(">HH", *read.registers[::-1])
    )[0]

    print("Decoded high-first:", high_first)
    print("Decoded low-first:", low_first)

    # Read pump output
    pump = client.read_coils(
        address=0,
        count=1,
        device_id=1
    )

    if pump.isError():
        raise RuntimeError(f"Pump read failed: {pump}")

    print("Pump status:", pump.bits[0])

finally:
    client.close()
