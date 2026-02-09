# Skills Factory - CCGG Community Edition

**Created by**: [Daron Vener](https://github.com/DaronVee)
**Community**: [CCGG - Custom GPT Goldmine](https://www.skool.com/ccgg)
**Contributors**: Claude Code

Production-ready meta-skill for creating Claude Code skills with evaluation-driven development, progressive disclosure patterns, and comprehensive validation.

---

## Quick Start (Claude Code CLI)

**Step 1**: Download the latest [Release ZIP](https://github.com/DaronVee/ccgg-skills-factory/releases)

**Step 2**: Extract and install

```bash
cd ccgg-skills-factory
python skills-factory/scripts/package_skill.py skills-factory --install personal

# Verify
ls ~/.claude/skills/skills-factory/SKILL.md

# Start using - Open Claude Code and say:
# "Create a new skill for [your use case]"
```

**Prefer Git?** Clone instead: `git clone https://github.com/DaronVee/ccgg-skills-factory.git` then run install command

---

## Platform Compatibility

| Platform | Installation | Script Execution | Requirements |
|----------|-------------|------------------|--------------|
| **Claude Code (CLI)** | Download ZIP + install | ✅ Local environment | Python 3.x installed |
| **Claude Desktop** | Download ZIP + upload | ✅ Server-side sandbox | "Code execution" enabled in Settings > Capabilities |
| **Claude.ai (Web)** | Download ZIP + upload | ✅ Server-side sandbox | "Code execution" enabled in Settings > Capabilities |

**All platforms support full functionality!** Scripts execute in secure sandboxes (Desktop/Web) or your local environment (Claude Code).

---

## What's Included

### Core Skill
- **SKILL.md** (~19 KB): Main skill file with intelligent frontmatter configuration, progressive disclosure, evaluation-driven development framework, and comprehensive guidance

### Automation Scripts (4 Python files)
- **comprehensive_validate.py** (~700 lines): Deep validation with 15+ checks (YAML structure, new frontmatter fields, invocation control, code patterns, progressive disclosure, etc.)
- **init_skill.py** (~390 lines): Skill generator with template creation, commented optional fields, and structure scaffolding
- **package_skill.py** (235 lines): Packager/installer for personal, project, and distribution deployment
- **quick_validate.py** (65 lines): Fast validation for iterative development

### Reference Guides (8 comprehensive docs)
- **FRONTMATTER_DECISION_GUIDE.md**: 6-question intelligent configuration wizard for YAML frontmatter fields
- **SUBAGENT_PATTERNS.md**: Bidirectional skill/subagent integration patterns (context: fork + skills field)
- **DEPLOYMENT_GUIDE.md** (6,000+ words): Complete deployment workflows including nested discovery, --add-dir, and plugin namespacing
- **EVALUATION_GUIDE.md**: Evaluation-driven development methodology with fork evaluation scenarios
- **TROUBLESHOOTING.md**: 15 common issues with detailed solutions
- **TWO_CLAUDE_METHODOLOGY.md**: Iterative testing framework using two Claude instances
- **VALIDATION_PATTERNS.md**: Feedback loop patterns and quality gates
- **WORKFLOW_PATTERNS.md**: Design patterns for skill creation (simple, standard, complex, forked context)

---

## System Requirements

### Required
- **Python 3.x** (no external packages needed - pure standard library)
- **Claude Code v1.0+** (for CLI usage) OR Claude Desktop/Web with Pro/Max/Team/Enterprise plan
- **Code execution enabled**: Settings > Capabilities > "Code execution and file creation" (Desktop/Web only)

### Optional
- **Git** (for team sharing and version control)
- **Text editor** (for manual skill editing)

---

## Installation Options

### Option 1: Claude Code CLI (Recommended for Power Users)

**Download**: Get the latest [Release ZIP](https://github.com/DaronVee/ccgg-skills-factory/releases) or clone with Git

**Personal Installation** (skill available across all projects):
```bash
# Extract ZIP or clone, then:
cd ccgg-skills-factory
python skills-factory/scripts/package_skill.py skills-factory --install personal
```

**Project Installation** (skill shared with team via Git):
```bash
cd /path/to/your-project
python /path/to/ccgg-skills-factory/skills-factory/scripts/package_skill.py skills-factory --install project

# Commit to share with team
git add .claude/skills/skills-factory/
git commit -m "Add Skills Factory for team skill creation"
git push
```

### Option 2: Claude Desktop / Web (Easiest for Beginners)

**The ZIP in releases is already packaged!** Just download and upload directly:

1. Download `skills-factory.zip` from [Releases](https://github.com/DaronVee/ccgg-skills-factory/releases)
2. Upload to Claude:
   - **Desktop**: Settings > Features > Skills > Upload Skill
   - **Web**: Settings (gear icon) > Features > Skills > Upload Skill
3. Enable code execution:
   - Settings > Capabilities > Toggle ON "Code execution and file creation"
4. Verify:
   - Start new conversation
   - Ask: "What skills are available?"
   - Should see "skills-factory" in response

---

## Documentation

### For Beginners
- [Installation Guide](docs/INSTALLATION_GUIDE.md) - Step-by-step with screenshots and troubleshooting
- [FAQ](docs/FAQ.md) - Common questions and answers
- [Platform Compatibility](docs/PLATFORM_COMPATIBILITY.md) - Detailed platform comparison

### For Advanced Users
- [Frontmatter Decision Guide](skills-factory/references/FRONTMATTER_DECISION_GUIDE.md) - Intelligent YAML configuration wizard
- [Subagent Patterns](skills-factory/references/SUBAGENT_PATTERNS.md) - Skill/subagent integration patterns
- [Deployment Guide](skills-factory/references/DEPLOYMENT_GUIDE.md) - Complete deployment workflows
- [Evaluation Guide](skills-factory/references/EVALUATION_GUIDE.md) - Evaluation-driven development
- [Troubleshooting](skills-factory/references/TROUBLESHOOTING.md) - 15 common issues + solutions

---

## Features

### Progressive Disclosure
Skills reveal information gradually based on context:
- **Tier 1**: Core instructions (always visible)
- **Tier 2**: Detailed guidance (shown when relevant)
- **Tier 3**: Advanced patterns (shown for complex scenarios)

### Evaluation-Driven Development
Build skills iteratively with continuous validation:
1. Define success criteria upfront
2. Build minimal viable skill
3. Test with real scenarios
4. Refine based on feedback
5. Validate comprehensively

### Comprehensive Validation
Four validation levels ensure quality:
- **Quick Validate**: Fast syntax + structure checks
- **Comprehensive Validate**: Deep analysis (15+ checks including new frontmatter fields)
- **Two-Claude Testing**: Real-world usage testing
- **Production Readiness**: Final quality gates

### Intelligent Frontmatter Configuration
6-question decision guide that determines the right YAML configuration:
- **Invocation Control**: Who triggers the skill (user, Claude, or both)?
- **Execution Context**: Main conversation or isolated subagent (context: fork)?
- **Arguments**: Does the skill accept parameters ($ARGUMENTS, $0, $1)?
- **Tool Access**: Should tools be restricted (allowed-tools)?
- **Dynamic Data**: Does the skill need live shell data (!`command`)?
- **Hooks**: Pre/post execution validation needed?

### Subagent Integration
Two patterns for skill/subagent interaction:
- **Pattern A**: Skill spawns subagent (`context: fork`) - for context protection, parallel execution, tool restriction
- **Pattern B**: Subagent uses skills (`skills` field) - for domain-specific agents with preloaded knowledge

### Design Patterns
Pre-built architectures for common use cases:
- **Simple Skills**: Single-purpose, minimal complexity
- **Standard Skills**: Multi-section, moderate complexity
- **Complex Skills**: Advanced patterns with subagents, hooks, multi-file support
- **Forked Context**: Isolated execution for heavy research or parallel tasks

---

## Usage Examples

### Create Your First Skill

```
You: "Create a new skill for generating meeting notes from transcripts"

Claude (with Skills Factory):
1. Analyzes your use case
2. Suggests skill architecture (simple/standard/complex)
3. Generates SKILL.md with appropriate sections
4. Creates validation checklist
5. Guides you through testing

Result: Production-ready skill in 15-30 minutes
```

### Validate Existing Skill

```bash
# Quick validation (fast feedback)
python skills-factory/scripts/quick_validate.py /path/to/your-skill

# Comprehensive validation (production readiness)
python skills-factory/scripts/comprehensive_validate.py /path/to/your-skill
```

### Package for Distribution

```bash
# Create ZIP for sharing
python skills-factory/scripts/package_skill.py your-skill --package

# Install to personal skills
python skills-factory/scripts/package_skill.py your-skill --install personal

# Install to project (team sharing)
python skills-factory/scripts/package_skill.py your-skill --install project
```

---

## Contributing

This is a CCGG community resource. Contributions welcome!

### Ways to Contribute
- **Bug Reports**: Open an [Issue](https://github.com/DaronVee/ccgg-skills-factory/issues)
- **Documentation**: Improve guides, add examples
- **Feature Requests**: Suggest enhancements
- **Skill Examples**: Share skills you've created

### Support
- **GitHub Issues**: Technical questions, bugs, feature requests
- **CCGG Community**: https://www.skool.com/ccgg - General questions, best practices, showcases

---

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current**: v2.0.0 - Full Feature Alignment (2026-02-09)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Acknowledgments

**Created by**: Daron Vener - [CCGG Community](https://www.skool.com/ccgg)
**Built with**: Claude Code - Anthropic's CLI for autonomous coding
**Methodology**: Evaluation-driven development + Progressive disclosure patterns

---

**Ready to create your first skill?** Download the [latest release](https://github.com/DaronVee/ccgg-skills-factory/releases) and follow the Quick Start above!
