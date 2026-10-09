import sqlite3
from historian import DB_PATH

with sqlite3.connect(DB_PATH) as connection:
    print("\n=== WATER TANK SQL REPORT ===\n")

    # Total readings recorded
    result = connection.execute("""
        SELECT COUNT(*)
        FROM tank_readings
    """)
    print("Total readings:", result.fetchone()[0])

    # Water level statistics
    result = connection.execute("""
        SELECT
            ROUND(MIN(water_level), 2),
            ROUND(MAX(water_level), 2),
            ROUND(AVG(water_level), 2)
        FROM tank_readings
    """)
    minimum, maximum, average = result.fetchone()

    print("Minimum water level:", minimum)
    print("Maximum water level:", maximum)
    print("Average water level:", average)

    # Pump starts
    result = connection.execute("""
        SELECT COUNT(*)
        FROM pump_events
        WHERE event_type = 'ON'
    """)
    print("Pump starts:", result.fetchone()[0])

    # Recent pump events
    print("\nRecent pump events:")

    result = connection.execute("""
        SELECT timestamp, event_type, water_level
        FROM pump_events
        ORDER BY id DESC
        LIMIT 10
    """)

    for timestamp, event_type, level in result:
        print(f"{timestamp} | Pump {event_type} | {level:.1f}%")

print("\n=== PUMP RUNTIME ANALYSIS ===\n")

with sqlite3.connect(DB_PATH) as connection:
    result = connection.execute("""
        WITH pump_cycles AS (
            SELECT
                timestamp AS start_time,
                event_type,
                LEAD(timestamp) OVER (
                    ORDER BY id
                ) AS end_time,
                LEAD(event_type) OVER (
                    ORDER BY id
                ) AS next_event
            FROM pump_events
        )
        SELECT
            start_time,
            end_time,
            ROUND(
                (julianday(end_time) - julianday(start_time)) * 86400,
                1
            ) AS runtime_seconds
        FROM pump_cycles
        WHERE event_type = 'ON'
          AND next_event = 'OFF'
    """)

    for start, end, runtime in result:
        print(f"Started: {start}")
        print(f"Stopped: {end}")
        print(f"Runtime: {runtime} seconds\n")