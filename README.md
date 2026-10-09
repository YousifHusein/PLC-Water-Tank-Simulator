# PLC Water Tank Simulator

An automated water tank control system built using OpenPLC ladder logic, Python, Modbus TCP, and SQLite. The project simulates a water tank filling and draining while a PLC controls the pump based on predefined water-level thresholds.

A SQL historian records process measurements and pump events for historical analysis.

## Technologies

- **OpenPLC** — PLC ladder logic and control
- **Python** — Tank simulation and Modbus communication
- **Modbus TCP** — Data exchange between Python and OpenPLC
- **SQLite** — Process historian and event logging
- **SQL** — Historical data queries and pump runtime analysis

## System Overview

The system uses hysteresis control to maintain the water level between two thresholds:

- **Low threshold (30%):** Start the pump when the water level falls below 30%.
- **High threshold (80%):** Stop the pump when the water level reaches 80%.
- **Between thresholds:** Maintain the previous pump state to prevent frequent switching.

The Python simulator communicates with OpenPLC through Modbus TCP. It writes the simulated water level to the PLC and reads the pump output to determine whether the tank should fill or drain.

## Simulation Logic

1. Initialize the tank at 20% capacity.
2. Send the water level to OpenPLC over Modbus TCP.
3. Read the pump output from the PLC.
4. Increase the water level by 5% per cycle when the pump is ON.
5. Decrease the water level by 2% per cycle when the pump is OFF.
6. Record the water level and pump status in SQLite.
7. Record pump ON/OFF transitions in a separate event table.

The simulation repeats automatically until stopped.

## PLC Variable Mapping

| Variable | Type | Address | Description |
|---|---|---|---|
| Water_Level | REAL | %MD0 | Simulated tank level |
| Low_Level | BOOL | Internal | Low-level condition |
| High_Level | BOOL | Internal | High-level condition |
| Pump | BOOL | %QX0.0 | Pump output |

## Running the Project

**Requirements**

- Python 3
- PyModbus 3.15.0
- OpenPLC Editor and a running compatible OpenPLC runtime

Load and run the PLC program in OpenPLC. The simulator expects Modbus TCP access at `127.0.0.1:1502`.

Install the Python dependency:

```bash
python -m pip install pymodbus==3.15.0
```

Start the simulation from the repository root:

```bash
python python/tank_sim.py
```

Run the SQL analysis report:

```bash
python python/analyze_history.py
```

The SQLite database is created automatically by the historian.

## Future Improvements

- Develop an HMI for real-time water-level monitoring.
- Add alarm handling for abnormal process conditions.
- Display historical trends and pump runtime statistics in a dashboard.
