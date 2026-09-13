# Demo Script and Shot List (No Voiceover)

Suggested 3-4 minute demonstration of the supported strategic preflight workflow. Use short on-screen captions.

## 1. Objective (0:00-0:20)

Show the title **UAV Deconflict** and a simple diagram of a planned path crossing simulated traffic. Caption: "Check a planned mission against scheduled flight paths before takeoff."

## 2. Inputs and project structure (0:20-0:50)

Show `data/sample_primary_mission.json`, `data/sample_simulated_flights.json`, and the `src/deconflict/` modules. Note that all paths use one local Cartesian `x/y/z` frame in metres; the tool does not convert latitude/longitude.

## 3. Clear run (0:50-1:35)

From the repository root, run:

```powershell
python .\src\cli.py --primary .\data\sample_primary_mission.json --sim .\data\sample_simulated_flights.json --buffer 50 --dt 1 --out .\outputs\demo_clear.json
```

Show `CLEAR` in the terminal and the JSON report with `"status": "clear"` and an empty conflicts list.

## 4. Conflict regression (1:35-2:20)

Run:

```powershell
python .\scenarios\run_all_scenarios.py
```

Show the two passing reference scenarios and `outputs/conflict_reference/report.json`. The conflict reference reuses the same traffic with a 200 m buffer and produces 37 sampled conflict entries in the accepted environment. Point out flight identity, sampled time, and separation in one entry.

## 5. Visualization and limits (2:20-3:20)

Run the CLI command from section 3 with `--animate` added to generate `demo_paths.png` and `animation.mp4`. Show the static path view and a short animation excerpt. Mention that the CLI checks horizontal separation and that an interactive 3D visualization utility exists in the Python package. Close by stating that this is a preflight tool, not a live telemetry or flight-control system.
