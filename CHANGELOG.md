# Changelog

All notable changes to Skills Factory will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-02-09 - Full Feature Alignment

### Added
- **FRONTMATTER_DECISION_GUIDE.md**: 6-question intelligent configuration wizard for YAML frontmatter
- **SUBAGENT_PATTERNS.md**: Bidirectional skill/subagent integration patterns (context: fork + skills field)
- **Complete YAML frontmatter reference** (11 fields): name, description, disable-model-invocation, user-invocable, context, agent, model, argument-hint, allowed-tools, hooks, metadata
- **Invocation Control matrix**: decision table for disable-model-invocation vs user-invocable
- **String Substitutions**: $ARGUMENTS, $N, ${CLAUDE_SESSION_ID}
- **Dynamic Context Injection**: !`command` syntax for live shell data
- **Advanced Patterns**: ultrathink keyword, character budget management, forked context workflow
- **3 new troubleshooting issues**: #13 budget exceeded, #14 unwanted triggers, #15 fork failures
- **Fork evaluation scenarios** in EVALUATION_GUIDE.md
- **Pattern 5: Forked Context Workflow** in WORKFLOW_PATTERNS.md
- **Deployment Guide additions**: nested directory auto-discovery, --add-dir support, expanded plugin namespacing

### Changed
- **SKILL.md** rewritten: Step 2 now triggers Frontmatter Decision Guide (MANDATORY)
- **comprehensive_validate.py**: recognizes all new fields, validates context: fork content, supports comma-separated allowed-tools (official format)
- **init_skill.py**: template includes commented optional fields with guide reference, name length 40 -> 64

### Fixed
- **Priority resolution order**: was "project > personal" (WRONG), now "enterprise > personal > project" (CORRECT)
- **Name max length**: was "40 chars", now "64 chars" (per official docs)
- **Removed SlashCommand** from valid tools list (deprecated)

---

## [1.1.0] - 2025-11-07 - CCGG Community Edition

### Added
- **GitHub Distribution**: Packaged for CCGG community distribution
- **Comprehensive Documentation**:
  - Installation guide with three-tier approach (quick/detailed/beginner)
  - Platform compatibility guide (Claude Code, Desktop, Web)
  - FAQ with troubleshooting
- **Platform Support Clarification**: All platforms (Code, Desktop, Web) support script execution
- **Attribution**: Proper credit to Daron Vener and CCGG community

### Changed
- **README.md**: Enhanced with quick start, platform compatibility matrix, comprehensive feature overview
- **SKILL.md**: Added prerequisites section with platform requirements
- **Deployment workflows**: Simplified installation instructions for all platforms

### Documentation
- **Platform Requirements**: Clarified "Code execution and file creation" setting requirement for Desktop/Web
- **Sandbox Details**: Documented server-side sandbox (Ubuntu 24.04.2, Python 3.12.3) vs local execution
- **Zero Dependencies**: Emphasized pure Python standard library (no pip installs needed)

---

## [1.0.0] - 2025-10-XX - Initial Release

### Added
- **Core Skill**: SKILL.md with progressive disclosure framework
- **Automation Scripts** (4 files):
  - `comprehensive_validate.py`: Deep validation with 12+ checks
  - `init_skill.py`: Skill generator and scaffolding
  - `package_skill.py`: Packager/installer for distribution
  - `quick_validate.py`: Fast validation for iteration
- **Reference Guides** (6 files):
  - `DEPLOYMENT_GUIDE.md`: Complete deployment workflows
  - `EVALUATION_GUIDE.md`: Evaluation-driven development methodology
  - `TROUBLESHOOTING.md`: 12 common issues + solutions
  - `TWO_CLAUDE_METHODOLOGY.md`: Iterative testing framework
  - `VALIDATION_PATTERNS.md`: Feedback loop patterns
  - `WORKFLOW_PATTERNS.md`: Design patterns for skills

### Features
- **Progressive Disclosure**: Three-tier information architecture
- **Evaluation-Driven Development**: Iterative quality framework
- **Comprehensive Validation**: Four validation levels (quick, comprehensive, two-claude, production)
- **Design Patterns**: Simple, standard, and complex skill architectures
- **Cross-Platform Support**: Works in Claude Code, Desktop, and Web

---

## Upcoming

### [2.1.0] - Future
- **Example Skills**: Pre-built skills demonstrating each pattern (simple, standard, forked, subagent)
- **Hooks Integration**: Deeper hooks validation and generation in skill creation workflow
- **Plugin Packaging**: Automated plugin creation from skill collections
- **Agent Skills Standard**: agentskills.io compatibility layer

---

**Maintained by**: Daron Vener | [CCGG Community](https://www.skool.com/ccgg)
