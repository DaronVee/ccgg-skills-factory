---
name: skills-factory
description: Meta-skill for creating production-ready Claude Code skills using evaluation-driven development, progressive disclosure patterns, comprehensive validation, and two-Claude iterative methodology
---

# Skills Factory

A comprehensive meta-skill for creating, validating, and iterating on production-ready Claude Code skills.

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
Before writing ANY YAML frontmatter, read and follow [references/FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md). Run through the 6-question decision guide to determine which frontmatter fields this skill needs. This ensures you collect the right context about invocation patterns, execution context, arguments, tool access, dynamic data, and hooks BEFORE generating the YAML.

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
python /path/to/init_skill.py my-skill-name
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
- Run through the Frontmatter Decision Guide (Step 2) to determine which fields to configure
- Replace ALL `TODO:` placeholders in YAML frontmatter
- Draft description with key trigger terms (max 1024 chars)
- Ensure name is hyphen-case (lowercase + hyphens only)
- Review commented optional fields and uncomment those needed

**See:** Bundled `scripts/init_skill.py`

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

Control when and how your skill is triggered:

| `disable-model-invocation` | `user-invocable` | Result |
|---------------------------|-----------------|--------|
| omitted (false) | omitted (true) | **Default**: Claude + user can invoke |
| `true` | omitted (true) | **Manual only**: User invokes with `/name`, Claude cannot auto-load |
| omitted (false) | `false` | **Auto-only**: Claude can invoke, hidden from `/` menu |
| `true` | `false` | **Disabled**: Neither can invoke (rarely useful) |

**Rule of thumb**: If the skill has side effects (deploy, send, delete, publish), use `disable-model-invocation: true`.

#### String Substitutions

Skills can accept arguments from the user:

| Variable | Meaning | Example |
|----------|---------|---------|
| `$ARGUMENTS` | All arguments as string | `/fix-issue 42` → `$ARGUMENTS` = `"42"` |
| `$0` or `$ARGUMENTS[0]` | First argument | `/convert file.md pdf` → `$0` = `"file.md"` |
| `$1` or `$ARGUMENTS[1]` | Second argument | `/convert file.md pdf` → `$1` = `"pdf"` |
| `${CLAUDE_SESSION_ID}` | Current session ID | Useful for unique output paths |

**Auto-append**: If `$ARGUMENTS` doesn't appear in skill content, arguments are automatically appended to the end.

**Example parameterized skill:**
```yaml
---
name: fix-issue
description: Fix a GitHub issue by number
argument-hint: "[issue-number]"
---
Look up issue $ARGUMENTS using `gh issue view $ARGUMENTS`.
Analyze the issue, implement a fix, and create a PR.
```

#### Dynamic Context Injection

Skills can inject live shell data (git status, GitHub info, system state) into their content at load time using a special syntax. Commands execute BEFORE skill content reaches Claude.

**Full documentation with examples and patterns:** See [references/FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md) — Question 5: "Does this skill need dynamic data?"

#### Advanced Patterns

- **`ultrathink`**: Include this keyword in skill content to enable extended thinking mode for complex analysis
- **Skill character budget**: Total skill descriptions use ~2% of context window. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable
- **Subagent integration**: Skills can spawn subagents (`context: fork`) or be preloaded into subagents (`skills:` field). See [references/SUBAGENT_PATTERNS.md](references/SUBAGENT_PATTERNS.md)

**SKILL.md Body Guidelines:**
- Start with clear "About" section explaining purpose
- Use concrete examples over abstract explanations
- Break complex workflows into numbered steps
- Reference detailed content (don't inline everything)
- Keep total SKILL.md under 500 lines (ideally under 200)

**Progressive Disclosure Rules:**
- Reference files ONE level deep: `[Guide](references/guide.md)` OK
- No nested references: `references/category/subcategory/file.md` NOT OK
- Load scripts when needed: "Run validation: `bash scripts/validate.py`"
- Front-load critical info, defer details to references

**Workflow Integration:**
- Add validation checkpoints after key steps
- Design feedback loops for quality assurance
- Use scripts to automate validation (not punt to Claude)
- Provide clear error messages with actionable fixes

**See:** [references/WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md), [references/VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md)

### Step 5: Validate & Package

Ensure quality before distribution:

**Comprehensive Validation:**
```bash
python scripts/comprehensive_validate.py /path/to/my-skill-name
```

This checks:
- YAML structure and field validity (including new fields: context, agent, model, etc.)
- Naming conventions (hyphen-case, no invalid chars)
- Description quality (length, clarity, trigger terms)
- Progressive disclosure (file references one-level deep)
- Best practices (no absolute paths, TODO markers, etc.)
- Content quality (examples present, clear structure)
- Workflow validation (if workflows present)
- Fork validation (if `context: fork`, checks for task instructions)

**Fix all errors and warnings before packaging.**

**Package for Distribution:**
```bash
python scripts/package_skill.py /path/to/my-skill-name
```

Creates: `my-skill-name.zip` ready for sharing or installation.

**See:** Bundled `scripts/comprehensive_validate.py` and `scripts/package_skill.py`

### Step 6: Iterate Using Two-Claude Methodology

Most skills require iteration to reach production quality. Use the **Two-Claude Method**:

**Claude A (Builder):**
- Has the skill loaded in their environment
- Performs realistic tasks the skill should help with
- Documents behavior, errors, confusion points
- Takes notes on what works and what doesn't

**Claude B (Tester/Observer):**
- Reviews Claude A's session logs and outputs
- Analyzes where the skill succeeded vs. failed
- Identifies improvement opportunities
- Proposes specific edits to skill files

**Iteration Cycle:**
1. Claude A uses the skill on realistic task
2. Observe and document behavior (what happened?)
3. Claude B analyzes session (what should change?)
4. Edit skill files based on findings
5. Re-validate with comprehensive_validate.py
6. Repeat until skill performs well consistently

**Key Observation Points:**
- Did Claude invoke the skill when appropriate?
- Did the skill provide sufficient guidance?
- Were workflows clear and easy to follow?
- Did validation catch errors effectively?
- What caused confusion or errors?
- For forked skills: Did the subagent return a useful summary?
- For `disable-model-invocation` skills: Did it correctly NOT auto-trigger?

**See:** [references/TWO_CLAUDE_METHODOLOGY.md](references/TWO_CLAUDE_METHODOLOGY.md) for complete iteration framework.

### Step 7: Deploy & Distribute

After validation and iteration, deploy your skill so Claude can use it.

**Deploy to Claude Code:**

For personal use (across all projects):
```bash
python scripts/package_skill.py my-skill --install personal
```
Installs to `~/.claude/skills/my-skill/` - immediately available in all Claude Code sessions.

For team/project use (shared via git):
```bash
python scripts/package_skill.py my-skill --install project
git add .claude/skills/my-skill/
git commit -m "Add my-skill for team workflows"
git push
```
Team members get skill automatically on `git pull`.

**Deploy to Claude.ai / Claude Desktop:**
```bash
python scripts/package_skill.py my-skill --package
```
Upload generated `my-skill.zip` via Settings > Features.

**Deploy to Claude API:**
Upload via `/v1/skills` endpoint for organization-wide availability.

**Verification:**
- Claude Code: Ask "What skills are available?"
- Claude.ai/Desktop: Check Settings > Features shows skill
- API: List skills via API endpoint

**Important:** Skills **do not sync across surfaces**. Must deploy separately to each platform (Code, .ai, Desktop, API).

**See:** [references/DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md) for complete deployment workflows, surface-specific instructions, and team distribution strategies.

## Troubleshooting

**Common Issues:**
- "Claude doesn't use my skill" → Check description triggers, YAML validity, `disable-model-invocation` not accidentally set
- "Skill loaded but ignored" → Add concrete examples, improve clarity
- "Skill triggers when it shouldn't" → Use `disable-model-invocation: true`
- "Validation failing" → Run comprehensive_validate.py for specific errors
- "Skill too complex" → Apply progressive disclosure, move content to references
- "Skill created but not available" → Check installation location, use --install flag
- "Skill works in Code but not .ai" → Skills don't sync, must upload separately
- "Team doesn't have skill" → Commit to git (project) or share zip (other surfaces)
- "Some skills not loading" → Character budget exceeded, shorten descriptions
- "Forked skill returns poor results" → Ensure body has task instructions, not just reference material

**See:** [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for comprehensive troubleshooting guide.

## Reference Documentation

- **[FRONTMATTER_DECISION_GUIDE.md](references/FRONTMATTER_DECISION_GUIDE.md)** - Intelligent YAML configuration wizard (6-question decision tree)
- **[SUBAGENT_PATTERNS.md](references/SUBAGENT_PATTERNS.md)** - Skill/subagent integration (fork patterns, agent skills loading)
- **[EVALUATION_GUIDE.md](references/EVALUATION_GUIDE.md)** - Evaluation-driven development methodology
- **[TWO_CLAUDE_METHODOLOGY.md](references/TWO_CLAUDE_METHODOLOGY.md)** - Complete iterative testing framework
- **[WORKFLOW_PATTERNS.md](references/WORKFLOW_PATTERNS.md)** - Workflow design patterns and examples
- **[VALIDATION_PATTERNS.md](references/VALIDATION_PATTERNS.md)** - Feedback loops and validation strategies
- **[DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md)** - Complete deployment and distribution guide
- **[TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Common issues and solutions

## Example Skills

See `references/examples/` for annotated example skills demonstrating best practices:
- **simple-skill/** - Minimal viable skill (commit-helper)
- **standard-skill/** - Moderate complexity with references (pdf-processor)
- **complex-skill/** - Full progressive disclosure (data-analysis)

Each example includes `ANNOTATIONS.md` explaining architectural decisions.

## Scripts

- **init_skill.py** - Generate new skill from template
- **comprehensive_validate.py** - Deep validation (structure, content, best practices)
- **package_skill.py** - Create distributable .zip file

## Version History

**v2.0.0** (2026-02-09)
- Complete frontmatter reference: all 11 official YAML fields documented
- Intelligent Frontmatter Decision Guide: 6-question wizard for configuring new skills
- Subagent integration patterns: context: fork, agent types, skills field in agents
- Invocation control: disable-model-invocation, user-invocable, decision matrix
- String substitutions: $ARGUMENTS, $N, ${CLAUDE_SESSION_ID}
- Dynamic context injection: exclamation-backtick syntax (examples moved to reference)
- Advanced patterns: ultrathink, character budget, argument patterns
- Fixed priority resolution order: enterprise > personal > project
- Fixed allowed-tools format: comma-separated string (not YAML list)
- Updated name/description status: recommended (not required, defaults exist)
- New reference: FRONTMATTER_DECISION_GUIDE.md
- New reference: SUBAGENT_PATTERNS.md
- Updated validation script with new field recognition

**v1.1.0** (2025-10-19)
- Added deployment layer with cross-surface support
- Enhanced package_skill.py with --install flag (personal/project)
- Enhanced init_skill.py with interactive location prompt
- Created DEPLOYMENT_GUIDE.md reference (~4,000 words)
- Added deployment troubleshooting (Issues 9-12)
- Complete end-to-end workflow: creation -> deployment -> distribution

**v1.0.0** (2025-10-19)
- Initial production release
- Evaluation-driven development framework
- Two-Claude iterative methodology
- Comprehensive validation script
- Workflow patterns (Sequential, Checklist, Conditional, Iterative)
- Validation patterns (Script-based, Reference-based, Plan-validate-execute, Multi-stage)
- Progressive disclosure implementation
- Troubleshooting guide (8 common issues)

---

**Created with Skills Factory** - Meta-skill for production-ready Claude Code skills
