#!/usr/bin/env python3
"""Aggregate individual run results into benchmark summary statistics.

Reads grading.json files from run directories and produces:
- run_summary with mean, stddev, min, max for each metric
- delta between with_skill and without_skill configurations

Usage:
    py -m scripts.aggregate_benchmark <benchmark_dir> --skill-name <name>

Supports workspace layout:
    <benchmark_dir>/
    └── eval-N/
        ├── with_skill/
        │   ├── grading.json
        │   └── timing.json
        └── without_skill/
            ├── grading.json
            └── timing.json

Windows: Always use `py` not `python` or `python3`.
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def calculate_stats(values):
    """Calculate mean, stddev, min, max for a list of values."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_run_results(benchmark_dir):
    """Load all run results from a benchmark directory.

    Returns dict keyed by config name (e.g. "with_skill"/"without_skill"),
    each containing a list of run results.
    """
    benchmark_dir = Path(benchmark_dir)
    configs = {}

    # Discover eval directories
    eval_dirs = sorted([
        d for d in benchmark_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

    for eval_dir in eval_dirs:
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            config_name = config_dir.name
            if config_name not in configs:
                configs[config_name] = []

            # Check for grading.json directly or in subdirectories (run-N/)
            grading_files = list(config_dir.glob("**/grading.json"))
            if not grading_files:
                continue

            for grading_file in grading_files:
                try:
                    grading = json.loads(grading_file.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError) as e:
                    print("[WARNING] Failed to read {}: {}".format(grading_file, e), file=sys.stderr)
                    continue

                # Load timing if available
                timing_file = grading_file.parent / "timing.json"
                timing = {}
                if timing_file.exists():
                    try:
                        timing = json.loads(timing_file.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, OSError):
                        pass

                summary = grading.get("summary", {})
                run_result = {
                    "eval_dir": eval_dir.name,
                    "config": config_name,
                    "pass_rate": summary.get("pass_rate", 0.0),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "total": summary.get("total", 0),
                    "time_seconds": timing.get("total_duration_seconds", 0),
                    "tokens": timing.get("total_tokens", 0),
                    "expectations": grading.get("expectations", []),
                }

                # Calculate pass_rate if not present
                if run_result["total"] > 0 and run_result["pass_rate"] == 0.0:
                    run_result["pass_rate"] = run_result["passed"] / run_result["total"]

                configs[config_name].append(run_result)

    return configs


def aggregate(benchmark_dir, skill_name=None):
    """Produce benchmark.json from run results."""
    benchmark_dir = Path(benchmark_dir)
    configs = load_run_results(benchmark_dir)

    if not configs:
        print("[ERROR] No run results found in {}".format(benchmark_dir), file=sys.stderr)
        sys.exit(1)

    # Build runs array
    runs = []
    run_number_counter = {}
    for config_name, results in configs.items():
        for r in results:
            key = (r["eval_dir"], config_name)
            run_number_counter[key] = run_number_counter.get(key, 0) + 1

            runs.append({
                "eval_id": r["eval_dir"],
                "eval_name": r["eval_dir"],
                "configuration": config_name,
                "run_number": run_number_counter[key],
                "result": {
                    "pass_rate": round(r["pass_rate"], 4),
                    "passed": r["passed"],
                    "failed": r["failed"],
                    "total": r["total"],
                    "time_seconds": r["time_seconds"],
                    "tokens": r["tokens"],
                },
                "expectations": r["expectations"],
            })

    # Build run_summary
    run_summary = {}
    for config_name, results in configs.items():
        run_summary[config_name] = {
            "pass_rate": calculate_stats([r["pass_rate"] for r in results]),
            "time_seconds": calculate_stats([r["time_seconds"] for r in results]),
            "tokens": calculate_stats([r["tokens"] for r in results]),
        }

    # Calculate delta if both configs exist
    config_names = list(configs.keys())
    if len(config_names) >= 2:
        c1, c2 = config_names[0], config_names[1]
        delta = {
            "pass_rate": "+{:.4f}".format(
                run_summary[c1]["pass_rate"]["mean"] - run_summary[c2]["pass_rate"]["mean"]
            ),
            "time_seconds": "+{:.1f}".format(
                run_summary[c1]["time_seconds"]["mean"] - run_summary[c2]["time_seconds"]["mean"]
            ),
            "tokens": "+{:.0f}".format(
                run_summary[c1]["tokens"]["mean"] - run_summary[c2]["tokens"]["mean"]
            ),
        }
        run_summary["delta"] = delta

    benchmark = {
        "metadata": {
            "skill_name": skill_name or "unknown",
            "skill_path": str(benchmark_dir),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "runs_per_configuration": max(len(r) for r in configs.values()) if configs else 0,
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": [],
    }

    return benchmark


def main():
    parser = argparse.ArgumentParser(description="Aggregate run results into benchmark statistics")
    parser.add_argument("benchmark_dir", help="Path to benchmark/iteration directory")
    parser.add_argument("--skill-name", default=None, help="Skill name for metadata")
    parser.add_argument("-o", "--output", default=None, help="Output JSON file (default: benchmark.json in dir)")
    args = parser.parse_args()

    benchmark = aggregate(args.benchmark_dir, args.skill_name)

    output_path = args.output or str(Path(args.benchmark_dir) / "benchmark.json")
    Path(output_path).write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    print("[OK] Benchmark written to {}".format(output_path), file=sys.stderr)

    # Also write markdown summary
    md_path = str(Path(output_path).with_suffix(".md"))
    md_lines = ["# Benchmark Summary\n"]
    for config_name, stats in benchmark["run_summary"].items():
        if config_name == "delta":
            continue
        md_lines.append("## {}\n".format(config_name))
        for metric, values in stats.items():
            md_lines.append("- **{}**: {:.4f} +/- {:.4f} (min={:.4f}, max={:.4f})\n".format(
                metric, values["mean"], values["stddev"], values["min"], values["max"]
            ))
        md_lines.append("\n")

    if "delta" in benchmark["run_summary"]:
        md_lines.append("## Delta\n")
        for metric, value in benchmark["run_summary"]["delta"].items():
            md_lines.append("- **{}**: {}\n".format(metric, value))

    Path(md_path).write_text("".join(md_lines), encoding="utf-8")
    print("[OK] Summary written to {}".format(md_path), file=sys.stderr)


if __name__ == "__main__":
    main()
