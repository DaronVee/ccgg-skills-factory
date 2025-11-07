# Platform Compatibility Guide

Detailed comparison of Skills Factory across Claude Code, Claude Desktop, and Claude.ai.

**Created by**: [Daron Vener](https://github.com/DaronVee) | [CCGG Community](https://www.skool.com/ccgg)

---

## Quick Reference

| Feature | Claude Code (CLI) | Claude Desktop | Claude.ai (Web) |
|---------|-------------------|----------------|-----------------|
| **Script Execution** | ✅ Local | ✅ Server sandbox | ✅ Server sandbox |
| **Installation Method** | Filesystem | ZIP upload | ZIP upload |
| **Persistence** | Always available | Per-user | Per-user |
| **Team Sharing** | Via Git | Manual per-user | Manual per-user |
| **Python Version** | YOUR Python | Python 3.12.3 | Python 3.12.3 |
| **Environment** | YOUR machine | Ubuntu 24.04.2 | Ubuntu 24.04.2 |
| **External Packages** | pip install works | Limited | Limited |
| **File Access** | Full local access | Sandbox only | Sandbox only |
| **Setup Time** | 2 min | 5 min | 5 min |
| **Best For** | Power users, teams | Beginners, Desktop app users | Beginners, multi-device |

---

## Platform Deep Dive

### Claude Code (CLI)

**What it is**: Command-line interface for Claude, integrated with your local development environment

**How Scripts Execute**:
- Run in YOUR local environment
- Use YOUR installed Python version
- Have access to YOUR file system
- Can call YOUR locally installed tools (git, npm, etc.)

**Advantages**:
- ✅ Full control over environment
- ✅ Can install any Python packages (pip install)
- ✅ Persistent across all projects (global skills)
- ✅ Team sharing via Git (project skills)
- ✅ Fastest script execution (no network latency)
- ✅ Integration with local dev tools

**Limitations**:
- ❌ Requires terminal/command line comfort
- ❌ Must install dependencies locally
- ❌ OS-specific (Windows paths vs Unix paths)

**Best For**:
- Developers and technical users
- Teams using Git workflows
- Projects requiring specific Python packages
- Users needing file system access

**Installation**:
```bash
git clone https://github.com/DaronVee/ccgg-skills-factory.git
cd ccgg-skills-factory
python skills-factory/scripts/package_skill.py skills-factory --install personal
```

**Requirements**:
- Claude Code CLI installed
- Python 3.x installed locally
- Git (optional, for cloning repo)

---

### Claude Desktop

**What it is**: Native desktop application for Claude with GUI interface

**How Scripts Execute**:
- Run in server-side sandbox (Anthropic's servers)
- Ubuntu 24.04.2 environment
- Python 3.12.3 pre-installed
- Node.js 18.19.1 pre-installed
- 9GB RAM, 5GB disk space

**Advantages**:
- ✅ Easy GUI installation (no terminal needed)
- ✅ No local Python required
- ✅ Secure sandbox (scripts can't harm your computer)
- ✅ Consistent environment (works same for everyone)
- ✅ Beginner-friendly

**Limitations**:
- ❌ Must enable "Code execution" in Settings > Capabilities
- ❌ Requires Pro/Max/Team/Enterprise plan
- ❌ Each user uploads individually (no team sync)
- ❌ Limited package installation (only standard library by default)
- ❌ No access to your local file system

**Best For**:
- Beginners new to command line
- Users who prefer GUI interfaces
- Individual users (not teams)
- Users who want "install once, works everywhere" simplicity

**Installation**:
1. Package to ZIP: `python skills-factory/scripts/package_skill.py skills-factory --package`
2. Upload via Settings > Features > Skills
3. Enable "Code execution" in Settings > Capabilities

**Requirements**:
- Claude Desktop app installed
- Pro, Max, Team, or Enterprise plan
- Code execution enabled

---

### Claude.ai (Web)

**What it is**: Browser-based Claude interface accessible from any device

**How Scripts Execute**:
- Same server-side sandbox as Desktop
- Ubuntu 24.04.2, Python 3.12.3, Node.js 18.19.1
- 9GB RAM, 5GB disk space
- Identical capabilities to Desktop

**Advantages**:
- ✅ No installation required (just browser)
- ✅ Works on any device (laptop, tablet, etc.)
- ✅ Same easy ZIP upload as Desktop
- ✅ Secure sandbox environment
- ✅ Multi-device access (use on multiple computers)

**Limitations**:
- ❌ Must enable "Code execution" in Settings > Capabilities
- ❌ Requires Pro/Max/Team/Enterprise plan
- ❌ Per-user upload (no team sharing)
- ❌ Limited package installation
- ❌ No local file access

**Best For**:
- Users who work across multiple devices
- Teams without Git workflows
- Users who prefer browser-based tools
- Quick demos and testing

**Installation**:
1. Package to ZIP: `python skills-factory/scripts/package_skill.py skills-factory --package`
2. Go to https://claude.ai > Settings > Features > Skills
3. Upload ZIP
4. Enable "Code execution" in Settings > Capabilities

**Requirements**:
- Claude.ai account (Pro/Max/Team/Enterprise)
- Modern web browser
- Code execution enabled

---

## Script Execution Details

### What "Code Execution" Means

**Desktop/Web**:
- Server-side sandbox on Anthropic's infrastructure
- Secure Ubuntu environment with pre-installed tools
- Scripts run remotely, results sent back to you
- Can't access your local files or network

**Claude Code**:
- Scripts run on YOUR computer in YOUR terminal
- Use YOUR Python installation and environment
- Full access to YOUR file system and tools
- No sandbox restrictions

---

### How Skills Factory Scripts Work

**Scripts Included**:
1. **comprehensive_validate.py**: Deep validation (12+ checks)
2. **init_skill.py**: Skill generator
3. **package_skill.py**: Packager/installer
4. **quick_validate.py**: Fast validation

**On All Platforms**:
- Claude can execute these scripts via Bash tool
- Scripts use only Python standard library (no external dependencies)
- Scripts read/write files in their context (sandbox or local)
- Output returned to Claude for analysis

**Example Workflow**:
```
You: "Validate my skill"

Claude (any platform):
1. Uses Skills Factory skill
2. Calls comprehensive_validate.py via Bash tool
3. Script runs (locally or in sandbox)
4. Results returned to Claude
5. Claude analyzes and reports to you
```

---

## Requirements Comparison

### Python Requirements

| Platform | Python Needed? | Version | Installation |
|----------|---------------|---------|--------------|
| **Claude Code** | YES (local) | 3.8+ | Install from python.org |
| **Desktop** | NO (provided) | 3.12.3 (sandbox) | Built-in |
| **Web** | NO (provided) | 3.12.3 (sandbox) | Built-in |

**Key Insight**: Desktop/Web users don't need Python installed locally!

---

### Account Requirements

| Platform | Plan Required | Code Execution |
|----------|--------------|----------------|
| **Claude Code** | Any (Free/Pro/Max/Team/Enterprise) | N/A (local execution) |
| **Desktop** | Pro/Max/Team/Enterprise | Must enable in Settings |
| **Web** | Pro/Max/Team/Enterprise | Must enable in Settings |

**Important**: Free plan users can use Claude Code, but not Desktop/Web skills

---

### Storage & Limits

| Platform | Skill Storage | Script Resources |
|----------|--------------|------------------|
| **Claude Code** | `~/.claude/skills/` (unlimited) | YOUR machine resources |
| **Desktop** | Cloud storage | 9GB RAM, 5GB disk |
| **Web** | Cloud storage | 9GB RAM, 5GB disk |

---

## Feature Comparison

### Team Sharing

**Claude Code**:
```bash
# Install skill to project (shared via Git)
python /path/to/package_skill.py skills-factory --install project

# Commit
git add .claude/skills/skills-factory/
git commit -m "Add Skills Factory"
git push

# Team members get it automatically
git pull
```

**Desktop/Web**:
- Each team member uploads ZIP individually
- No automatic sync
- Version management manual

**Recommendation**: Teams should use Claude Code for collaborative skill development

---

### Skill Persistence

**Claude Code**:
- Global skills: Available in ALL projects forever
- Project skills: Available in specific project, shared via Git

**Desktop/Web**:
- Per-user: Each user uploads once, available until removed
- No cross-device sync: Upload on each device separately

---

### Environment Customization

**Claude Code**:
```bash
# Install any Python package
pip install pandas numpy matplotlib

# Skills can use them
import pandas as pd
```

**Desktop/Web**:
- Standard library only (by default)
- Some packages available on-demand (pandas, matplotlib, etc.)
- Can't install arbitrary packages

**Use Case**: If your skill needs specific packages, Claude Code is better

---

## Migration Between Platforms

### From Desktop/Web to Claude Code

**Why migrate?**
- Need local file system access
- Want team sharing via Git
- Require specific Python packages

**How**:
1. Download skill source from GitHub
2. Install to Claude Code: `python package_skill.py skills-factory --install personal`
3. Done - skill now runs locally

---

### From Claude Code to Desktop/Web

**Why migrate?**
- Want GUI interface
- Don't want to manage local environment
- Need multi-device access

**How**:
1. Package skill: `python skills-factory/scripts/package_skill.py skills-factory --package`
2. Upload ZIP via Settings > Features > Skills
3. Enable code execution
4. Done - skill now runs in sandbox

---

## Choosing the Right Platform

### Choose Claude Code if you...
- Are comfortable with terminal/command line
- Work in a team using Git
- Need specific Python packages
- Want full control over environment
- Develop skills frequently

### Choose Claude Desktop if you...
- Prefer GUI over command line
- Want easy installation
- Work individually (not team)
- Don't need custom packages
- Use one primary computer

### Choose Claude.ai (Web) if you...
- Work across multiple devices
- Want zero installation
- Prefer browser-based tools
- Share devices with others
- Need quick demos/testing

---

## Common Questions

### Q: Can I use Skills Factory on multiple platforms?

**A**: Yes! Install on Claude Code for development, upload to Desktop/Web for convenience. Skills work identically across platforms (with environment differences noted above).

---

### Q: Do I need Python installed for Desktop/Web?

**A**: No! Python is provided in the server-side sandbox. You only need Python locally for:
1. Packaging the skill to ZIP (one-time)
2. Using Claude Code (ongoing)

**Workaround**: Download pre-packaged ZIP from GitHub releases (skip packaging step).

---

### Q: Why do Desktop/Web require paid plans?

**A**: Skills require "Code execution and file creation" feature, which is only available on Pro/Max/Team/Enterprise plans. This is an Anthropic limitation, not Skills Factory.

---

### Q: Can scripts access my files in Desktop/Web?

**A**: No. Desktop/Web scripts run in isolated server-side sandbox with no access to your local file system. Only Claude Code scripts run locally and can access your files.

---

### Q: Do skills sync between Desktop and Web?

**A**: No. You must upload the skill separately to Desktop and Web. They don't sync automatically.

---

### Q: Can I develop skills on Web, then move to Claude Code?

**A**: Yes! Develop/test on Web (easy GUI), then install to Claude Code (filesystem copy) for production use or team sharing.

---

## Troubleshooting by Platform

### Claude Code Issues

**"Skill not found"**:
- Check: `ls ~/.claude/skills/skills-factory/SKILL.md`
- Reinstall: `python package_skill.py skills-factory --install personal`
- Restart Claude Code

**"Python not found"**:
- Install Python from python.org
- Ensure `python3` or `python` command works in terminal

---

### Desktop/Web Issues

**"Code execution disabled"**:
- Settings > Capabilities > Toggle ON "Code execution and file creation"
- Requires Pro+ plan

**"Skill upload failed"**:
- Verify ZIP file is valid (created by package_skill.py)
- Check file size < 10MB
- Try re-uploading

**"Scripts not executing"**:
- Verify code execution enabled
- Start new conversation (skills load at conversation start)
- Check plan tier (Free plans can't execute code)

---

## Technical Specifications

### Server-Side Sandbox (Desktop/Web)

**Operating System**: Ubuntu 24.04.2 LTS
**Python**: 3.12.3
**Node.js**: 18.19.1
**RAM**: 9GB
**Disk Space**: 5GB
**Network**: Outbound HTTPS allowed
**File System**: Ephemeral (resets between conversations)

**Pre-installed Packages**:
- Python standard library (all modules)
- pip (package manager)
- Common packages available on-demand: pandas, numpy, matplotlib, requests, beautifulsoup4, etc.

---

### Local Environment (Claude Code)

**Everything depends on YOUR setup**:
- YOUR operating system
- YOUR Python version
- YOUR installed packages
- YOUR file system
- YOUR network access

**Advantage**: Complete flexibility
**Disadvantage**: Dependency management required

---

## Summary

**All platforms support Skills Factory fully!** Choose based on:
- **Ease of use**: Desktop/Web (GUI)
- **Team collaboration**: Claude Code (Git)
- **Flexibility**: Claude Code (custom packages)
- **Multi-device**: Web (browser-based)

No wrong choice - pick what fits your workflow.

---

**Questions?** Ask in [CCGG Community](https://www.skool.com/ccgg) or open an [issue](https://github.com/DaronVee/ccgg-skills-factory/issues)

**Created by**: Daron Vener | CCGG Community
