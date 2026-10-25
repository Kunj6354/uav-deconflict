# UAV Deconflict

UAV Deconflict (CAN-069) is a Python system for **strategic preflight trajectory deconfliction**. It checks a planned UAV mission against simulated traffic before flight and reports where their paths violate a chosen separation buffer during overlapping time windows.

## Problem and supported scope

Paths can cross in space without creating a conflict if aircraft arrive at different times. This project builds time-parameterized trajectories, samples their overlapping intervals, and classifies the mission as `clear` or `conflict`.

The supported workflow includes validated primary-mission and simulated-traffic JSON inputs, mission-window and waypoint-timestamp handling, linear interpolation, a primary-mission speed constraint, configurable safety buffer and sampling interval, structured conflict reports, a CLI, JSON output, static and animated 2D output, an interactive 3D visualization utility, automated tests, and committed regression scenarios. The CLI checks horizontal (2D) separation; the Python core also accepts a `use_3d` option for Euclidean 3D separation.

## Non-goals

This is a preflight analysis tool. It does not ingest live telemetry, provide real-time tactical deconfliction, autonomously avoid conflicts, control aircraft, process WGS84/geodetic coordinates, expose a supported REST API or web frontend, or manage high-density production traffic.

## Coordinate and time model

Every input trajectory must use the **same local Cartesian frame**: `x` and `y` are horizontal coordinates in metres, and `z` is the vertical coordinate in metres. No latitude/longitude conversion or WGS84 transformation is performed. The CLI's default separation check uses `x/y`; callers of the Python core can request `x/y/z` distance.

The primary mission supplies an overall start/end time window. Its untimed waypoint times are distributed across that window in proportion to path length, subject to its optional `max_speed_mps` constraint. Simulated flights supply waypoint timestamps. Trajectory positions are linearly interpolated between waypoints. Passing another interpolation method raises `NotImplementedError` by design.

## Repository structure

```text
data/                         sample primary mission and simulated traffic
scenarios/                    clear/conflict references and regression runner
src/cli.py                    supported command-line workflow
src/deconflict/
  analyzer.py                 analysis orchestration
  io.py                       JSON loading and validation
  models.py                   mission, flight, and waypoint models
  spatial.py                  spatial utilities
  temporal.py                 sampled conflict detection and reporting
  traject.py                  trajectory construction and interpolation
  visualize.py                2D and interactive 3D visualization utilities
tests/                        automated tests
docs/                         project documentation and closure record
```

## Setup and verification

The accepted project environment uses **Python 3.13**. The dependency versions in `requirements.txt` are pinned to those used for acceptance. In PowerShell:

```powershell
git clone https://github.com/Kunj6354/uav-deconflict.git
cd uav-deconflict
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the automated tests and both committed scenario references:

```powershell
python -m pytest -q
python .\scenarios\run_all_scenarios.py
```

The accepted run passed **17/17 tests** and **2/2 scenarios**. `clear_reference` produced `clear` with 0 conflicts; `conflict_reference` produced `conflict` with 37 sampled conflict entries. Both CLI paths, JSON reports, and static/animated 2D output passed acceptance. The interactive 3D utility exists and is tested. See [completion closure](docs/COMPLETION_CLOSURE.md) for the acceptance record.

## CLI example

Run the clear sample from the repository root:

```powershell
python .\src\cli.py --primary .\data\sample_primary_mission.json --sim .\data\sample_simulated_flights.json --buffer 50 --dt 1 --out .\outputs\manual_report.json
```

The console prints:

```text
CLEAR
```

The JSON report has this shape:

```json
{
  "status": "clear",
  "conflicts": []
}
```

`--buffer` is the separation threshold in metres; `--dt` is the sampling step in seconds. The committed `conflict_reference.json` uses the same inputs and a 200 m buffer to exercise conflict detection and detailed reporting. Run the scenario command above to produce reports under `outputs/`, including `outputs/summary.csv`.

Add `--animate` to a CLI invocation to write `demo_paths.png` and `animation.mp4` in the current working directory. The interactive 3D plot is available through `src/deconflict/visualize.py`; it is not a CLI output option. Matplotlib uses the headless `Agg` backend, so file rendering does not require a display or Tcl/Tk. Generated reports and visualizations are ignored by Git and can be recreated.

## Scalability and historical API prototype

The engine samples overlapping time windows and compares the primary mission with simulated flights. It is intended for small, controlled preflight analyses; high-density fleet management would require further work such as candidate pruning, spatial indexing, temporal partitioning, and batching.

An earlier placeholder FastAPI `src/server.py` prototype was removed because its `/check` endpoint did not call the authoritative analysis engine. The supported interfaces are the CLI and Python core; there is no supported server runtime.

## License

No license file is currently present in this repository. Reuse permissions have not been specified.
