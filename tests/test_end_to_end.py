import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def cli_result(tmp_path: Path):
    report = tmp_path / "report.json"

    command = [
        sys.executable,
        "src/cli.py",
        "--primary",
        "data/sample_primary_mission.json",
        "--sim",
        "data/sample_simulated_flights.json",
        "--buffer",
        "50",
        "--dt",
        "1.0",
        "--out",
        str(report),
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return completed, report


def test_cli_run(cli_result):
    completed, report_path = cli_result

    assert completed.returncode == 0
    assert "clear" in completed.stdout.lower()
    assert report_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == "clear"
    assert isinstance(report["conflicts"], list)


def test_conflict_cli_report(tmp_path: Path):
    report_path = tmp_path / "conflict_report.json"

    completed = subprocess.run(
        [
            sys.executable,
            "src/cli.py",
            "--primary",
            "data/sample_primary_mission.json",
            "--sim",
            "data/sample_simulated_flights.json",
            "--buffer",
            "200",
            "--dt",
            "1.0",
            "--out",
            str(report_path),
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "conflict detected" in completed.stdout.lower()

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == "conflict"
    assert len(report["conflicts"]) >= 1
