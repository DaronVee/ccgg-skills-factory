#!/usr/bin/env python3
"""Improve a skill description based on eval results.

Takes eval results (from run_eval.py) and generates an improved description
by calling `claude -p` as a subprocess.

Usage:
    py -m scripts.improve_description --eval-results results.json --skill-path /path/to/skill --model claude-sonnet-4-6

Windows: Always use `py` not `python` or `python3`.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from scripts.utils import parse_skill_md


def _call_claude(prompt, model, timeout=300):
    """Run `claude -p` with the prompt on stdin and return the text response."""
    claude_bin = shutil.which("claude")
    if not claude_bin:
        raise FileNotFoundError("claude CLI not found on PATH")
    cmd = [claude_bin, "-p", "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "claude -p exited {}\nstderr: {}".format(result.returncode, result.stderr)
        )
    return result.stdout


def improve_description(skill_name, skill_content, current_description,
                        eval_results, history, model, test_results=None,
                        log_dir=None, iteration=None):
    """Call Claude to improve the description based on eval results."""
    failed_triggers = [
        r for r in eval_results["results"]
        if r["should_trigger"] and not r["pass"]
    ]
    false_triggers = [
        r for r in eval_results["results"]
        if not r["should_trigger"] and not r["pass"]
    ]

    train_score = "{}/{}".format(
        eval_results["summary"]["passed"], eval_results["summary"]["total"]
    )
    if test_results:
        test_score = "{}/{}".format(
            test_results["summary"]["passed"], test_results["summary"]["total"]
        )
        scores_summary = "Train: {}, Test: {}".format(train_score, test_score)
    else:
        scores_summary = "Train: {}".format(train_score)

    prompt = (
        'You are optimizing a skill description for a Claude Code skill called "{}". '
        "A skill has a title and description that Claude sees when deciding whether to use it. "
        "Your goal is to write a description that triggers for relevant queries and doesn't "
        "trigger for irrelevant ones.\n\n"
        "Current description:\n<current_description>\n\"{}\"\n</current_description>\n\n"
        "Current scores ({}):\n<scores_summary>\n"
    ).format(skill_name, current_description, scores_summary)

    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += '  - "{}" (triggered {}/{} times)\n'.format(
                r["query"], r["triggers"], r["runs"]
            )
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but shouldn't have):\n"
        for r in false_triggers:
            prompt += '  - "{}" (triggered {}/{} times)\n'.format(
                r["query"], r["triggers"], r["runs"]
            )
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (do NOT repeat these):\n\n"
        for h in history:
            train_s = "{}/{}".format(
                h.get("train_passed", h.get("passed", 0)),
                h.get("train_total", h.get("total", 0))
            )
            score_str = "train={}".format(train_s)
            prompt += '<attempt {}>\nDescription: "{}"\n'.format(score_str, h["description"])
            if "results" in h:
                prompt += "Train results:\n"
                for r in h["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    prompt += '  [{}] "{}" (triggered {}/{})\n'.format(
                        status, r["query"][:80], r["triggers"], r["runs"]
                    )
            prompt += "</attempt>\n\n"

    prompt += "</scores_summary>\n\n"
    prompt += "Skill content (for context):\n<skill_content>\n{}\n</skill_content>\n\n".format(
        skill_content
    )
    prompt += (
        "Write a new, improved description. Generalize from failures to broader categories "
        "of user intent. Do NOT create an ever-expanding list of specific queries. "
        "Keep under 200 words and under 1024 characters. "
        "Phrase in the imperative ('Use this skill for...'). "
        "Focus on user intent, not implementation details.\n\n"
        "Respond with only the new description in <new_description> tags."
    )

    text = _call_claude(prompt, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip().strip('"') if match else text.strip().strip('"')

    transcript = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "over_limit": len(description) > 1024,
    }

    if len(description) > 1024:
        shorten_prompt = (
            "This description is {} characters, over the 1024-character limit:\n\n"
            '"{}"\n\n'
            "Rewrite it under 1024 characters while keeping the most important trigger "
            "words and intent coverage. Respond with only the new description in "
            "<new_description> tags."
        ).format(len(description), description)
        shorten_text = _call_claude(shorten_prompt, model)
        match = re.search(r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL)
        shortened = match.group(1).strip().strip('"') if match else shorten_text.strip().strip('"')
        transcript["rewrite_description"] = shortened
        description = shortened

    transcript["final_description"] = description

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "improve_iter_{}.json".format(iteration or "unknown")
        log_file.write_text(json.dumps(transcript, indent=2), encoding="utf-8")

    return description


def main():
    parser = argparse.ArgumentParser(description="Improve a skill description based on eval results")
    parser.add_argument("--eval-results", required=True, help="Path to eval results JSON")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--history", default=None, help="Path to history JSON")
    parser.add_argument("--model", required=True, help="Model for improvement")
    parser.add_argument("--verbose", action="store_true", help="Print thinking to stderr")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print("[ERROR] No SKILL.md found at {}".format(skill_path), file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text(encoding="utf-8"))
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text(encoding="utf-8"))

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results["description"]

    if args.verbose:
        print("[INFO] Current: {}".format(current_description), file=sys.stderr)
        print("[INFO] Score: {}/{}".format(
            eval_results["summary"]["passed"], eval_results["summary"]["total"]
        ), file=sys.stderr)

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        model=args.model,
    )

    if args.verbose:
        print("[INFO] Improved: {}".format(new_description), file=sys.stderr)

    output = {
        "description": new_description,
        "history": history + [{
            "description": current_description,
            "passed": eval_results["summary"]["passed"],
            "failed": eval_results["summary"]["failed"],
            "total": eval_results["summary"]["total"],
            "results": eval_results["results"],
        }],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
