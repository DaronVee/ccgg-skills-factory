#!/usr/bin/env python3
"""Generate an HTML report from run_loop.py output.

Takes the JSON output from run_loop.py and generates a visual HTML report
showing each description attempt with check/x for each test case.
Distinguishes between train and test queries.

Usage:
    py -m scripts.generate_report results.json -o report.html
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from html import escape as html_escape
except ImportError:
    from cgi import escape as html_escape


def generate_html(data, auto_refresh=False, skill_name=""):
    """Generate HTML report from loop output data."""
    history = data.get("history", [])
    title_prefix = html_escape(skill_name + " -- ") if skill_name else ""

    train_queries = []
    test_queries = []
    if history:
        for r in history[0].get("train_results", history[0].get("results", [])):
            train_queries.append({"query": r["query"], "should_trigger": r.get("should_trigger", True)})
        if history[0].get("test_results"):
            for r in history[0].get("test_results", []):
                test_queries.append({"query": r["query"], "should_trigger": r.get("should_trigger", True)})

    refresh_tag = '    <meta http-equiv="refresh" content="5">\n' if auto_refresh else ""

    parts = []
    parts.append('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n')
    parts.append(refresh_tag)
    parts.append('<title>{}Skill Description Optimization</title>\n'.format(title_prefix))
    parts.append("""<style>
body { font-family: Georgia, serif; max-width: 100%; margin: 0 auto; padding: 20px; background: #faf9f5; color: #141413; }
h1 { font-family: sans-serif; }
.summary { background: white; padding: 15px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #e8e6dc; }
.summary p { margin: 5px 0; }
.best { color: #788c5d; font-weight: bold; }
.table-container { overflow-x: auto; width: 100%; }
table { border-collapse: collapse; background: white; border: 1px solid #e8e6dc; font-size: 12px; min-width: 100%; }
th, td { padding: 8px; text-align: left; border: 1px solid #e8e6dc; }
th { background: #141413; color: #faf9f5; font-weight: 500; }
th.test-col { background: #6a9bcc; }
td.description { font-family: monospace; font-size: 11px; word-wrap: break-word; max-width: 400px; }
td.result { text-align: center; font-size: 16px; min-width: 40px; }
td.test-result { background: #f0f6fc; }
.pass { color: #788c5d; }
.fail { color: #c44; }
.rate { font-size: 9px; color: #b0aea5; display: block; }
.score { display: inline-block; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px; }
.score-good { background: #eef2e8; color: #788c5d; }
.score-ok { background: #fef3c7; color: #d97706; }
.score-bad { background: #fceaea; color: #c44; }
.best-row { background: #f5f8f2; }
th.positive-col { border-bottom: 3px solid #788c5d; }
th.negative-col { border-bottom: 3px solid #c44; }
</style>\n</head>\n<body>\n""")

    parts.append('<h1>{}Skill Description Optimization</h1>\n'.format(title_prefix))

    best_test_score = data.get("best_test_score")
    parts.append('<div class="summary">\n')
    parts.append('<p><strong>Original:</strong> {}</p>\n'.format(
        html_escape(data.get("original_description", "N/A"))))
    parts.append('<p class="best"><strong>Best:</strong> {}</p>\n'.format(
        html_escape(data.get("best_description", "N/A"))))
    parts.append('<p><strong>Best Score:</strong> {} {}</p>\n'.format(
        data.get("best_score", "N/A"), "(test)" if best_test_score else "(train)"))
    parts.append('<p><strong>Iterations:</strong> {} | <strong>Train:</strong> {} | <strong>Test:</strong> {}</p>\n'.format(
        data.get("iterations_run", 0), data.get("train_size", "?"), data.get("test_size", "?")))
    parts.append('</div>\n')

    # Table
    parts.append('<div class="table-container">\n<table>\n<thead><tr>\n')
    parts.append('<th>Iter</th><th>Train</th><th>Test</th><th>Description</th>\n')
    for qinfo in train_queries:
        pol = "positive-col" if qinfo["should_trigger"] else "negative-col"
        parts.append('<th class="{}">{}</th>\n'.format(pol, html_escape(qinfo["query"][:60])))
    for qinfo in test_queries:
        pol = "positive-col" if qinfo["should_trigger"] else "negative-col"
        parts.append('<th class="test-col {}">{}</th>\n'.format(pol, html_escape(qinfo["query"][:60])))
    parts.append('</tr></thead>\n<tbody>\n')

    # Find best iteration
    if test_queries:
        best_iter = max(history, key=lambda h: h.get("test_passed") or 0).get("iteration")
    elif history:
        best_iter = max(history, key=lambda h: h.get("train_passed", h.get("passed", 0))).get("iteration")
    else:
        best_iter = None

    for h in history:
        iteration = h.get("iteration", "?")
        train_results = h.get("train_results", h.get("results", []))
        test_results_list = h.get("test_results", [])
        description = h.get("description", "")

        train_by_query = {r["query"]: r for r in train_results}
        test_by_query = {r["query"]: r for r in test_results_list} if test_results_list else {}

        def aggregate_runs(results):
            correct = total = 0
            for r in results:
                runs = r.get("runs", 0)
                triggers = r.get("triggers", 0)
                total += runs
                if r.get("should_trigger", True):
                    correct += triggers
                else:
                    correct += runs - triggers
            return correct, total

        train_correct, train_runs = aggregate_runs(train_results)
        test_correct, test_runs = aggregate_runs(test_results_list)

        def score_class(correct, total):
            if total > 0:
                ratio = correct / total
                if ratio >= 0.8:
                    return "score-good"
                elif ratio >= 0.5:
                    return "score-ok"
            return "score-bad"

        row_class = "best-row" if iteration == best_iter else ""
        parts.append('<tr class="{}">\n'.format(row_class))
        parts.append('<td>{}</td>\n'.format(iteration))
        parts.append('<td><span class="score {}">{}/{}</span></td>\n'.format(
            score_class(train_correct, train_runs), train_correct, train_runs))
        parts.append('<td><span class="score {}">{}/{}</span></td>\n'.format(
            score_class(test_correct, test_runs), test_correct, test_runs))
        parts.append('<td class="description">{}</td>\n'.format(html_escape(description)))

        for qinfo in train_queries:
            r = train_by_query.get(qinfo["query"], {})
            did_pass = r.get("pass", False)
            icon = "[OK]" if did_pass else "[X]"
            css = "pass" if did_pass else "fail"
            parts.append('<td class="result {}">{}  <span class="rate">{}/{}</span></td>\n'.format(
                css, icon, r.get("triggers", 0), r.get("runs", 0)))

        for qinfo in test_queries:
            r = test_by_query.get(qinfo["query"], {})
            did_pass = r.get("pass", False)
            icon = "[OK]" if did_pass else "[X]"
            css = "pass" if did_pass else "fail"
            parts.append('<td class="result test-result {}">{}  <span class="rate">{}/{}</span></td>\n'.format(
                css, icon, r.get("triggers", 0), r.get("runs", 0)))

        parts.append('</tr>\n')

    parts.append('</tbody>\n</table>\n</div>\n</body>\n</html>\n')
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Generate HTML report from run_loop output")
    parser.add_argument("input", help="Path to JSON output from run_loop.py (or - for stdin)")
    parser.add_argument("-o", "--output", default=None, help="Output HTML file (default: stdout)")
    parser.add_argument("--skill-name", default="", help="Skill name for report title")
    args = parser.parse_args()

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    html_output = generate_html(data, skill_name=args.skill_name)

    if args.output:
        Path(args.output).write_text(html_output, encoding="utf-8")
        print("[OK] Report written to {}".format(args.output), file=sys.stderr)
    else:
        print(html_output)


if __name__ == "__main__":
    main()
