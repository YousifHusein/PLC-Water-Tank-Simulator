import struct, time
from pymodbus.client import ModbusTcpClient

c = ModbusTcpClient("127.0.0.1", port=1502)
c.connect()

hi, lo = struct.unpack(">HH", struct.pack(">f", 85.0))
print("write:", c.write_registers(address=2048, values=[lo, hi], device_id=1))
time.sleep(2)
print("HR 2048-2049:", c.read_holding_registers(address=2048, count=2, device_id=1).registers)
print("Pump coil 0:", c.read_coils(address=0, count=1, device_id=1).bits[0])
c.close()