# Frontmatter Configuration Guide

## Purpose

This guide ensures you collect the right context about the skill being built BEFORE writing any YAML frontmatter. Each question maps to specific frontmatter fields. Skip questions where the default answer applies.

**MANDATORY**: Run through all 6 questions before generating the YAML frontmatter for any new skill.

---

## Question 1: Invocation Pattern

**Ask**: "How should this skill be triggered?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) Both Claude and user** (default) | No special fields needed | Claude auto-loads when description matches context; user can also invoke with `/name` |
| **B) User-only (manual trigger)** | `disable-model-invocation: true` | Only user can invoke with `/name`. Claude will NOT auto-load this skill. Description is NOT added to context. |
| **C) Claude-only (background knowledge)** | `user-invocable: false` | Hidden from `/` menu. Only Claude can invoke. For reference material Claude should discover automatically. |

### How to Determine the Right Answer

Ask these probing questions about the skill:

- **Does this skill have side effects?** (deploy, send messages, delete data, publish) → **B** (user-only)
  - *Why*: Side-effect skills should never auto-trigger
- **Is this a convention, guideline, or reference document?** → **C** (Claude-only)
  - *Why*: Users don't invoke these; Claude references them when relevant
- **Is this a general-purpose workflow or helper?** → **A** (both)
  - *Why*: Maximum accessibility for common tasks

### Examples

| Skill | Answer | Reasoning |
|-------|--------|-----------|
| `commit-helper` | A (both) | General workflow, safe to auto-load |
| `deploy-production` | B (user-only) | Has side effects (deployment) |
| `api-conventions` | C (Claude-only) | Reference material, not a task |
| `code-review` | A (both) | General workflow, safe to auto-load |
| `send-slack-notification` | B (user-only) | Has side effects (sends messages) |
| `project-architecture` | C (Claude-only) | Background knowledge reference |

### Invocation Control Decision Matrix

| `disable-model-invocation` | `user-invocable` | Result |
|---------------------------|-----------------|--------|
| omitted (false) | omitted (true) | **Default**: Claude + user can invoke |
| `true` | omitted (true) | **Manual only**: User invokes with `/name`, Claude cannot auto-load |
| omitted (false) | `false` | **Auto-only**: Claude can invoke, hidden from `/` menu |
| `true` | `false` | **Disabled**: Neither can invoke (rarely useful) |

---

## Question 2: Execution Context

**Ask**: "Should this skill run in the main conversation or in an isolated subagent?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) Main conversation** (default) | No `context` field | Skill runs in current chat with full conversation history |
| **B) Isolated subagent** | `context: fork` | Skill runs in a fresh subagent with NO conversation history |

### When to Choose Isolated (Fork)

Choose `context: fork` when:
- **Context window protection**: Skill generates heavy output (research, analysis) that would bloat main context
- **Self-contained task**: Skill doesn't need conversation history to execute
- **Parallel execution**: Task can run independently alongside other work
- **Tool restriction**: Want to limit what the skill can do (read-only research, etc.)

### When NOT to Fork

Stay in main conversation when:
- Skill is reference material / guidelines (no task to execute in isolation)
- Skill needs conversation history for context
- Skill requires interactive back-and-forth with user
- Latency matters (subagents start fresh, slower startup)

### Follow-up Questions (Only if Answer B: Fork)

**2a. What kind of work does the subagent do?**

| Work Type | Configuration | Use Case |
|-----------|--------------|----------|
| Read-only research/exploration | `agent: Explore` | Codebase research, file analysis, documentation review |
| Full capability (read + write + bash) | `agent: general-purpose` | Complete tasks, generate files, run commands |
| Planning/analysis only | `agent: Plan` | Architecture planning, strategy analysis |
| Custom specialized agent | `agent: <custom-agent-name>` | Agents defined in `.claude/agents/` |

**2b. Should the subagent use a specific model?**

| Need | Configuration |
|------|--------------|
| Fast/cheap tasks (simple searches, formatting) | `model: haiku` |
| Complex analysis (deep research, nuanced writing) | `model: opus` |
| Balanced (default behavior) | `model: sonnet` |
| Same as main conversation | `model: inherit` (or omit) |

### Critical Warning for Fork Skills

When `context: fork` is set, the skill content becomes the subagent's ONLY context. The subagent has:
- NO conversation history
- NO knowledge of what the user asked before
- ONLY the skill's SKILL.md content + any CLAUDE.md files

**Therefore**: Fork skills MUST contain explicit task instructions (not just reference material). The skill body should read like a complete task prompt.

**Good fork skill body**:
```markdown
Research the codebase to find all API endpoints. For each endpoint, document:
- HTTP method and path
- Request/response schema
- Authentication requirements
Output a structured markdown report.
```

**Bad fork skill body** (will produce poor results in fork):
```markdown
## API Conventions
- Use REST standards
- Always validate inputs
- Return proper status codes
```

---

## Question 3: Arguments

**Ask**: "Does this skill accept input parameters from the user?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) No arguments** (default) | No special fields | Skill works without user-provided parameters |
| **B) Single argument** | Add `argument-hint` + use `$ARGUMENTS` in body | User provides one value when invoking |
| **C) Multiple arguments** | Add `argument-hint` + use `$0`, `$1`, `$2` in body | User provides multiple values |

### Probing Questions

- What does the user need to specify when invoking this skill? → That's the argument
- If nothing → No arguments needed

### Argument Configuration

**Single argument example** (fix a specific issue):
```yaml
---
name: fix-issue
description: Fix a GitHub issue by number
argument-hint: "[issue-number]"
---

Look up issue $ARGUMENTS using `gh issue view $ARGUMENTS`.
Analyze the issue, implement a fix, and create a PR.
```

**Multiple arguments example** (convert file format):
```yaml
---
name: convert-format
description: Convert a file from one format to another
argument-hint: "[source-file] [target-format]"
---

Convert `$0` to `$1` format.
Read the source file, transform the content, and write the output.
```

### String Substitution Reference

| Variable | Meaning | Example |
|----------|---------|---------|
| `$ARGUMENTS` | All arguments as a single string | `/fix-issue 42` → `$ARGUMENTS` = `"42"` |
| `$0` or `$ARGUMENTS[0]` | First argument | `/convert README.md pdf` → `$0` = `"README.md"` |
| `$1` or `$ARGUMENTS[1]` | Second argument | `/convert README.md pdf` → `$1` = `"pdf"` |
| `$N` or `$ARGUMENTS[N]` | Nth argument (0-indexed) | Any positional argument |
| `${CLAUDE_SESSION_ID}` | Current session ID | Useful for unique output paths |

**Auto-append behavior**: If `$ARGUMENTS` does not appear anywhere in the skill content, arguments are automatically appended to the end of the skill body. This means simple skills work without explicit `$ARGUMENTS` placement.

---

## Question 4: Tool Access

**Ask**: "Should this skill restrict which tools Claude can use?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) All tools** (default) | No `allowed-tools` field | Full tool access |
| **B) Read-only** | `allowed-tools: Read, Grep, Glob` | Can only read, search - no modifications |
| **C) Specific tool set** | `allowed-tools: <comma-separated>` | Custom tool subset |
| **D) Bash with restrictions** | `allowed-tools: Bash(pattern), ...` | Bash limited to matching commands |

### Probing Questions

- Should this skill be able to modify files? If no → **B**
- Does the skill need Bash for specific commands only? → **D**
- Does the skill need only a subset of tools? → **C**
- Full capability needed? → **A**

### Format

`allowed-tools` uses a **comma-separated string** (not a YAML list):

```yaml
# Correct format
allowed-tools: Read, Grep, Glob

# Also correct - Bash with argument pattern
allowed-tools: Bash(gh *), Bash(git status), Read, Grep, Glob

# INCORRECT - do not use YAML list format
allowed-tools:
  - Read
  - Grep
```

### Available Tools

`Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `Task`, `Skill`

### Bash Argument Patterns

Restrict Bash to specific command patterns:
- `Bash(gh *)` - Only GitHub CLI commands
- `Bash(git status)` - Only `git status`
- `Bash(npm test)` - Only `npm test`
- `Bash(py scripts/*)` - Only Python scripts in scripts/

### Examples

| Skill | Configuration | Reasoning |
|-------|--------------|-----------|
| Code auditor | `allowed-tools: Read, Grep, Glob` | Should never modify code |
| GitHub reviewer | `allowed-tools: Bash(gh *), Read, Grep, Glob` | Only needs GH CLI + reading |
| File organizer | `allowed-tools: Read, Write, Edit, Glob` | No Bash needed |
| Full assistant | (omit field) | Needs all tools |

---

## Question 5: Dynamic Data

**Ask**: "Does this skill need live data injected before execution?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) No dynamic data** (default) | No special syntax | Skill content is static |
| **B) Needs live data from shell commands** | Use `` !`command` `` syntax in skill body | Commands run BEFORE skill content is sent to Claude |

### How Dynamic Context Injection Works

The `` !`command` `` syntax executes a shell command and injects its output directly into the skill content before Claude sees it. This happens at load time, not runtime.

### Examples

**Git-aware skill**:
```markdown
## Current Repository State

!`git status`

## Recent Changes

!`git log --oneline -5`

## Instructions

Based on the repository state above, suggest the next development steps.
```

**GitHub-aware skill**:
```markdown
## Open Issues

!`gh issue list --limit 10`

## Pull Requests

!`gh pr list --limit 5`

## Instructions

Prioritize the open issues and suggest which PR to review first.
```

**System-aware skill**:
```markdown
## Environment

Current user: !`whoami`
Current date: !`date`
Working directory: !`pwd`

## Instructions

Generate a daily status report for the current user.
```

### When to Use Dynamic Data

- Skill behavior depends on current git state
- Skill needs to reference current issues/PRs
- Skill output changes based on environment
- Skill needs current date/time for formatting

### When NOT to Use

- Static instructions (most skills)
- Commands that are slow or could fail
- Commands that expose sensitive data (API keys, passwords)

---

## Question 6: Hooks

**Ask**: "Does this skill need pre/post execution validation?"

| Answer | Configuration | Description |
|--------|--------------|-------------|
| **A) No hooks** (default, most skills) | No `hooks` field | Standard execution |
| **B) Pre-tool validation** | Add `hooks:` with `PreToolUse` | Validate before Claude uses a tool |
| **C) Post-execution actions** | Add `hooks:` with `PostToolUse` or `Stop` | Run actions after tool use or skill completion |

### When to Use Hooks

Hooks are rarely needed for skills. Use them when:
- You need to enforce safety checks (e.g., prevent writes to certain directories)
- You need logging or audit trails
- You need to transform tool outputs before Claude sees them
- You need cleanup after skill execution

### Hook Configuration Example

```yaml
---
name: safe-editor
description: Edit files with safety guardrails
hooks:
  PreToolUse:
    - matcher: Write
      command: "node scripts/validate-write-target.js"
  PostToolUse:
    - matcher: Edit
      command: "node scripts/log-edit.js"
---
```

### Important

- Hooks add complexity - only use when there's a clear safety or workflow need
- Hook commands must exist and be executable
- Hook failures can block skill execution (by design, for safety)

---

## Summary: Generate Your Frontmatter

After collecting answers to all 6 questions, generate the YAML frontmatter using ONLY the fields that apply. Start with the minimal template and add fields based on answers:

```yaml
---
name: <skill-name>
description: |
  <Clear description of what this skill does.
  Include key terms that should trigger the skill.
  Focus on capabilities and use cases. Max 1024 chars.>
# --- Add only the fields indicated by your answers above ---
# From Q1 (if B): disable-model-invocation: true
# From Q1 (if C): user-invocable: false
# From Q2 (if B): context: fork
# From Q2b (if fork): agent: <Explore|Plan|general-purpose|custom-name>
# From Q2c (if override): model: <haiku|sonnet|opus|inherit>
# From Q3 (if B/C): argument-hint: "[your-arguments]"
# From Q4 (if B/C/D): allowed-tools: <comma-separated tools>
# From Q6 (if B/C): hooks: <hook configuration>
---
```

### Common Configurations (Quick Reference)

| Skill Type | Frontmatter Fields |
|------------|-------------------|
| **Simple helper** (commit, format, lint) | `name` + `description` only |
| **Dangerous action** (deploy, send, delete) | + `disable-model-invocation: true` |
| **Background knowledge** (conventions, standards) | + `user-invocable: false` |
| **Research skill** (explore, analyze, audit) | + `context: fork` + `agent: Explore` |
| **Parameterized task** (fix-issue, process-file) | + `argument-hint` + `$ARGUMENTS` in body |
| **Read-only skill** (review, audit, analyze) | + `allowed-tools: Read, Grep, Glob` |
| **Forked research with restrictions** | + `context: fork` + `agent: Explore` + `allowed-tools: Read, Grep, Glob` |

---

## Metadata Field (Optional, Non-Standard)

The `metadata` field stores custom key-value pairs for tracking and categorization. It is NOT part of the official Claude Code skill spec but is supported as a pass-through.

```yaml
metadata:
  author: "TeamName"
  version: "2.0.0"
  category: "content-creation"
  last-updated: "2026-02-09"
```

Use for: version tracking, team ownership, categorization, custom IDs.

**Important**: Use unique key names to avoid conflicts with future official fields.

---

**Remember**: Most skills only need `name` + `description`. Only add fields that your answers indicate are necessary. Simpler frontmatter = fewer things to go wrong.
