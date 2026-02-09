# Skills Factory - Frequently Asked Questions

Common questions and answers about Skills Factory installation and usage.

**Created by**: [Daron Vener](https://github.com/DaronVee) | [CCGG Community](https://www.skool.com/ccgg)

---

## Installation Questions

### Do I need to know Python to use Skills Factory?

**No!** You don't need Python programming knowledge. However:
- **Claude Code users**: Need Python installed (the program, not the knowledge)
- **Desktop/Web users**: Don't need Python installed at all (sandbox provides it)

Skills Factory creates skills FOR you - you just describe what you want.

---

### Which platform should I use?

**Quick decision guide**:

Choose **Claude Code** if:
- You're comfortable with terminal/command line
- You work in a team using Git
- You need custom Python packages

Choose **Claude Desktop** if:
- You prefer GUI over command line
- You work individually
- You want easy installation

Choose **Claude.ai (Web)** if:
- You work across multiple devices
- You want zero installation
- You prefer browser-based tools

**All platforms have full functionality!** This is about convenience, not capability.

---

### Can I use Skills Factory for free?

**Partially**:
- **Claude Code**: Yes! Works with free Claude accounts
- **Claude Desktop/Web**: No - requires Pro/Max/Team/Enterprise plan (for code execution feature)

The skill itself is free (MIT license), but some platforms require paid Claude plans.

---

### Why does it say "Enable code execution"?

**Desktop/Web only**: Skills require the "Code execution and file creation" capability to run their scripts.

**How to enable**:
1. Settings > Capabilities
2. Toggle ON "Code execution and file creation"
3. Start new conversation

**Why required?**: Skills Factory scripts (validation, packaging) need to execute Python code. This is a security feature - you control whether Claude can run code.

---

### Do I need Git?

**No!** Git is optional:

**If you have Git**:
- Clone repo: `git clone https://github.com/DaronVee/ccgg-skills-factory.git`
- Easier updates: `git pull`

**If you don't have Git**:
- Download ZIP from GitHub (green "Code" button > "Download ZIP")
- Extract and use normally

Both methods work identically.

---

## Usage Questions

### How do I use Skills Factory after installing?

**Simple approach**:
```
You: "Create a skill for [your use case]"

Example: "Create a skill for formatting meeting notes from transcripts"
```

Claude will:
1. Ask clarifying questions
2. Suggest skill architecture
3. Generate SKILL.md file
4. Provide validation checklist

**No special commands needed** - just describe what you want!

---

### What kind of skills can I create?

**Any Claude Code skill!** Examples:
- Content formatting skills (meeting notes, emails, reports)
- Code generation skills (boilerplate, documentation)
- Analysis skills (data processing, summarization)
- Workflow automation skills (task management, project planning)

**Complexity levels**:
- **Simple**: Single-purpose, minimal sections
- **Standard**: Multi-section, moderate complexity
- **Complex**: Advanced patterns, subagents, multi-file

Skills Factory guides you to the right architecture for your use case.

---

### Can Skills Factory create skills for Desktop/Web?

**Yes!** Skills created by Skills Factory work on ALL platforms:
- Claude Code (CLI)
- Claude Desktop
- Claude.ai (Web)

You create once, deploy everywhere (with packaging adjustments).

---

### How do I validate my skills?

**Two validation levels**:

**Quick Validate** (fast feedback):
```bash
python skills-factory/scripts/quick_validate.py /path/to/your-skill
```

**Comprehensive Validate** (production readiness):
```bash
python skills-factory/scripts/comprehensive_validate.py /path/to/your-skill
```

**Or ask Claude**: "Validate my skill using Skills Factory"

---

### Can I share skills I create with others?

**Absolutely!** Sharing options:

**Option 1**: Package to ZIP
```bash
python skills-factory/scripts/package_skill.py your-skill --package
```
Share the ZIP file (email, Slack, CCGG community, etc.)

**Option 2**: GitHub repository (like Skills Factory itself)
- Create repo, push skill files
- Others clone and install

**Option 3**: CCGG community showcase
- Post in community with description
- Share download link or GitHub URL

---

## Troubleshooting Questions

### "Python not found" error

**Claude Code only** (Desktop/Web don't use local Python)

**Fix**:
1. Install Python from [python.org](https://www.python.org/downloads/)
2. **Windows**: During install, CHECK "Add Python to PATH"
3. After install, close and reopen terminal
4. Verify: `python --version` (or `python3 --version` on Mac/Linux)

---

### "Permission denied" error (Mac/Linux)

**Fix**:
```bash
# Make scripts executable
chmod +x skills-factory/scripts/*.py

# Try again
python3 skills-factory/scripts/package_skill.py skills-factory --install personal
```

---

### Skill doesn't appear in Claude

**Claude Code**:
- Restart Claude Code
- Verify installation: `ls ~/.claude/skills/skills-factory/SKILL.md` (should exist)
- If missing: Reinstall

**Claude Desktop/Web**:
- Refresh/restart app or browser
- Check Settings > Features > Skills (should show "skills-factory")
- If missing: Re-upload ZIP

---

### Scripts not executing in Desktop/Web

**Most common cause**: Code execution not enabled

**Fix**:
1. Settings > Capabilities
2. Toggle ON "Code execution and file creation"
3. Start **new conversation** (skills load at conversation start)

**Other causes**:
- Free plan (need Pro+ for code execution)
- Skill upload incomplete (re-upload ZIP)

---

### "Can't find skills-factory.zip"

**The ZIP is created where you ran the command**:

If you ran:
```bash
cd ccgg-skills-factory/skills-factory
python scripts/package_skill.py skills-factory --package
```

ZIP is in: `ccgg-skills-factory/skills-factory/skills-factory.zip`

**Finding it**:
- File Explorer (Windows) or Finder (Mac)
- Search for "skills-factory.zip"
- Look in the folder where you ran the command

---

### Skill works on Claude Code but not Desktop

**Likely causes**:
1. **Code execution disabled**: Enable in Settings > Capabilities
2. **Free plan**: Upgrade to Pro+ for code execution
3. **ZIP not uploaded**: Re-upload via Settings > Features > Skills
4. **Old conversation**: Start new conversation (skills load fresh)

**Environment differences**:
- Desktop runs in server-side sandbox (Ubuntu 24.04.2, Python 3.12.3)
- Claude Code runs locally (YOUR Python, YOUR environment)
- Some skills may need adjustments if they rely on local file paths

---

## Feature Questions

### What is "progressive disclosure"?

**Skills reveal information gradually** based on context:

**Example**:
- **Tier 1** (always shown): Core task instructions
- **Tier 2** (shown when relevant): Detailed guidance for complex cases
- **Tier 3** (shown when needed): Advanced patterns for edge cases

**Benefit**: Skills don't overwhelm Claude with unnecessary info, improving quality and speed.

---

### What is "evaluation-driven development"?

**Build skills iteratively with continuous validation**:

1. **Define**: Success criteria upfront (what makes this skill "good"?)
2. **Build**: Minimal viable skill (simplest version that works)
3. **Test**: Real-world scenarios (does it actually work?)
4. **Refine**: Based on feedback (fix issues, add features)
5. **Validate**: Comprehensive checks (production readiness)

**Benefit**: Catch problems early, ship quality skills, continuous improvement.

---

### What are the "15+ validation checks"?

**Comprehensive validation checks**:
1. YAML frontmatter structure
2. New frontmatter fields (disable-model-invocation, context, agent, model, etc.)
3. Required sections present
4. Progressive disclosure formatting
5. Code block syntax
6. Cross-references valid
7. Placeholder detection
8. Section completeness
9. Instruction clarity
10. Example formatting
11. Edge case coverage
12. Error handling patterns
13. Documentation completeness
14. Allowed-tools format validation (comma-separated, Bash argument patterns)
15. Context: fork content validation (task instructions present)
16. + more

**Run it**: `python scripts/comprehensive_validate.py your-skill`

---

### Can I customize Skills Factory itself?

**Yes!** MIT License allows modification:

**Ways to customize**:
1. **Edit SKILL.md**: Change skill generation behavior
2. **Modify scripts**: Adjust validation rules, packaging logic
3. **Add templates**: Create your own skill templates
4. **Fork on GitHub**: Make your own version

**Recommendation**: Create Git branch before modifying, easier to pull updates.

---

## Team & Collaboration Questions

### Can my team use Skills Factory together?

**Yes!** Team workflows:

**Claude Code + Git** (recommended):
```bash
# Install to project (not personal)
python package_skill.py skills-factory --install project

# Commit
git add .claude/skills/skills-factory/
git commit -m "Add Skills Factory"
git push

# Team members automatically get it
git pull
```

**Desktop/Web**:
- Each team member uploads ZIP individually
- Share one ZIP file via Slack/email/etc.
- Everyone uploads same version

---

### How do we keep team skills in sync?

**Claude Code + Git**:
- Commit skills to project `.claude/skills/` folder
- Team pulls updates automatically
- Version control via Git

**Desktop/Web**:
- Manual: Re-upload updated ZIP to each user
- Version tracking via filenames: `my-skill-v1.0.zip`, `my-skill-v1.1.zip`

**Recommendation**: Teams should use Claude Code for collaborative skill development.

---

### Can we share skills privately within organization?

**Yes!** Options:

**Option 1**: Private GitHub repo (like this one)
- Team members get access via collaborators
- Pull/clone as needed

**Option 2**: Internal file share
- Upload ZIPs to company Sharepoint/Google Drive
- Team downloads and installs

**Option 3**: Claude API (advanced)
- Upload skills to organization's Claude API workspace
- Org-wide availability

---

## Platform-Specific Questions

### Claude Code: Can I install skills globally vs per-project?

**Yes!** Two installation modes:

**Global (personal)**:
```bash
python package_skill.py skills-factory --install personal
# Installs to: ~/.claude/skills/
# Available in: ALL projects
```

**Project (team)**:
```bash
python package_skill.py skills-factory --install project
# Installs to: .claude/skills/ (current project)
# Available in: This project only (but shareable via Git)
```

**When to use each**:
- **Personal**: Skills you use across all projects (your personal toolkit)
- **Project**: Skills specific to one project or for team sharing

---

### Desktop/Web: Can I use skills offline?

**No**. Desktop/Web skills run in server-side sandbox, requiring internet connection.

**Workaround**: Use Claude Code (runs locally, works offline after initial setup).

---

### Web: Do skills sync across devices?

**No**. Upload separately on each device (laptop, tablet, etc.).

**Workaround**: Keep ZIPs in cloud storage (Dropbox, Google Drive), download and upload per-device.

---

## Advanced Questions

### Can I create skills with external dependencies?

**It depends**:

**Claude Code**: Yes!
```bash
pip install pandas numpy
# Your skill can now import pandas, numpy
```

**Desktop/Web**: Limited
- Standard library: Always available
- Popular packages: Available on-demand (pandas, matplotlib, requests)
- Arbitrary packages: Not guaranteed

**Recommendation**: Design skills for standard library if deploying to Desktop/Web.

---

### Can Skills Factory scripts use external packages?

**No!** Skills Factory intentionally uses **only Python standard library**:
- `sys`, `os`, `re`, `pathlib`, `typing`, `zipfile`, `shutil`, `argparse`

**Why?**: Universal compatibility - works everywhere without pip installs.

---

### How do I update Skills Factory?

**Git method**:
```bash
cd ccgg-skills-factory
git pull
# Reinstall
python skills-factory/scripts/package_skill.py skills-factory --install personal
```

**ZIP method**:
1. Download latest release from GitHub
2. Extract and overwrite old folder
3. Reinstall (Claude Code) or re-upload (Desktop/Web)

**Check version**: Look in SKILL.md frontmatter (`version: 1.1.0`)

---

### Can I contribute to Skills Factory?

**Yes!** Contributions welcome:

**Ways to contribute**:
1. **Bug reports**: Open GitHub issue
2. **Feature requests**: Suggest enhancements
3. **Documentation**: Improve guides, add examples
4. **Code**: Fork, modify, submit pull request
5. **Showcase**: Share skills you've created in CCGG community

**GitHub**: https://github.com/DaronVee/ccgg-skills-factory

---

## Getting Help

### Where can I ask questions?

**Two channels**:

1. **GitHub Issues** (technical):
   - https://github.com/DaronVee/ccgg-skills-factory/issues
   - Best for: Bugs, installation problems, technical questions

2. **CCGG Community** (general):
   - https://www.skool.com/ccgg
   - Best for: Usage questions, best practices, skill showcases

---

### How do I report a bug?

**GitHub Issues** (preferred):
1. Go to: https://github.com/DaronVee/ccgg-skills-factory/issues
2. Click "New Issue"
3. Include:
   - Your platform (Claude Code/Desktop/Web)
   - Your OS (Windows/Mac/Linux)
   - Python version (if Claude Code): `python --version`
   - Exact error message (copy/paste)
   - Steps to reproduce

**Example good bug report**:
```
Title: "Installation fails on Windows with 'Permission denied'"

Platform: Claude Code (CLI)
OS: Windows 11
Python: 3.11.5

Error:
PermissionError: [Errno 13] Permission denied: 'C:\\Users\\...'

Steps to reproduce:
1. Cloned repo
2. Ran: python scripts/package_skill.py skills-factory --install personal
3. Error occurred

Expected: Skill installs successfully
Actual: Permission denied error
```

---

### Can I request new features?

**Absolutely!** Submit via:
- **GitHub Issues**: Feature request label
- **CCGG Community**: Discuss with Daron and members

**Popular requests**:
- More skill templates
- Video tutorials
- Example skills library
- GUI installer

---

## Still Have Questions?

**Ask in**:
- **CCGG Community**: https://www.skool.com/ccgg
- **GitHub Issues**: https://github.com/DaronVee/ccgg-skills-factory/issues

**Or check**:
- [Installation Guide](INSTALLATION_GUIDE.md) - Step-by-step instructions
- [Platform Compatibility](PLATFORM_COMPATIBILITY.md) - Detailed platform comparison
- [Skills Factory References](../skills-factory/references/) - Advanced guides

---

**Created by**: Daron Vener | CCGG Community
