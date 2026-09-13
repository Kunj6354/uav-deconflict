from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "outputs"
SUMMARY_FILE = OUTPUT_DIR / "summary.csv"


def run_scenario(scenario_file: Path) -> dict[str, object]:
    with scenario_file.open("r", encoding="utf-8") as f:
        scenario = json.load(f)

    output_dir = OUTPUT_DIR / scenario_file.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / "report.json"

    command = [
        sys.executable,
        str(REPO_ROOT / "src" / "cli.py"),
        "--primary",
        str(REPO_ROOT / scenario["primary_mission_file"]),
        "--sim",
        str(REPO_ROOT / scenario["simulated_flights_file"]),
        "--buffer",
        str(scenario.get("buffer", 50)),
        "--dt",
        str(scenario.get("dt", 1.0)),
        "--out",
        str(report_file),
    ]

    if scenario.get("animate", False):
        command.append("--animate")

    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    with report_file.open("r", encoding="utf-8") as f:
        report = json.load(f)

    actual_status = report["status"]
    expected_status = scenario["expected_status"]

    if actual_status != expected_status:
        raise RuntimeError(
            f"{scenario_file.name}: expected {expected_status!r}, "
            f"got {actual_status!r}. stdout={completed.stdout!r}"
        )

    conflicts = report.get("conflicts", [])

    return {
        "scenario": scenario_file.stem,
        "expected_status": expected_status,
        "actual_status": actual_status,
        "conflict_count": len(conflicts),
        "report": str(report_file.relative_to(REPO_ROOT)),
        "passed": True,
    }


def run_all_scenarios() -> list[dict[str, object]]:
    scenario_files = sorted(SCENARIOS_DIR.glob("*.json"))

    if not scenario_files:
        raise RuntimeError("No committed scenario JSON files were found.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_data = [
        run_scenario(scenario_file)
        for scenario_file in scenario_files
    ]

    pd.DataFrame(summary_data).to_csv(SUMMARY_FILE, index=False)

    for item in summary_data:
        print(
            f"PASS {item['scenario']}: "
            f"{item['actual_status']} "
            f"(conflicts={item['conflict_count']})"
        )

    print(f"Scenario regression: {len(summary_data)}/{len(summary_data)} PASS")
    return summary_data


if __name__ == "__main__":
    run_all_scenarios()
