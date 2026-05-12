# Pull Request Skill Guide

## Overview

The PR Skill automates the creation of well-formatted pull requests that follow:
- **Conventional Commits** standards (https://www.conventionalcommits.org/)
- Your repository's **PR template** (`.github/pull_request_template.md`)
- **Best practices** for change description and scope categorization

## Installation

The skill is included in the repository. Ensure you have:
- Python 3.7+
- `git` command-line tool
- `gh` (GitHub CLI) for PR creation: https://cli.github.com/

```bash
# Install GitHub CLI if needed
brew install gh  # macOS
apt install gh   # Linux
winget install github.cli  # Windows
```

## Quick Start

### 1. Validate Your Branch

Check that your current branch has valid changes:

```bash
python scripts/pr-skill.py validate
```

Output shows:
- Branch name
- Number of files changed
- Additions/deletions count
- File list grouped by scope

### 2. Preview PR

See the generated PR title and description:

```bash
python scripts/pr-skill.py summary
```

### 3. Create PR

Create a pull request with auto-generated title and description:

```bash
python scripts/pr-skill.py create \
  --description "Add JWT token validation" \
  --type feat \
  --scope auth
```

You'll be prompted to review the PR before creation. Confirm with `y` to proceed.

## Command Reference

### create - Create a pull request

```bash
python scripts/pr-skill.py create [OPTIONS]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--title` | string | auto-generated | Override the PR title |
| `--description` | string | "Auto-generated PR" | Summary of changes |
| `--type` | choice | feat | Conventional commit type |
| `--scope` | string | (none) | Scope of changes |
| `--draft` | flag | false | Create as draft PR |

**Conventional Commit Types:**
- `feat` - A new feature
- `fix` - A bug fix
- `docs` - Documentation changes
- `chore` - Build, dependency, or tooling changes
- `refactor` - Code refactoring (no feature/fix)
- `test` - Test additions or updates
- `perf` - Performance improvements
- `style` - Code style changes (formatting, etc)
- `ci` - CI/CD configuration changes

**Examples:**

```bash
# Feature with scope
python scripts/pr-skill.py create \
  --description "Add user authentication" \
  --type feat \
  --scope auth

# Bug fix
python scripts/pr-skill.py create \
  --description "Fix memory leak in data pipeline" \
  --type fix \
  --scope data

# Documentation
python scripts/pr-skill.py create \
  --description "Add API endpoint documentation" \
  --type docs

# Dependency update
python scripts/pr-skill.py create \
  --description "Update pandas to 2.0" \
  --type chore \
  --scope automation

# Draft PR (for work-in-progress)
python scripts/pr-skill.py create \
  --description "WIP: New dashboard component" \
  --type feat \
  --scope ui \
  --draft
```

### validate - Validate branch changes

```bash
python scripts/pr-skill.py validate
```

Verifies:
- Current branch is not main
- There are changes compared to main
- Changes can be described

### summary - Show change summary

```bash
python scripts/pr-skill.py summary
```

Displays:
- Current branch name
- File count
- Added/deleted lines
- File list (grouped if >10 files)

## PR Template

Your PR will be populated with this template:

```markdown
## Summary
[Your change description]

## Type of Change
- [ ] feat
- [ ] fix
- [ ] docs
- [ ] chore
- [ ] refactor
- [ ] test

## Scope
Main areas touched:
- [ ] data
- [ ] ui
- [ ] docs
- [ ] ci
- [ ] automation

## Files Changed
[Auto-populated with changed files]

## Diff Summary
- Files changed: X
- Additions: +Y
- Deletions: -Z

## Validation
How was this tested?
- [ ] local run
- [ ] CI checks
- [ ] manual QA

## Screenshots (if UI)
Before / after screenshots or short notes.

## Risks
Any behavior changes, migrations, or known limitations.

## Checklist
- [ ] Conventional commit messages used
- [ ] README/docs updated (if needed)
- [ ] No secrets added
- [ ] Ready for review
```

## File Grouping

When changes affect 10+ files, the skill groups them by scope:

| Scope | Pattern | Description |
|-------|---------|-------------|
| data | `data/` | Data files and datasets |
| ui | `notebooks/` | UI/notebooks |
| docs | `docs/`, `README.md` | Documentation |
| ci | `.github/` | CI/CD configuration |
| automation | `requirements.txt`, `scripts/` | Automation scripts and dependencies |
| other | anything else | Uncategorized |

Example with many files:

```
**Changed files (grouped by scope):**

**Ci** (3 files)
- `.github/workflows/test.yml`
- `.github/workflows/deploy.yml`
- ... and 1 more

**Data** (5 files)
- `data/processed.csv`
- ... and 4 more
```

## Conventional Commits

Your PR title follows this format:

```
<type>[optional scope]: <description>
```

**Examples:**
```
feat: Add user authentication
feat(auth): Add JWT token validation
fix(data): Correct CSV parsing bug
docs: Update API documentation
chore(deps): Update pandas dependency
```

**Benefits:**
- Semantic versioning via commit history
- Clear change categorization
- Easier changelog generation
- Better project history

## Before Creating a PR

1. **Commit your changes** with meaningful messages
2. **Run tests** locally:
   ```bash
   pytest
   # or your test command
   ```
3. **Update documentation** if needed
4. **Check for secrets**: No API keys, passwords, or credentials
5. **Validate format**:
   ```bash
   python scripts/pr-skill.py validate
   ```

## After Creating a PR

1. **Review the generated description** - Edit as needed on GitHub
2. **Check CI status** - Ensure all checks pass
3. **Request reviewers** - Tag relevant team members
4. **Address feedback** - Push new commits to the same branch
5. **Merge when ready** - GitHub will handle the merge

## Troubleshooting

### "Error: Already on main branch"

```bash
# Create and switch to a feature branch first
git checkout -b feature/my-feature
# Make your changes
git add .
git commit -m "description"
```

### "Error creating PR"

Ensure:
- `gh` CLI is installed: `gh --version`
- You're authenticated: `gh auth login`
- Your branch is pushed: `git push origin branch-name`

### "git diff" returns no changes

- Check current branch: `git branch`
- Compare with main: `git diff main...current-branch`
- Ensure changes are committed (not staged)

## Examples

### Example 1: Feature with multiple files

```bash
# Create feature branch
git checkout -b feat/dashboard-redesign

# Make changes across multiple files
# ...commits...

# Create PR
python scripts/pr-skill.py create \
  --description "Redesign dashboard with new layout and charts" \
  --type feat \
  --scope ui
```

**Generated Title:** `feat(ui): Redesign dashboard with new layout and charts`

**Files Changed (grouped):**
```
**UI** (8 files)
- `notebooks/dashboard.ipynb`
- `docs/dashboard-guide.md`
- ... and 6 more

**Docs** (2 files)
- `README.md`
- ... and 1 more
```

### Example 2: Bug fix

```bash
python scripts/pr-skill.py create \
  --description "Fix off-by-one error in data processing" \
  --type fix \
  --scope data
```

### Example 3: Work in progress

```bash
python scripts/pr-skill.py create \
  --description "WIP: Refactor authentication system" \
  --type refactor \
  --scope auth \
  --draft
```

Creates a **draft PR** that's not ready for review yet. Mark as ready when done.

## Integration with CI/CD

The PR skill works with your repository's CI:

```bash
# GitHub Actions will run on PR creation
# Check status: https://github.com/your-repo/pulls
# All specified checks must pass before merging
```

## References

- **Conventional Commits:** https://www.conventionalcommits.org/
- **GitHub CLI:** https://cli.github.com/docs/
- **Git Branching:** https://git-scm.com/book/en/v2/Git-Branching-Branch-Management

---

**Need help?** Check the script documentation:
```bash
python scripts/pr-skill.py --help
python scripts/pr-skill.py create --help
```
