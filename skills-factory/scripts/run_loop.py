#!/usr/bin/env python3
"""Run the eval + improve loop until all pass or max iterations reached.

Combines run_eval.py and improve_description.py in a loop, tracking history
and returning the best description found. Supports train/test split to prevent
overfitting.

Usage:
    py -m scripts.run_loop --eval-set evals/trigger-eval.json --skill-path /path/to/skill --model claude-sonnet-4-6 --verbose

Windows: Always use `py` not `python` or `python3`.
"""

import argparse
import json
import random
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

from scripts.generate_report import generate_html
from scripts.improve_description import improve_description
from scripts.run_eval import find_project_root, run_eval
from scripts.utils import parse_skill_md


def split_eval_set(eval_set, holdout, seed=42):
    """Split eval set into train and test sets, stratified by should_trigger."""
    random.seed(seed)

    trigger = [e for e in eval_set if e["should_trigger"]]
    no_trigger = [e for e in eval_set if not e["should_trigger"]]

    random.shuffle(trigger)
    random.shuffle(no_trigger)

    n_trigger_test = max(1, int(len(trigger) * holdout))
    n_no_trigger_test = max(1, int(len(no_trigger) * holdout))

    test_set = trigger[:n_trigger_test] + no_trigger[:n_no_trigger_test]
    train_set = trigger[n_trigger_test:] + no_trigger[n_no_trigger_test:]

    return train_set, test_set


def run_loop(eval_set, skill_path, description_override, num_workers, timeout,
             max_iterations, runs_per_query, trigger_threshold, holdout, model,
             verbose, live_report_path=None, log_dir=None):
    """Run the eval + improvement loop."""
    project_root = find_project_root()
    name, original_description, content = parse_skill_md(skill_path)
    current_description = description_override or original_description

    if holdout > 0:
        train_set, test_set = split_eval_set(eval_set, holdout)
        if verbose:
            print("[INFO] Split: {} train, {} test (holdout={})".format(
                len(train_set), len(test_set), holdout), file=sys.stderr)
    else:
        train_set = eval_set
        test_set = []

    history = []
    exit_reason = "unknown"

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print("\n{}".format("=" * 60), file=sys.stderr)
            print("[INFO] Iteration {}/{}".format(iteration, max_iterations), file=sys.stderr)
            print("[INFO] Description: {}".format(current_description), file=sys.stderr)

        all_queries = train_set + test_set
        t0 = time.time()
        all_results = run_eval(
            eval_set=all_queries,
            skill_name=name,
            description=current_description,
            num_workers=num_workers,
            timeout=timeout,
            project_root=project_root,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
        )
        eval_elapsed = time.time() - t0

        train_queries_set = {q["query"] for q in train_set}
        train_result_list = [r for r in all_results["results"] if r["query"] in train_queries_set]
        test_result_list = [r for r in all_results["results"] if r["query"] not in train_queries_set]

        train_passed = sum(1 for r in train_result_list if r["pass"])
        train_total = len(train_result_list)
        train_summary = {"passed": train_passed, "failed": train_total - train_passed, "total": train_total}

        if test_set:
            test_passed = sum(1 for r in test_result_list if r["pass"])
            test_total = len(test_result_list)
            test_summary = {"passed": test_passed, "failed": test_total - test_passed, "total": test_total}
        else:
            test_summary = None

        history.append({
            "iteration": iteration,
            "description": current_description,
            "train_passed": train_summary["passed"],
            "train_failed": train_summary["failed"],
            "train_total": train_summary["total"],
            "train_results": train_result_list,
            "test_passed": test_summary["passed"] if test_summary else None,
            "test_failed": test_summary["failed"] if test_summary else None,
            "test_total": test_summary["total"] if test_summary else None,
            "test_results": test_result_list if test_set else None,
            "passed": train_summary["passed"],
            "failed": train_summary["failed"],
            "total": train_summary["total"],
            "results": train_result_list,
        })

        if live_report_path:
            partial_output = {
                "original_description": original_description,
                "best_description": current_description,
                "best_score": "in progress",
                "iterations_run": len(history),
                "holdout": holdout,
                "train_size": len(train_set),
                "test_size": len(test_set),
                "history": history,
            }
            live_report_path.write_text(
                generate_html(partial_output, auto_refresh=True, skill_name=name),
                encoding="utf-8"
            )

        if verbose:
            print("[INFO] Train: {}/{} passed ({:.1f}s)".format(
                train_summary["passed"], train_summary["total"], eval_elapsed
            ), file=sys.stderr)
            if test_summary:
                print("[INFO] Test: {}/{}".format(
                    test_summary["passed"], test_summary["total"]
                ), file=sys.stderr)
            for r in train_result_list + test_result_list:
                status = "PASS" if r["pass"] else "FAIL"
                print("  [{}] {}/{} expected={}: {}".format(
                    status, r["triggers"], r["runs"], r["should_trigger"], r["query"][:60]
                ), file=sys.stderr)

        if train_summary["failed"] == 0:
            exit_reason = "all_passed (iteration {})".format(iteration)
            if verbose:
                print("\n[OK] All train queries passed on iteration {}!".format(iteration), file=sys.stderr)
            break

        if iteration == max_iterations:
            exit_reason = "max_iterations ({})".format(max_iterations)
            break

        if verbose:
            print("\n[INFO] Improving description...", file=sys.stderr)

        t0 = time.time()
        blinded_history = [
            {k: v for k, v in h.items() if not k.startswith("test_")}
            for h in history
        ]
        new_description = improve_description(
            skill_name=name,
            skill_content=content,
            current_description=current_description,
            eval_results={"results": train_result_list, "summary": train_summary},
            history=blinded_history,
            model=model,
            log_dir=log_dir,
            iteration=iteration,
        )
        improve_elapsed = time.time() - t0

        if verbose:
            print("[INFO] Proposed ({:.1f}s): {}".format(improve_elapsed, new_description), file=sys.stderr)

        current_description = new_description

    if test_set:
        best = max(history, key=lambda h: h["test_passed"] or 0)
        best_score = "{}/{}".format(best["test_passed"], best["test_total"])
    else:
        best = max(history, key=lambda h: h["train_passed"])
        best_score = "{}/{}".format(best["train_passed"], best["train_total"])

    if verbose:
        print("\n[INFO] Exit reason: {}".format(exit_reason), file=sys.stderr)
        print("[OK] Best score: {} (iteration {})".format(best_score, best["iteration"]), file=sys.stderr)

    return {
        "exit_reason": exit_reason,
        "original_description": original_description,
        "best_description": best["description"],
        "best_score": best_score,
        "best_train_score": "{}/{}".format(best["train_passed"], best["train_total"]),
        "best_test_score": "{}/{}".format(best["test_passed"], best["test_total"]) if test_set else None,
        "final_description": current_description,
        "iterations_run": len(history),
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


def main():
    parser = argparse.ArgumentParser(description="Run eval + improve loop")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override starting description")
    parser.add_argument("--num-workers", type=int, default=10, help="Parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query (seconds)")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max improvement iterations")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--holdout", type=float, default=0.4, help="Test holdout fraction (0 to disable)")
    parser.add_argument("--model", required=True, help="Model for improvement calls")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    parser.add_argument("--report", default="auto", help="HTML report path ('auto' for temp, 'none' to disable)")
    parser.add_argument("--results-dir", default=None, help="Save all outputs to timestamped subdirectory")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print("[ERROR] No SKILL.md found at {}".format(skill_path), file=sys.stderr)
        sys.exit(1)

    name, _, _ = parse_skill_md(skill_path)

    if args.report != "none":
        if args.report == "auto":
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            live_report_path = Path(tempfile.gettempdir()) / "skill_description_report_{}_{}.html".format(
                skill_path.name, timestamp)
        else:
            live_report_path = Path(args.report)
        live_report_path.write_text(
            "<html><body><h1>Starting optimization loop...</h1>"
            '<meta http-equiv="refresh" content="5"></body></html>',
            encoding="utf-8"
        )
        webbrowser.open(str(live_report_path))
    else:
        live_report_path = None

    if args.results_dir:
        timestamp = time.strftime("%Y-%m-%d_%H%M%S")
        results_dir = Path(args.results_dir) / timestamp
        results_dir.mkdir(parents=True, exist_ok=True)
    else:
        results_dir = None

    log_dir = results_dir / "logs" if results_dir else None

    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        description_override=args.description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        max_iterations=args.max_iterations,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        holdout=args.holdout,
        model=args.model,
        verbose=args.verbose,
        live_report_path=live_report_path,
        log_dir=log_dir,
    )

    json_output = json.dumps(output, indent=2)
    print(json_output)
    if results_dir:
        (results_dir / "results.json").write_text(json_output, encoding="utf-8")

    if live_report_path:
        live_report_path.write_text(
            generate_html(output, auto_refresh=False, skill_name=name),
            encoding="utf-8"
        )
        print("\n[OK] Report: {}".format(live_report_path), file=sys.stderr)

    if results_dir and live_report_path:
        (results_dir / "report.html").write_text(
            generate_html(output, auto_refresh=False, skill_name=name),
            encoding="utf-8"
        )
        print("[OK] Results saved to: {}".format(results_dir), file=sys.stderr)


if __name__ == "__main__":
    main()
