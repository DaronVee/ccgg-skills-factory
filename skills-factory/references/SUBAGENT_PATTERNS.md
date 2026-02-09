# Skill + Subagent Integration Patterns

## Overview

Skills and subagents interact in **two directions**:

| Direction | Mechanism | What Happens |
|-----------|-----------|-------------|
| **Skill spawns Subagent** | `context: fork` in skill YAML | Skill content becomes a subagent's task. Runs in isolation. |
| **Subagent uses Skills** | `skills:` field in agent YAML | Full skill content injected into subagent at startup as reference. |

These are complementary patterns that solve different problems. Understanding both is essential for building sophisticated skill architectures.

---

## Pattern A: Skill Spawning a Subagent (`context: fork`)

### How It Works

When a skill has `context: fork` in its YAML frontmatter:

1. User invokes skill (e.g., `/research-codebase`)
2. Claude Code creates a **new, isolated subagent**
3. The skill's SKILL.md body becomes the subagent's task prompt
4. Subagent executes with **NO conversation history** - only SKILL.md content + CLAUDE.md files
5. Subagent completes its work
6. Results are **summarized back** to the main conversation

### Configuration

```yaml
---
name: research-codebase
description: Deep codebase research and analysis
context: fork              # REQUIRED: Creates isolated subagent
agent: Explore             # OPTIONAL: Subagent type (default: general-purpose)
model: haiku               # OPTIONAL: Model override
allowed-tools: Read, Grep, Glob  # OPTIONAL: Restrict subagent tools
---

Research the codebase thoroughly. Find all API endpoints, document their
request/response schemas, and identify patterns. Output a comprehensive
markdown report.
```

### Available Agent Types

| Agent Type | Capabilities | Best For |
|-----------|-------------|----------|
| `Explore` | Read-only exploration (Glob, Grep, Read) | Codebase research, file analysis |
| `Plan` | Analysis and planning (no writes) | Architecture planning, strategy |
| `general-purpose` | Full capabilities (read + write + bash) | Complete tasks, file generation |
| `<custom-agent-name>` | Custom agent from `.claude/agents/` | Specialized workflows |

### Important Constraints

- **No nesting**: Subagents CANNOT spawn other subagents (no recursive forking)
- **No history**: Forked skills have ZERO conversation context - write self-contained instructions
- **CLAUDE.md loads**: The project's CLAUDE.md hierarchy IS loaded in forked context
- **Results summarized**: Verbose subagent output is condensed before returning to main context
- **Latency**: Subagents start fresh, so expect slightly longer execution time

---

### Use Case 1: Context Window Protection

**Problem**: Deep research or analysis generates massive output that bloats the main conversation context, leaving less room for subsequent tasks.

**Solution**: Fork to an Explore agent. The subagent's verbose research stays in its isolated context. Only a summary returns to the main conversation.

**Example: Deep Codebase Research Skill**

```yaml
---
name: deep-research
description: Comprehensive codebase research that protects main context from output bloat
context: fork
agent: Explore
model: haiku
---

# Deep Codebase Research

Thoroughly explore the codebase to answer the research question below.

## Research Process

1. Start with broad file discovery (Glob for relevant patterns)
2. Read key files identified in step 1
3. Search for specific patterns (Grep for function names, imports, etc.)
4. Cross-reference findings across files
5. Synthesize into a structured report

## Output Format

Provide a structured markdown report with:
- **Summary** (3-5 sentences of key findings)
- **Detailed Findings** (organized by topic)
- **File References** (paths and line numbers for key code)
- **Recommendations** (if applicable)

## Research Question

$ARGUMENTS
```

**Usage**: `/deep-research how does authentication work in this project?`

**Why this works**: The Explore agent reads dozens of files and generates detailed notes internally. Only the final structured report returns to the main conversation, preserving context for follow-up work.

---

### Use Case 2: Parallel Execution

**Problem**: Multiple independent research tasks need to happen simultaneously, but doing them sequentially is slow.

**Solution**: Fork multiple skills (or Claude spawns multiple subagents from one skill). Each runs independently and returns results.

**Example: Multi-Module Analysis Skill**

```yaml
---
name: module-analysis
description: Analyze a specific module's architecture, dependencies, and test coverage
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# Module Analysis

Analyze the module specified below. Provide:

1. **Architecture**: Key files, classes, patterns used
2. **Dependencies**: Internal and external dependencies
3. **Test Coverage**: What's tested, what's missing
4. **Code Quality**: Potential issues, complexity hotspots

## Module to Analyze

$ARGUMENTS
```

**Usage** (Claude or user can invoke multiple times):
```
Analyze these modules in parallel:
/module-analysis src/auth/
/module-analysis src/api/
/module-analysis src/database/
```

**Important notes on parallel forking**:
- Each fork runs independently with its own context
- Results return to main context (watch for context inflation if many forks)
- For sustained parallelism with inter-agent communication, consider agent teams instead
- Subagents cannot communicate with each other - only with the main conversation

---

### Use Case 3: Tool Restriction

**Problem**: A skill should only read and analyze code, never modify it. But you can't guarantee Claude won't try to "help" by editing files.

**Solution**: Fork with restricted tools. The subagent physically cannot access tools not in `allowed-tools`.

**Example: Code Audit Skill**

```yaml
---
name: security-audit
description: Read-only security audit of codebase - identifies vulnerabilities without modifying code
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# Security Audit

Perform a thorough security review of the codebase. You are in READ-ONLY mode
and cannot modify any files.

## Audit Checklist

1. **Input Validation**: Check all user inputs are validated/sanitized
2. **Authentication**: Review auth flows for weaknesses
3. **Authorization**: Check access control patterns
4. **Data Exposure**: Look for sensitive data in logs, responses, config
5. **Dependencies**: Check for known vulnerable patterns
6. **Injection**: Search for SQL injection, XSS, command injection risks

## Output

Produce a security audit report with:
- **Critical** findings (immediate action needed)
- **High** findings (should fix soon)
- **Medium** findings (plan to address)
- **Low** findings (best practice improvements)
- **Info** findings (observations, no action needed)

For each finding, include: file path, line number, description, recommended fix.
```

**Why fork + tool restriction?**: Even without fork, `allowed-tools` restricts tool access. But combining with fork adds context isolation - the audit report doesn't consume main context, and the subagent can't accidentally modify files even if the skill instructions had a bug.

**Alternative without fork**: You can use `allowed-tools` without `context: fork` if you want the audit to run in the main conversation (e.g., for interactive follow-up questions about findings).

---

### When NOT to Use Fork

| Situation | Why Not Fork | Better Approach |
|-----------|-------------|-----------------|
| Skill is pure reference/guidelines | No task to execute in isolation | Omit `context` (or use `user-invocable: false`) |
| Need conversation history | Fork has zero context | Omit `context` (runs in main conversation) |
| Interactive back-and-forth needed | Fork runs to completion, then returns | Omit `context` |
| Quick, simple tasks | Fork overhead not justified | Omit `context` |
| Skill needs to modify files in user's project context | May work, but loses conversational awareness | Omit `context` unless modifications are self-contained |

---

## Pattern B: Subagent Using Skills (`skills` field)

### How It Works

Subagents (defined in `.claude/agents/<name>.md`) can preload skills via the `skills:` field in their YAML frontmatter:

1. Agent is spawned (via Task tool or agent teams)
2. At startup, ALL skills listed in `skills:` are loaded
3. **Full skill content** is injected into the agent's context (not just the description)
4. Skills serve as **reference material** - the agent can read and follow them
5. Agent does NOT get skills from the parent conversation - only explicitly listed ones

### Configuration (in agent frontmatter)

```yaml
---
name: api-builder
description: Builds API endpoints following project conventions
tools: [Read, Write, Edit, Grep, Glob, Bash]
model: sonnet
skills: [api-conventions, error-handling-standards, test-patterns]
---

You are an API builder agent. Build the requested API endpoint following
the conventions and patterns loaded from your skills.
```

### Key Behaviors

| Aspect | Behavior |
|--------|---------|
| **Content loading** | Full SKILL.md body + referenced files loaded at startup |
| **Inheritance** | Subagents do NOT inherit skills from parent conversation |
| **Discovery** | Skills must exist in standard locations (`~/.claude/skills/` or `.claude/skills/`) |
| **Invocation** | Skills are context, not commands - agent reads them as reference |
| **Multiple skills** | List multiple skill names: `skills: [skill-a, skill-b, skill-c]` |

### Use Cases

**Domain-specific agents with specialized knowledge**:
```yaml
---
name: frontend-builder
skills: [react-conventions, design-system, accessibility-standards]
---
```

**Convention-following agents**:
```yaml
---
name: code-reviewer
skills: [code-review-checklist, testing-requirements, documentation-standards]
---
```

**Agents that need reference material without runtime loading**:
```yaml
---
name: data-migrator
skills: [database-schema, migration-patterns, rollback-procedures]
---
```

### Important Distinctions

| Aspect | Skills in agents (`skills:` field) | Skills in main conversation |
|--------|-----------------------------------|----------------------------|
| Loading | Full content at startup | Description always; full content on invoke |
| Invocation | Not invocable (reference only) | User (`/name`) or Claude (auto) |
| Inheritance | Explicitly listed only | Available per scope (personal/project) |
| Purpose | Give agent domain knowledge | Extend Claude's capabilities |

---

## Decision Guide: Which Pattern to Use

### Quick Decision Tree

```
Do you want the SKILL to drive the task?
  ├─ YES → Pattern A (context: fork)
  │        The skill IS the task. Subagent executes skill instructions.
  │
  └─ NO → Does the skill provide knowledge for another task?
          ├─ YES → Pattern B (skills field in agent)
          │        The agent drives the task. Skills are reference material.
          │
          └─ NO → Use standard skill (no fork, no agent)
                  Claude invokes skill when relevant, runs in main conversation.
```

### Detailed Decision Matrix

| Question | Pattern A (Skill → Subagent) | Pattern B (Subagent → Skills) | Standard Skill |
|----------|------------------------------|-------------------------------|----------------|
| Who drives the task? | The skill | The agent | Claude in main conversation |
| Where does it execute? | Isolated subagent | Subagent (Task tool or teams) | Main conversation |
| Conversation history? | None | None (agent starts fresh) | Full history |
| Content role? | Task instructions | Reference material | Guidance for Claude |
| User invokes? | Yes (with `/name`) | No (agent spawned by Claude) | Yes or auto |
| Use case | Self-contained task | Knowledge-enriched agent | Interactive workflow |

### Combining Both Patterns

You CAN combine patterns. A forked skill can reference other skills:

**Skill that forks AND the subagent has preloaded skills**:
This works when the `agent` field points to a custom agent that has `skills:` in its own frontmatter.

```yaml
# SKILL.md for the forked skill
---
name: comprehensive-review
description: Complete code review with conventions checking
context: fork
agent: convention-reviewer
---

Review all changed files in the current branch.
Check each file against the loaded conventions.
```

```yaml
# .claude/agents/convention-reviewer.md
---
name: convention-reviewer
description: Reviews code against loaded convention skills
tools: [Read, Grep, Glob]
skills: [api-conventions, naming-standards, test-requirements]
---

You are a convention reviewer. Use the loaded skills as your
reference for what constitutes correct conventions.
```

**Flow**: User invokes `/comprehensive-review` → Fork creates `convention-reviewer` agent → Agent loads with `api-conventions`, `naming-standards`, `test-requirements` skills as context → Agent reviews code against those conventions → Summary returns to main conversation.

---

## Examples

### Example 1: Research Skill (Context Protection)

```yaml
---
name: architecture-explorer
description: Explore and document project architecture without bloating main context
context: fork
agent: Explore
model: haiku
---

# Architecture Exploration

Explore this project's architecture comprehensively:

1. Identify the main entry points
2. Map the directory structure and module organization
3. Find key abstractions (interfaces, base classes, shared types)
4. Document the data flow (request → processing → response)
5. Identify external dependencies and integration points

## Output

Provide a structured architecture document with:
- High-level overview (2-3 paragraphs)
- Module dependency diagram (text-based)
- Key file reference table (file → purpose)
- Architecture patterns identified
- Potential improvement areas
```

### Example 2: Code Audit Skill (Tool Restriction)

```yaml
---
name: dependency-audit
description: Audit project dependencies for security and maintenance risks (read-only)
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# Dependency Audit

Analyze all project dependencies for:

1. **Security**: Known vulnerability patterns in dependency usage
2. **Freshness**: Look for version pinning, outdated patterns
3. **Weight**: Identify heavy dependencies used for simple tasks
4. **Redundancy**: Multiple packages solving the same problem

Read package.json, requirements.txt, Cargo.toml, or equivalent.
Cross-reference with lock files if present.

Output a prioritized report with recommendations.
```

### Example 3: Agent with Preloaded Skills

```yaml
# .claude/agents/content-writer.md
---
name: content-writer
description: Creates content following brand voice and SEO conventions
tools: [Read, Write, Edit, Grep, Glob]
model: sonnet
skills: [brand-voice-guide, seo-conventions, content-templates]
---

You are a content writer for our team. When creating any content:

1. Follow the brand voice guide loaded from skills
2. Apply SEO conventions from your loaded skills
3. Use content templates when available
4. Output final content ready for publication
```

### Example 4: Deploy Skill (Manual Only, No Fork)

```yaml
---
name: deploy-staging
description: Deploy current branch to staging environment
disable-model-invocation: true
argument-hint: "[branch-name]"
---

# Deploy to Staging

Deploy branch `$ARGUMENTS` to staging:

1. Run tests: `npm test`
2. Build: `npm run build`
3. Deploy: `npm run deploy:staging -- --branch $ARGUMENTS`
4. Verify: Check staging URL responds
5. Report deployment status

**WARNING**: This modifies the staging environment. Verify branch name before proceeding.
```

---

## Common Mistakes

### Mistake 1: Forking Reference-Only Skills

```yaml
# BAD: This skill has no task instructions
---
name: api-standards
context: fork        # Fork creates a subagent... to do what?
---
## API Standards
- Use REST conventions
- Validate all inputs
- Return proper error codes
```

**Fix**: Remove `context: fork`. This is reference material, not a task.

### Mistake 2: Expecting Conversation History in Fork

```yaml
# BAD: This references "the file above" which doesn't exist in fork context
---
name: review-file
context: fork
---
Review the file the user mentioned above and provide feedback.
```

**Fix**: Use `$ARGUMENTS` to pass the file path explicitly:
```yaml
---
name: review-file
context: fork
argument-hint: "[file-path]"
---
Review the file at `$ARGUMENTS` and provide detailed feedback.
```

### Mistake 3: Assuming Skills Inherit in Subagents

```yaml
# BAD: Agent won't have commit-helper skill unless explicitly listed
---
name: feature-builder
tools: [Read, Write, Edit, Bash]
# Missing: skills: [commit-helper]
---
Build the feature and use the commit-helper skill to commit.
```

**Fix**: Explicitly list skills the agent needs:
```yaml
---
name: feature-builder
tools: [Read, Write, Edit, Bash]
skills: [commit-helper]
---
```

### Mistake 4: Nesting Subagent Spawns

```yaml
# BAD: Subagents cannot spawn other subagents
---
name: orchestrator
context: fork
---
For each module, spawn an Explore agent to analyze it.
```

**Fix**: Either handle all analysis in a single forked agent, or have the main conversation orchestrate multiple fork invocations.

---

**Remember**: Most skills don't need subagent integration. Only use these patterns when you have a clear need for context isolation (Pattern A) or knowledge injection (Pattern B). Simple skills with just `name` + `description` cover the majority of use cases.
