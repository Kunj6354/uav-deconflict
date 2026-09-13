# Design Reflection: UAV Deconflict

## Design and tradeoffs

The project separates JSON loading and validation (`io.py`, `models.py`), trajectory construction (`traject.py`), overlap and distance checks (`temporal.py`), orchestration (`analyzer.py`), and output (`cli.py`, `visualize.py`). This keeps the strategic preflight analysis testable without a server or live traffic source.

The primary mission provides a time window. Its waypoint times are allocated in proportion to path distance, with an optional `max_speed_mps` check. Simulated traffic provides timestamped waypoints. Linear interpolation defines positions between waypoints; other interpolation methods are deliberately unsupported.

The conflict checker samples the shared time interval for each primary/simulated pair at the chosen `dt`. It flags a sample when distance is strictly less than the safety buffer and records a conflict entry with flight identity, time, positions, and separation. The CLI uses horizontal `x/y` distance. The Python core can use `x/y/z` distance through `use_3d=True`. All coordinates must already be in the same local Cartesian frame in metres.

## Verification

The accepted Python 3.13 environment passed 17/17 automated tests and both committed scenario references. The 50 m reference was clear with zero conflicts; the 200 m reference detected 37 sampled conflict entries. CLI execution, JSON reporting, and static/animated 2D rendering passed acceptance. The interactive 3D visualization utility is tested. The authoritative acceptance details are in [Completion Closure](COMPLETION_CLOSURE.md).

## Limits and future enhancements

Sampling resolution affects which short-lived proximity events can be observed. The present design compares one primary mission against a set of simulated flights and is intended for controlled preflight analysis. It does not ingest live telemetry, perform autonomous avoidance or flight control, transform WGS84 coordinates, expose a supported REST API, or claim production-scale traffic management. Candidate pruning, spatial and temporal indexing, uncertainty models, and fleet-scale operation would be separate enhancement milestones.
