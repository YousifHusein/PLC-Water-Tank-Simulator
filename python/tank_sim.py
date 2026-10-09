import struct
import time

from pymodbus.client import ModbusTcpClient


def float_to_registers(value):
    packed = struct.pack(">f", value)
    return list(struct.unpack(">HH", packed))


def write_water_level(client, level):
    registers = float_to_registers(level)

    return client.write_registers(
        address=0,
        values=registers,
        device_id=1
    )


client = ModbusTcpClient("127.0.0.1", port=1502)

if not client.connect():
    print("Could not connect to OpenPLC.")
    raise SystemExit

water_level = 20.0

print("Water Tank Simulation Started. Press Ctrl+C to stop.\n")

try:
    while True:
        # Send water level to OpenPLC
        response = write_water_level(client, water_level)

        if response.isError():
            raise RuntimeError(f"Write failed: {response}")

        time.sleep(0.1)

        # Read pump output from OpenPLC
        result = client.read_coils(
            address=0,
            count=1,
            device_id=1
        )

        if result.isError():
            raise RuntimeError(f"Read failed: {result}")

        pump_on = result.bits[0]

        # Simulate tank filling or draining
        if pump_on:
            water_level += 5.0
        else:
            water_level -= 2.0

        # Keep water level between 0% and 100%
        water_level = max(0.0, min(100.0, water_level))

        print(
            f"Water Level: {water_level:5.1f}% | "
            f"Pump: {'ON' if pump_on else 'OFF'}"
        )

        time.sleep(1)

except KeyboardInterrupt:
    print("\nSimulation stopped.")

finally:
    client.close()
