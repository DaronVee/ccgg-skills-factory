# Skills Factory - Installation Guide

Complete installation instructions for all platforms and skill levels.

**Created by**: [Daron Vener](https://github.com/DaronVee) | [CCGG Community](https://www.skool.com/ccgg)

---

## Choose Your Path

- **[Tier 1: Quick Start](#tier-1-quick-start)** - For technical users (3 commands, 2 minutes)
- **[Tier 2: Step-by-Step](#tier-2-step-by-step)** - For intermediate users (guided, 10 minutes)
- **[Tier 3: Beginner Guide](#tier-3-beginner-guide)** - For first-time users (detailed, 20 minutes)

---

## Tier 1: Quick Start

**For**: Technical users comfortable with terminal/command line

### Prerequisites
- Python 3.x installed
- Git installed (or download ZIP from releases)
- Claude Code CLI OR Claude Desktop/Web with Pro+ plan

### Claude Code (CLI)

```bash
# Clone repository
git clone https://github.com/DaronVee/ccgg-skills-factory.git
cd ccgg-skills-factory

# Install to personal skills
python skills-factory/scripts/package_skill.py skills-factory --install personal

# Verify
ls ~/.claude/skills/skills-factory/SKILL.md

# Start using
# Open Claude Code, say: "Create a new skill for X"
```

### Claude Desktop / Web

```bash
# Package to ZIP
cd ccgg-skills-factory/skills-factory
python scripts/package_skill.py skills-factory --package

# Upload skills-factory.zip via Settings > Features > Skills
# Enable "Code execution and file creation" in Settings > Capabilities
# Verify: Ask Claude "What skills are available?"
```

**Done!** Jump to [Verification](#verification) to test your installation.

---

## Tier 2: Step-by-Step

**For**: Intermediate users who want guided instructions with explanations

### Step 1: Check Prerequisites

**Check Python**:
```bash
# Mac/Linux
python3 --version

# Windows
python --version
# OR
py --version
```

Expected output: `Python 3.8.x` or higher

**If Python not found**: Download from [python.org](https://www.python.org/downloads/)

**Check Git** (optional):
```bash
git --version
```

Expected output: `git version 2.x.x`

**If Git not found**: Download from [git-scm.com](https://git-scm.com/downloads) OR skip Git and download ZIP from GitHub

---

### Step 2: Get Skills Factory

**Option A: Clone with Git (Recommended)**

```bash
# Navigate to your projects folder
cd ~/Downloads  # or wherever you keep projects

# Clone repository
git clone https://github.com/DaronVee/ccgg-skills-factory.git

# Navigate into folder
cd ccgg-skills-factory

# Verify contents
ls
# Should see: README.md, skills-factory/, docs/, LICENSE, etc.
```

**Option B: Download ZIP (No Git)**

1. Go to https://github.com/DaronVee/ccgg-skills-factory
2. Click green "Code" button > "Download ZIP"
3. Extract ZIP to your projects folder
4. Open terminal/command prompt in extracted folder

---

### Step 3: Choose Installation Method

#### Method A: Claude Code (CLI) - For Command Line Users

**Why choose this?**
- Skill available across ALL your Claude Code projects
- Scripts run in your local environment (YOUR Python)
- Persistent across sessions

**Installation**:

```bash
# From ccgg-skills-factory folder
python skills-factory/scripts/package_skill.py skills-factory --install personal

# Windows alternative (if python doesn't work)
py skills-factory/scripts/package_skill.py skills-factory --install personal
```

**What this does**:
- Copies `skills-factory/` to `~/.claude/skills/`
- Makes skill available globally
- Claude Code auto-discovers it on startup

**Verify**:
```bash
# Mac/Linux
ls ~/.claude/skills/skills-factory/SKILL.md

# Windows (PowerShell)
ls $HOME/.claude/skills/skills-factory/SKILL.md

# Windows (CMD)
dir %USERPROFILE%\.claude\skills\skills-factory\SKILL.md
```

Expected: File exists, no error

---

#### Method B: Claude Desktop - For Desktop App Users

**Why choose this?**
- Easy upload via GUI (no terminal needed)
- Works with existing Claude Desktop installation
- Scripts run in secure server-side sandbox

**Prerequisites**:
- Claude Desktop app installed
- Pro, Max, Team, or Enterprise plan
- "Code execution and file creation" enabled

**Installation**:

**Step B1: Package to ZIP**

```bash
# Navigate to skills-factory folder
cd ccgg-skills-factory/skills-factory

# Package
python scripts/package_skill.py skills-factory --package

# Windows alternative
py scripts/package_skill.py skills-factory --package
```

Output: `Created skills-factory.zip`

**Step B2: Upload to Claude Desktop**

1. Open Claude Desktop app
2. Click Settings icon (gear) > Features
3. Scroll to "Skills" section
4. Click "Upload Skill" button
5. Select `skills-factory.zip`
6. Wait for upload confirmation

**Step B3: Enable Code Execution**

1. Still in Settings > Capabilities
2. Find "Code execution and file creation"
3. Toggle ON (switch turns blue)
4. Close settings

**Verify**:
- Start new conversation in Claude Desktop
- Ask: "What skills are available?"
- Should see "skills-factory" mentioned in response

---

#### Method C: Claude.ai (Web) - For Web Users

**Why choose this?**
- No installation needed (browser-based)
- Same server-side sandbox as Desktop
- Access from any device

**Prerequisites**:
- Claude.ai account (Pro/Max/Team/Enterprise)
- Browser access to claude.ai

**Installation**:

**Step C1: Package to ZIP** (same as Desktop)

```bash
cd ccgg-skills-factory/skills-factory
python scripts/package_skill.py skills-factory --package
```

**Step C2: Upload to Claude.ai**

1. Go to https://claude.ai
2. Click Settings icon (bottom left)
3. Go to Features tab
4. Scroll to "Skills" section
5. Click "Upload Skill"
6. Select `skills-factory.zip`
7. Confirm upload

**Step C3: Enable Code Execution**

1. In Settings > Capabilities
2. Toggle ON "Code execution and file creation"
3. Close settings

**Verify**:
- Start new conversation
- Ask: "What skills are available?"
- Should see "skills-factory" in response

---

### Step 4: Test Installation

**Simple Test**:
```
You: "What skills are available?"

Expected response: Claude mentions "skills-factory" or similar
```

**Functional Test**:
```
You: "Create a simple skill for formatting meeting notes"

Expected: Claude uses Skills Factory to:
1. Ask clarifying questions
2. Suggest skill architecture
3. Generate SKILL.md
4. Provide validation checklist
```

**Script Test** (Claude Code only):
```bash
# From ccgg-skills-factory folder
python skills-factory/scripts/quick_validate.py skills-factory

# Expected: Validation passes with checkmarks
```

---

## Tier 3: Beginner Guide

**For**: First-time users new to terminal, Python, or Claude Code

### What You'll Need

**Required**:
- A computer (Windows, Mac, or Linux)
- Internet connection
- Claude account (Pro, Max, Team, or Enterprise plan)
- 20 minutes of time

**Don't worry if you don't have**:
- Programming experience (not needed!)
- Terminal/command line knowledge (we'll guide you)
- Git (we'll show alternatives)

---

### Understanding the Basics

**What is Skills Factory?**
- A "skill" is like a plugin that teaches Claude how to do a specific task
- Skills Factory is a skill that helps you CREATE other skills
- Think of it as: "A tool that builds tools"

**What is a terminal/command line?**
- A text-based way to talk to your computer
- On Mac: App called "Terminal"
- On Windows: App called "Command Prompt" or "PowerShell"
- Don't worry - we'll give you exact commands to copy/paste

**What is Python?**
- A programming language (but you don't need to code!)
- We need it to run the installation scripts
- It's like having Microsoft Word to open .docx files

---

### Step-by-Step Installation (Beginner)

#### Step 1: Check if Python is Installed

**Mac**:
1. Open "Terminal" app (find via Spotlight - press Cmd+Space, type "terminal")
2. Type: `python3 --version` and press Enter
3. If you see `Python 3.8.x` or similar: ✅ You have Python!
4. If you see "command not found": Go to [python.org](https://www.python.org/downloads/), click "Download Python", install

**Windows**:
1. Press Windows key, type "PowerShell", press Enter
2. Type: `python --version` and press Enter
3. If you see `Python 3.8.x` or similar: ✅ You have Python!
4. If not: Type `py --version` and press Enter
5. If still nothing: Go to [python.org](https://www.python.org/downloads/), click "Download Python", install (check "Add Python to PATH" during install!)

---

#### Step 2: Download Skills Factory

**Easy Way (No Git)**:

1. Go to https://github.com/DaronVee/ccgg-skills-factory
2. Look for green "Code" button (top right)
3. Click it > "Download ZIP"
4. Save to your Downloads folder
5. Extract ZIP (double-click on Windows, or right-click > Extract on Mac)
6. Remember this location (you'll need it!)

---

#### Step 3: Open Terminal in the Right Place

**Mac**:
1. Open Finder
2. Navigate to where you extracted the ZIP (probably Downloads)
3. Find the `ccgg-skills-factory` folder
4. Right-click folder > "Services" > "New Terminal at Folder"
5. Terminal opens with correct location

**Windows**:
1. Open File Explorer
2. Navigate to where you extracted the ZIP (probably Downloads)
3. Find the `ccgg-skills-factory` folder
4. Click in the address bar at top (where it shows the path)
5. Type: `powershell` and press Enter
6. PowerShell opens in that folder

**Verify you're in the right place**:
- Type: `ls` (Mac) or `dir` (Windows)
- You should see: `README.md`, `skills-factory`, `docs`, etc.
- If not, you're in the wrong folder! Go back to step 3

---

#### Step 4: Choose Your Claude Platform

**Using Claude Code (CLI)?** → Go to [Step 5A](#step-5a-install-for-claude-code)
**Using Claude Desktop app?** → Go to [Step 5B](#step-5b-install-for-claude-desktop)
**Using claude.ai website?** → Go to [Step 5B](#step-5b-install-for-claude-desktop) (same process)

---

#### Step 5A: Install for Claude Code

**Copy and paste this command**:

Mac/Linux:
```bash
python3 skills-factory/scripts/package_skill.py skills-factory --install personal
```

Windows:
```powershell
python skills-factory/scripts/package_skill.py skills-factory --install personal
```

Windows (if python doesn't work):
```powershell
py skills-factory/scripts/package_skill.py skills-factory --install personal
```

**Press Enter**

**What you'll see**:
- Some text scrolling (the script working)
- Final message: "Installed skills-factory to personal skills directory"
- If you see errors: Jump to [Troubleshooting](#troubleshooting)

**You're done!** Jump to [Verification](#verification)

---

#### Step 5B: Install for Claude Desktop / Web

**Part 1: Create the ZIP file**

**Navigate into skills-factory folder**:

Mac:
```bash
cd skills-factory
```

Windows:
```powershell
cd skills-factory
```

**Package the skill**:

Mac:
```bash
python3 scripts/package_skill.py skills-factory --package
```

Windows:
```powershell
python scripts/package_skill.py skills-factory --package
```

Windows (if python doesn't work):
```powershell
py scripts/package_skill.py skills-factory --package
```

**What you'll see**:
- Message: "Created skills-factory.zip"
- This ZIP file is now in your `skills-factory` folder

**Part 2: Upload to Claude**

**For Claude Desktop**:
1. Open Claude Desktop app
2. Click gear icon (Settings) at bottom
3. Click "Features" tab
4. Scroll down to "Skills" section
5. Click "Upload Skill" button
6. Browse to your `skills-factory` folder
7. Select `skills-factory.zip`
8. Click Open
9. Wait for "Upload successful" message

**For Claude.ai (Web)**:
1. Go to https://claude.ai in your browser
2. Click Settings icon (bottom left corner)
3. Click "Features" tab
4. Scroll to "Skills" section
5. Click "Upload Skill"
6. Browse to your `skills-factory` folder
7. Select `skills-factory.zip`
8. Click Open
9. Wait for confirmation

**Part 3: Enable Code Execution** (IMPORTANT!)

1. Still in Settings
2. Click "Capabilities" tab
3. Find "Code execution and file creation"
4. Toggle it ON (switch turns blue/green)
5. Close settings

**You're done!** Jump to [Verification](#verification)

---

## Verification

### Test 1: Check Skill is Loaded

**In Claude (any platform)**:
```
You: "What skills are available?"
```

**Expected response**: Claude mentions "skills-factory" or lists it among available skills

**If not**:
- Claude Code: Restart Claude Code CLI
- Desktop: Restart Claude Desktop app
- Web: Refresh browser page

---

### Test 2: Use Skills Factory

**In Claude**:
```
You: "Create a simple skill that helps me format customer emails"
```

**Expected behavior**:
- Claude asks clarifying questions about your use case
- Suggests a skill architecture (probably "simple skill")
- Generates a SKILL.md file with appropriate sections
- Provides a validation checklist

**If Claude doesn't use Skills Factory**:
- Try being more explicit: "Use the skills-factory skill to create a new skill for formatting customer emails"
- Check that code execution is enabled (Desktop/Web)

---

### Test 3: Validate Scripts Work (Optional)

**Claude Code only** (Desktop/Web don't need this test):

```bash
# From ccgg-skills-factory folder
python3 skills-factory/scripts/quick_validate.py skills-factory
```

**Expected**:
- Green checkmarks for various validation checks
- Final message: "Validation passed"

---

## Troubleshooting

### "Python not found" or "command not found"

**Fix**:
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Windows: During install, CHECK "Add Python to PATH"
3. After install, close and reopen terminal
4. Try again

---

### "Permission denied" (Mac/Linux)

**Fix**:
```bash
# Make scripts executable
chmod +x skills-factory/scripts/*.py

# Try installation again
python3 skills-factory/scripts/package_skill.py skills-factory --install personal
```

---

### "Skill not appearing in Claude"

**Claude Code**:
- Restart Claude Code: `claude --restart` or close/reopen terminal
- Check installation: `ls ~/.claude/skills/skills-factory/SKILL.md` (should exist)

**Claude Desktop/Web**:
- Refresh/restart the app or browser
- Check Settings > Features > Skills (should show "skills-factory")
- Verify "Code execution" is enabled in Settings > Capabilities

---

### "Scripts not executing in Desktop/Web"

**This is normal if**:
- You forgot to enable "Code execution and file creation" in Settings > Capabilities
- You're on a Free plan (need Pro/Max/Team/Enterprise)

**Fix**:
1. Settings > Capabilities
2. Toggle ON "Code execution and file creation"
3. Start new conversation
4. Test again

---

### "Can't find skills-factory.zip"

**Fix**:
- The ZIP is created in the folder where you ran the command
- If you ran `python scripts/package_skill.py...`, ZIP is in current folder
- Use File Explorer (Windows) or Finder (Mac) to search for "skills-factory.zip"
- Look in the `ccgg-skills-factory/skills-factory/` folder

---

### Still Having Issues?

**Get help**:
1. **GitHub Issues**: https://github.com/DaronVee/ccgg-skills-factory/issues
   - Click "New Issue"
   - Describe problem with exact error message
   - Include: Your OS (Windows/Mac), Python version, Claude platform

2. **CCGG Community**: https://www.skool.com/ccgg
   - Post in community discussion
   - Daron and other members can help

---

## Advanced: Project Installation (Team Sharing)

**For teams using Git** to share skills across projects:

```bash
# From your project folder
cd /path/to/your-project

# Install skill to project
python /path/to/ccgg-skills-factory/skills-factory/scripts/package_skill.py skills-factory --install project

# Commit to share with team
git add .claude/skills/skills-factory/
git commit -m "Add Skills Factory skill for team"
git push

# Team members pull and automatically get the skill
git pull
```

---

## Next Steps

Now that Skills Factory is installed:

1. **Create your first skill**: Ask Claude "Create a skill for [your use case]"
2. **Read references**: Check `skills-factory/references/` for detailed guides
3. **Explore examples**: Visit CCGG community for skill showcases
4. **Share your skills**: Package and share your creations with the community

---

**Questions?** Open an [issue](https://github.com/DaronVee/ccgg-skills-factory/issues) or ask in [CCGG community](https://www.skool.com/ccgg)

**Created by**: Daron Vener | CCGG Community
