---
name: skills-factory
description: "Meta-skill for creating production-ready Claude Code skills using evaluation-driven development, automated eval loops, blind A/B comparison, benchmark aggregation, description optimization, and progressive disclosure patterns. Includes grader, comparator, and analyzer agents with schema-enforced data interchange."
---

# Skills Factory

A comprehensive meta-skill for creating, validating, evaluating, and iterating on production-ready Claude Code skills.

## About Skills

Skills extend Claude Code's capabilities with specialized knowledge and workflows. They use a **two-level progressive disclosure system**:

1. **Description** (YAML `description` field) - Always loaded into context at startup. Claude uses this to decide when to invoke the skill.
2. **Full Content** (SKILL.md body + referenced files) - Loaded when the skill is invoked, either by Claude or the user.

Skills are filesystem-based and live in:
- `~/.claude/skills/` - Personal skills (available across all projects)
- `.claude/skills/` - Project skills (version-controlled, shared via git)
- `.claude/commands/` - Backward-compatible location (also works)

**Priority resolution** (when same name exists at multiple levels): Enterprise > Personal > Project.

**Note:** Skills follow the [Agent Skills open standard](https://agentskills.io) for cross-platform compatibility.

**Context budget:** Skill descriptions consume context. Total budget is ~2% of context window (default ~16k chars). If you have many skills, keep descriptions concise or use `disable-model-invocation: true` on rarely-needed skills.

---

## Workspace Convention

**CRITICAL**: All eval and benchmark operations use this predetermined directory layout. Scripts, agents, and viewers depend on these exact paths. Do NOT deviate.

```
<skill-workspace>/
├── SKILL.md                          # The skill under development
├── evals/
│   ├── evals.json                    # Test cases (see SCHEMAS.md > evals.json)
│   ├── trigger-eval.json             # Trigger queries (see SCHEMAS.md > trigger-eval.json)
│   └── files/                        # Input files referenced by evals
├── iteration-<N>/                    # One per eval cycle (iteration-0 = baseline)
│   ├── eval-<ID>/                    # One per eval case
│   │   ├── with_skill/               # Runs WITH the skill loaded
│   │   │   ├── run-<M>/
│   │   │   │   ├── outputs/          # Executor output files + metrics.json
│   │   │   │   ├── transcript.md     # Full executor transcript
│   │   │   │   ├── grading.json      # Grader output (SCHEMAS.md > grading.json)
│   │   │   │   └── timing.json       # Wall clock + token counts
│   │   │   └── ...
│   │   └── without_skill/            # Runs WITHOUT the skill (baseline)
│   │       └── run-<M>/
│   │           └── (same structure)
│   ├── benchmark.json                # Aggregated stats (SCHEMAS.md > benchmark.json)
│   └── benchmark.md                  # Human-readable summary
├── description-optimization/         # Trigger description tuning
│   ├── results.json                  # run_loop.py output
│   └── report.html                   # Visual optimization report
└── history.json                      # Iteration progression tracker
```

**Schema reference**: All JSON formats are defined in [references/SCHEMAS.md](references/SCHEMAS.md). Read SCHEMAS.md before creating or parsing any JSON file. Using wrong field names causes silent downstream failures.

---

## Asset Registry

All scripts, agents, templates, and references available in this skill. **Read the linked file before using each asset** — inline pointers below tell you WHERE each asset is used in the workflow.

**Working directory**: All `py -m scripts.*` commands must run from the skills-factory skill directory (where this SKILL.md lives). Direct `py scripts/...` calls accept absolute paths.

### Scripts

| Script | Purpose | Used In |
|--------|---------|---------|
| `scripts/init_skill.py` | Generate new skill from template | Step 3 |
| `scripts/comprehensive_validate.py` | Deep validation (structure, content, best practices) | Step 5 |
| `scripts/quick_validate.py` | Fast YAML-only validation | Step 5 |
| `scripts/package_skill.py` | Create distributable .zip | Step 8 |
| `scripts/run_eval.py` | Spawn `claude -p` to test trigger rates | Step 6, Step 7 |
| `scripts/run_loop.py` | Full eval-improve-re-eval optimization loop | Step 7 |
| `scripts/improve_description.py` | LLM-powered description rewriter | Step 7 (called by run_loop) |
| `scripts/generate_report.py` | HTML report from run_loop output | Step 7 |
| `scripts/aggregate_benchmark.py` | Aggregate grading.json into benchmark stats | Step 6 |
| `scripts/utils.py` | Shared utilities (parse_skill_md) | Internal |

### Agents

| Agent | Purpose | Used In |
|-------|---------|---------|
| `agents/grader.md` | Grade expectations against transcripts, extract claims | Step 6 |
| `agents/comparator.md` | Blind A/B comparison between skill versions | Step 6 |
| `agents/analyzer.md` | Post-hoc analysis + improvement suggestions | Step 6 |

### Templates & Viewers

| Asset | Purpose | Used In |
|-------|---------|---------|
| `assets/eval_review.html` | Interactive eval query editor | Step 5 (eval creation) |
| `eval-viewer/viewer.html` | Full eval review UI (Outputs + Benchmark tabs) | Step 6 (review) |
| `eval-viewer/generate_review.py` | HTTP server for interactive review | Step 6 (review) |

### References

| Reference | Purpose |
|-----------|---------|
| [SCHEMAS.md](references/SCHEMAS.md) | **All JSON schemas** — read before creating/parsing data files |
| [FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md) | YAML configuration wizard (6-question decision tree) |
| [SUBAGENT_PATTERNS.md](references/SUBAGENT_PATTERNS.md) | Fork patterns, agent skills loading |
| [EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md) | Evaluation-driven development methodology |
| [TWO_CLAUDE_METHODOLOGY.md](references/TWO_CLAUDE_METHODOLOGY.md) | Manual iterative testing (supplementary to automated evals) |
| [WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md) | Workflow design patterns and examples |
| [VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md) | Feedback loops and validation strategies |
| [DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md) | Deployment and distribution guide |
| [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) | Common issues and solutions |

---

## Skill Creation Process

### Step 1: Understanding the Domain

Before writing anything, deeply understand what you're building:

**Ask Critical Questions:**
- What specific problem does this skill solve?
- Who is the user and what's their context?
- What tasks should be automated vs. guided?
- What knowledge must Claude have vs. can reference?
- How will success be measured?

**Research Thoroughly:**
- Review similar existing skills
- Study relevant documentation
- Understand the workflow domain
- Identify edge cases and failure modes

**Define Success Criteria:**
- What specific outcomes indicate the skill works?
- What would success look like without the skill vs. with it?
- How will you evaluate effectiveness?

**See:** [references/EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md) for evaluation-driven development methodology.

### Step 2: Planning Your Architecture

Design your skill's structure before implementation:

**MANDATORY - Configure Frontmatter First:**
Before writing ANY YAML frontmatter, read and follow [references/FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md). Run through the 6-question decision guide to determine which frontmatter fields this skill needs.

**Choose Your Pattern:**
- **Simple skill**: SKILL.md only (~100-300 lines)
- **Standard skill**: SKILL.md + 1-3 reference files
- **Script-heavy skill**: SKILL.md + scripts/ + validation patterns
- **Reference-heavy skill**: SKILL.md + references/ with 5+ supporting docs

**Plan Progressive Disclosure:**
- What must be in SKILL.md? (triggers, core workflow, navigation)
- What goes to references/? (detailed guides, examples, context)
- What goes to scripts/? (validation, automation, processing)
- Keep SKILL.md under 200 lines when possible

**Design Workflows:**
- Linear process? Use simple sequential steps
- Quality gates? Use checklist workflow
- Conditional paths? Design decision tree
- Iteration needed? Plan feedback loop
- Isolated subagent task? Use forked context workflow

**See:** [references/WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md) and [references/VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md)

### Step 3: Initialize Skill Structure

Create your skill's foundation:

```bash
cd ~/.claude/skills  # or .claude/skills for project-specific
py /path/to/scripts/init_skill.py my-skill-name
```

This creates:
```
my-skill-name/
├── SKILL.md          # Main skill file (YAML + instructions)
├── scripts/          # Executable scripts (optional)
├── references/       # Supporting documentation (optional)
└── assets/           # Images, templates, data files (optional)
```

**Post-Initialization:**
- Run through the Frontmatter Decision Guide (Step 2)
- Replace ALL placeholder markers in YAML frontmatter
- Draft description with key trigger terms (max 1024 chars)
- Ensure name is hyphen-case (lowercase + hyphens only)

### Step 4: Design & Implement

Build your skill following best practices:

**Complete YAML Frontmatter Reference:**

| Field | Status | Description |
|-------|--------|-------------|
| `name` | Recommended | Lowercase + hyphens, max 64 chars. Defaults to directory name if omitted. |
| `description` | Recommended | What it does + when to use. Max 1024 chars. Include trigger terms. Defaults to first paragraph of body. |
| `disable-model-invocation` | Optional | `true` = only user can invoke with /name. Claude cannot auto-load. Use for side-effect skills (deploy, send, delete). |
| `user-invocable` | Optional | `false` = hide from / menu. Only Claude can invoke. Use for background knowledge/conventions. |
| `context` | Optional | `fork` = run in isolated subagent. No conversation history. See [SUBAGENT_PATTERNS.md](references/SUBAGENT_PATTERNS.md). |
| `agent` | Optional | Subagent type when `context: fork`. Values: `Explore`, `Plan`, `general-purpose`, or custom agent name. |
| `model` | Optional | Model override: `sonnet`, `opus`, `haiku`, or `inherit`. |
| `argument-hint` | Optional | Autocomplete hint shown in / menu: `[issue-number]`, `[filename] [format]`. |
| `allowed-tools` | Optional | Comma-separated tool restriction: `Read, Grep, Glob` or `Bash(gh *), Read`. |
| `hooks` | Optional | Lifecycle hooks scoped to skill execution (PreToolUse, PostToolUse, Stop). |
| `metadata` | Custom | Key-value tracking data: `{author: "Team", version: "1.0"}`. |

**Minimal example** (most skills only need this):
```yaml
---
name: my-helper
description: Helps with specific task. Use when user asks about X or Y.
---
```

**Full example** (forked research skill with restrictions):
```yaml
---
name: deep-research
description: Deep codebase research that protects main context from output bloat
context: fork
agent: Explore
model: haiku
allowed-tools: Read, Grep, Glob
argument-hint: "[research-question]"
---
```

**Important format notes:**
- `allowed-tools` is a **comma-separated string**, not a YAML list
- `allowed-tools` supports argument patterns: `Bash(gh *)`, `Bash(npm test)`
- Available tools: `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `Task`, `Skill`

**See:** [references/FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md) for the full 6-question decision guide.

#### Invocation Control

| `disable-model-invocation` | `user-invocable` | Result |
|---------------------------|-----------------|--------|
| omitted (false) | omitted (true) | **Default**: Claude + user can invoke |
| `true` | omitted (true) | **Manual only**: User invokes with `/name`, Claude cannot auto-load |
| omitted (false) | `false` | **Auto-only**: Claude can invoke, hidden from `/` menu |
| `true` | `false` | **Disabled**: Neither can invoke (rarely useful) |

**Rule of thumb**: If the skill has side effects (deploy, send, delete, publish), use `disable-model-invocation: true`.

#### String Substitutions

| Variable | Meaning | Example |
|----------|---------|---------|
| `$ARGUMENTS` | All arguments as string | `/fix-issue 42` -> `$ARGUMENTS` = `"42"` |
| `$0` or `$ARGUMENTS[0]` | First argument | `/convert file.md pdf` -> `$0` = `"file.md"` |
| `$1` or `$ARGUMENTS[1]` | Second argument | `/convert file.md pdf` -> `$1` = `"pdf"` |
| `${CLAUDE_SESSION_ID}` | Current session ID | Useful for unique output paths |

**Auto-append**: If `$ARGUMENTS` doesn't appear in skill content, arguments are automatically appended to the end.

#### Dynamic Context Injection

Skills can inject live shell data (git status, GitHub info, system state) into their content at load time. Commands execute BEFORE skill content reaches Claude.

**See:** [references/FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md) -- Question 5: "Does this skill need dynamic data?"

#### Advanced Patterns

- **`ultrathink`**: Include this keyword in skill content to enable extended thinking mode
- **Skill character budget**: Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable
- **Subagent integration**: Skills can spawn subagents (`context: fork`) or be preloaded into subagents (`skills:` field). See [references/SUBAGENT_PATTERNS.md](references/SUBAGENT_PATTERNS.md)

**SKILL.md Body Guidelines:**
- Start with clear "About" section explaining purpose
- Use concrete examples over abstract explanations
- Break complex workflows into numbered steps
- Reference detailed content (don't inline everything)
- Keep total SKILL.md under 500 lines (ideally under 200)

**Progressive Disclosure Rules:**
- Reference files ONE level deep (e.g. `references/MY_GUIDE.md`) — OK
- No nested references (`references/category/subcategory/file.md`) — NOT OK
- Load scripts when needed: "Run validation: `py scripts/validate.py`"
- Front-load critical info, defer details to references

**See:** [references/WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md), [references/VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md)

### Step 5: Validate & Create Evals

Ensure quality and prepare evaluation infrastructure:

**5a. Comprehensive Validation:**
```bash
py scripts/comprehensive_validate.py /path/to/my-skill-name
```

Checks: YAML structure, naming conventions, description quality, progressive disclosure, best practices, content quality, workflow validation, fork validation.

**Fix all errors and warnings before proceeding.**

**5b. Create Eval Cases** (`evals/evals.json`):

Design test cases that define what "working correctly" means. Read [references/SCHEMAS.md](references/SCHEMAS.md) for the `evals.json` schema.

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user prompt that should use this skill",
      "expected_output": "Description of what success looks like",
      "files": ["evals/files/sample-input.pdf"],
      "expectations": [
        "The output includes a summary section",
        "All input data points are preserved",
        "The format matches the specified template"
      ]
    }
  ]
}
```

**Guidelines for good expectations:**
- Verifiable: Can be checked against actual output
- Specific: "Output has 5 columns" not "Output is well-formatted"
- Independent: Each expectation tests one thing
- Non-trivial: Don't test things that always pass

**5c. Create Trigger Eval Queries** (`evals/trigger-eval.json`):

Define when your skill SHOULD and SHOULD NOT trigger. Read [references/SCHEMAS.md](references/SCHEMAS.md) for the `trigger-eval.json` schema.

```json
[
  {"query": "Create a new Claude Code skill for PDF processing", "should_trigger": true},
  {"query": "Help me set up a Python virtual environment", "should_trigger": false}
]
```

**Guidelines:** 8-10 should-trigger + 8-10 should-not-trigger. Negative queries must be **near-misses** (related domain but wrong intent), not obviously irrelevant.

**Interactive editor**: Open `assets/eval_review.html` in a browser for visual eval query editing with add/delete/toggle/export.

**See:** [references/EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md), [references/SCHEMAS.md](references/SCHEMAS.md)

### Step 6: Evaluate & Iterate (Automated Eval Loop)

This is the core quality loop. Run your skill against eval cases, grade results, compare versions, and iterate.

**STATE DETECTION**: Before starting, detect where you are in the process:

```
IF no iteration-* directories exist:
    -> Start at 6a (first baseline run)
IF iteration-N exists but has no benchmark.json:
    -> Resume at 6c (aggregate incomplete iteration)
IF iteration-N exists WITH benchmark.json:
    -> Start iteration-N+1 at 6a
IF comparison.json exists in latest iteration:
    -> Go to 6e (analyze) or 6f (decide next action)
```

#### 6a. Execute Eval Runs

For each eval case, run the skill in both configurations. Run with_skill and without_skill **in parallel** (they are independent).

**Subagent prompt for executor** (use this exact template when spawning executor subagents):

```
You are an eval executor. Your task:

EVAL CASE:
- Prompt: {eval.prompt}
- Expected: {eval.expected_output}
- Input files: {eval.files}

INSTRUCTIONS:
1. Execute the prompt as a real user would
2. Save all output files to: outputs/
3. Save a metrics.json to outputs/ with tool_calls, total_tool_calls, total_steps, files_created, errors_encountered, output_chars
4. Do NOT grade yourself — just execute faithfully

SKILL CONTEXT (only for with_skill runs):
{skill_content}
```

**Save timing data**: When each executor subagent completes, capture `total_tokens` and `duration_ms` from the task notification into `timing.json`. These values are NOT persisted anywhere else.

```json
{"total_tokens": 84852, "duration_ms": 23332, "total_duration_seconds": 23.3}
```

#### 6b. Grade Each Run

For each completed run, spawn the grader agent. Run grading for all completed runs **in parallel**.

**Subagent prompt for grader** (use this exact template):

```
You are an eval grader. Read agents/grader.md for your full instructions.

EVAL METADATA:
- Eval ID: {eval.id}
- Prompt: {eval.prompt}
- Expectations to verify:
{expectations_list}

WORKSPACE: {run_dir}
- Read outputs/ for executor output files
- Read transcript.md for the execution transcript

OUTPUT: Write grading.json to {run_dir}/grading.json

CRITICAL SCHEMA RULE: Your grading.json MUST use these exact field names in the expectations array:
- "text" (NOT "name")
- "passed" (NOT "met")
- "evidence" (NOT "details")
Read references/SCHEMAS.md > grading.json for the complete schema.
```

#### 6c. Aggregate Benchmark

After ALL runs for an iteration are graded, aggregate results:

```bash
py -m scripts.aggregate_benchmark iteration-N --skill-name my-skill
```

This reads all `grading.json` files and produces:
- `iteration-N/benchmark.json` — statistical summary (mean, stddev, min, max per metric)
- `iteration-N/benchmark.md` — human-readable summary

**Do NOT run this until every run in the iteration has a grading.json.** Partial aggregation produces misleading stats.

#### 6d. Compare Versions (iteration >= 1 only)

After iteration-1+, compare current vs. previous best using the blind comparator agent.

**Subagent prompt for comparator** (use this exact template):

```
You are a blind comparator. Read agents/comparator.md for your full instructions.

EVAL CASE:
- Prompt: {eval.prompt}
- Expected: {eval.expected_output}

OUTPUT A (anonymized):
{output_from_version_X}

OUTPUT B (anonymized):
{output_from_version_Y}

OUTPUT: Write comparison.json to {grading_dir}/comparison.json
Read references/SCHEMAS.md > comparison.json for the schema.

IMPORTANT: You do NOT know which output used a skill. Judge purely on quality.
```

**Randomize A/B assignment** each time to prevent position bias.

#### 6e. Analyze Results

After comparison, spawn the analyzer agent for improvement insights.

**Subagent prompt for analyzer** (use this exact template):

```
You are a post-hoc analyzer. Read agents/analyzer.md for your full instructions.

COMPARISON RESULT: {comparison.json contents}
WINNER OUTPUT: {winner's full output}
LOSER OUTPUT: {loser's full output}
SKILL CONTENT: {current SKILL.md}
BENCHMARK DATA: {benchmark.json contents}

OUTPUT: Write analysis.json to {grading_dir}/analysis.json
Read references/SCHEMAS.md > analysis.json for the schema.

Focus on: What specific skill instructions led to wins/losses?
What changes would improve the skill?
```

#### 6f. Decide Next Action

Based on benchmark + analysis results:

| Condition | Action |
|-----------|--------|
| pass_rate >= 0.90 AND delta > +0.20 | Skill is strong. Proceed to Step 7 (description optimization) |
| pass_rate >= 0.70 AND delta > 0 | Good progress. Apply analyzer suggestions, run iteration N+1 |
| pass_rate < 0.70 OR delta <= 0 | Significant issues. Review analyzer feedback, make substantial edits |
| 5 iterations with no improvement | Stop. Reassess skill architecture (Step 2) |

**Loop termination**: Maximum 5 iterations. If pass_rate has not improved for 3 consecutive iterations, stop and reassess.

#### Review Results Interactively

Launch the eval viewer for detailed inspection:

```bash
py -m eval-viewer.generate_review /path/to/skill-workspace
```

Opens a browser with the full review UI (Outputs tab + Benchmark tab). Use this to inspect individual run outputs, grading details, and benchmark comparisons.

**See:** [references/EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md), [references/TWO_CLAUDE_METHODOLOGY.md](references/TWO_CLAUDE_METHODOLOGY.md) (supplementary manual testing)

### Step 7: Optimize Description (Trigger Accuracy)

After the skill content is strong (Step 6), optimize the YAML description so Claude invokes it at the right time.

**7a. Prepare trigger-eval.json** (if not done in Step 5c).

**7b. Run the optimization loop:**

```bash
py -m scripts.run_loop --eval-set evals/trigger-eval.json --skill-path /path/to/my-skill --max-iterations 10 --runs-per-query 3 --verbose
```

This automatically:
1. Splits queries into **train (60%) / test (40%)** sets (stratified by should_trigger)
2. Evaluates current description against train set
3. Calls `improve_description.py` to rewrite based on failures
4. Re-evaluates the new description
5. Repeats until convergence or max iterations
6. Selects the best description by **test score** (not train) to prevent overfitting
7. Generates live HTML report with auto-refresh

**Output:**
- `description-optimization/results.json` — full history of all iterations
- `description-optimization/report.html` — visual report (open in browser)

**7c. Generate final report** (if not auto-generated):

```bash
py -m scripts.generate_report description-optimization/results.json -o description-optimization/report.html --skill-name my-skill
```

**7d. Apply the winning description:**

Update the YAML frontmatter `description` field in SKILL.md with the best description from `results.json > best_description`.

**Anti-pattern**: Do NOT manually tune the description without re-running the eval loop. Manual edits that improve one trigger often break others.

### Step 8: Deploy & Distribute

After validation, evaluation, and description optimization, deploy your skill.

**Deploy to Claude Code:**

For personal use (across all projects):
```bash
py scripts/package_skill.py my-skill --install personal
```
Installs to `~/.claude/skills/my-skill/` - immediately available in all sessions.

For team/project use (shared via git):
```bash
py scripts/package_skill.py my-skill --install project
git add .claude/skills/my-skill/
git commit -m "Add my-skill for team workflows"
git push
```

**Deploy to Claude.ai / Claude Desktop:**
```bash
py scripts/package_skill.py my-skill --package
```
Upload generated `my-skill.zip` via Settings > Features.

**Deploy to Claude API:**
Upload via `/v1/skills` endpoint for organization-wide availability.

**Verification:**
- Claude Code: Ask "What skills are available?"
- Claude.ai/Desktop: Check Settings > Features shows skill
- API: List skills via API endpoint

**Important:** Skills **do not sync across surfaces**. Must deploy separately to each platform.

**See:** [references/DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md)

---

## Anti-Patterns

**Do NOT do these:**

- **Skip schema validation**: Never create grading.json, benchmark.json, or comparison.json without first reading [SCHEMAS.md](references/SCHEMAS.md). Wrong field names cause silent failures in the viewer and aggregation scripts.
- **Run aggregate before all runs complete**: Partial benchmarks produce misleading statistics.
- **Manually tune descriptions without eval loop**: Manual edits that fix one trigger break others. Always re-run `run_loop.py`.
- **Use train score to select best description**: Always use test score. Train score overfits.
- **Grade your own output**: The executor must NOT self-grade. Grading is a separate agent with separate context.
- **Forget timing data**: Capture `total_tokens` and `duration_ms` from task notifications immediately. They cannot be recovered later.
- **Nest reference files**: Keep references ONE level deep. No `references/category/subcategory/`.
- **Inline everything in SKILL.md**: Use progressive disclosure. SKILL.md is the router, not the encyclopedia.

---

## Troubleshooting

**Common Issues:**
- "Claude doesn't use my skill" -> Check description triggers, YAML validity, `disable-model-invocation` not accidentally set
- "Skill loaded but ignored" -> Add concrete examples, improve clarity, run Step 7
- "Skill triggers when it shouldn't" -> Use `disable-model-invocation: true` or optimize description (Step 7)
- "Validation failing" -> Run `py scripts/comprehensive_validate.py` for specific errors
- "Skill too complex" -> Apply progressive disclosure, move content to references
- "Grading.json has wrong fields" -> Read SCHEMAS.md. Must use `text`/`passed`/`evidence`, NOT `name`/`met`/`details`
- "Benchmark shows all zeros" -> Check `runs[].result` is nested object, not flat fields. Check `configuration` not `config`
- "Eval viewer shows empty" -> Verify workspace directory structure matches convention above
- "Description optimization not improving" -> Check trigger-eval.json quality: are negative queries near-misses?
- "Forked skill returns poor results" -> Ensure body has task instructions, not just reference material
- "Some skills not loading" -> Character budget exceeded, shorten descriptions

**See:** [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for comprehensive troubleshooting guide.

---

## Example Skills

Skills created using this factory serve as living examples. Run `py scripts/comprehensive_validate.py /path/to/any-skill` to see how validation checks apply in practice. For architecture pattern examples, see [WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md) and [FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md).

---

## Version History

**v3.0.1** (2026-03-07)
- Self-evaluation using own methodology (Steps 5a-5c)
- Fixed: broken `references/examples/` directory reference (CRITICAL)
- Fixed: missing working directory requirement for `py -m scripts.*` commands (CRITICAL)
- Fixed: false-positive validation errors (TODO marker in instruction text, example markdown link)
- Added: `evals/evals.json` with 5 eval cases (happy path, forked skill, complex skill, failure case, meta-eval)
- Added: `evals/trigger-eval.json` with 18 trigger queries (9 positive, 9 near-miss negatives)
- Validation: comprehensive_validate.py passes with 0 errors on skills-factory itself

**v3.0.0** (2026-03-07)
- Automated eval loop: run_eval.py, run_loop.py, improve_description.py, generate_report.py, aggregate_benchmark.py
- Agent-based grading: grader.md, comparator.md (blind A/B), analyzer.md (post-hoc)
- Schema-enforced data interchange: SCHEMAS.md with 10 JSON schemas (evals, grading, benchmark, comparison, analysis, etc.)
- Description optimization: train/test split, overfitting prevention, convergence detection
- Interactive eval tools: eval_review.html (query editor), eval-viewer (review UI with Outputs + Benchmark tabs)
- Orchestration contract: state detection, workspace convention, subagent prompt templates, parallelism rules, loop termination
- Anti-pattern blocks: explicit "do NOT" section preventing common failures
- Shared utilities: utils.py (parse_skill_md), scripts/__init__.py
- Windows adaptation: `py` command, UTF-8 encoding, ASCII status markers, no select() on pipes
- New Step 5b-5c: eval creation integrated into validation step
- New Step 6: automated eval-grade-compare-analyze loop (replaces manual Two-Claude as primary)
- New Step 7: description optimization with automated trigger testing
- Two-Claude Methodology demoted to supplementary reference (still useful for manual exploration)
- Updated description in YAML frontmatter to reflect v3.0 capabilities

**v2.0.0** (2026-02-09)
- Complete frontmatter reference: all 11 official YAML fields documented
- Intelligent Frontmatter Decision Guide: 6-question wizard
- Subagent integration patterns: context: fork, agent types, skills field in agents
- Invocation control: disable-model-invocation, user-invocable, decision matrix
- String substitutions: $ARGUMENTS, $N, ${CLAUDE_SESSION_ID}
- Dynamic context injection
- New references: FRONTMATTER_DECISION_GUIDE.md, SUBAGENT_PATTERNS.md
- Updated validation script with new field recognition

**v1.1.0** (2025-10-19)
- Added deployment layer with cross-surface support
- Enhanced package_skill.py with --install flag
- Created DEPLOYMENT_GUIDE.md reference

**v1.0.0** (2025-10-19)
- Initial production release
- Evaluation-driven development framework
- Two-Claude iterative methodology
- Comprehensive validation script
- Workflow and validation patterns
- Progressive disclosure implementation

---

**Created with Skills Factory** - Meta-skill for production-ready Claude Code skills
