# PLC Water Tank Simulator

A water tank level-control simulation built using OpenPLC ladder logic and Python. The PLC controls a pump based on the tank's water level, while a Python script simulates the filling and draining process through Modbus TCP communication.

## Overview

The system maintains the tank's water level using two thresholds:

- **Below 30%:** Turn the pump ON to refill the tank.
- **At 80%:** Turn the pump OFF to prevent overfilling.
- **Between thresholds:** Maintain the previous pump state.

This creates hysteresis, preventing the pump from rapidly switching on and off near a single threshold.

## Technologies

- **OpenPLC** — PLC programming and ladder logic
- **Python** — Water tank simulation
- **Modbus TCP** — Communication between Python and OpenPLC
- **PyModbus** — Python Modbus client library

## How It Works

1. Python initializes the simulated tank at 20%.
2. The current water level is converted into two 16-bit Modbus registers and sent to OpenPLC.
3. The PLC evaluates the water level and controls the pump using ladder logic.
4. Python reads the pump output through Modbus TCP.
5. When the pump is ON, the simulated water level increases by 5% per cycle.
6. When the pump is OFF, the simulated water level decreases by 2% per cycle.

The process repeats continuously, demonstrating automatic pump control.

## PLC I/O Mapping

| Variable | Type | Location | Description |
|---|---|---|---|
| Water_Level | REAL | %MD0 | Current simulated tank level |
| Low_Level | BOOL | Internal | Low-level condition |
| High_Level | BOOL | Internal | High-level condition |
| Pump | BOOL | %QX0.0 | Pump control output |

## Running the Simulation

**Requirements:** Python, PyModbus, and a running OpenPLC runtime with the water tank program loaded.

Install PyModbus:

```bash
python -m pip install pymodbus==3.15.0
```

The Python simulator connects to OpenPLC at `127.0.0.1:1502`. Make sure the runtime is accessible at this address and port.

Start the simulation:

```bash
cd python
python tank_sim.py
```

Press `Ctrl+C` to stop.

## Future Improvements

- Add an HMI to visualize the water level and pump status.
- Implement high- and low-level alarms.
- Add sensor fault detection and additional operator controls.
