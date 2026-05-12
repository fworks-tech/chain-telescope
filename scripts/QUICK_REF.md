# PR Skill - Quick Reference

## One-Liner Examples

```bash
# Check what changed
python scripts/pr-skill.py summary

# Validate before creating PR
python scripts/pr-skill.py validate

# Create a feature PR
python scripts/pr-skill.py create --description "Add JWT validation" --type feat --scope auth

# Create a bug fix PR
python scripts/pr-skill.py create --description "Fix data parsing" --type fix --scope data

# Create a documentation PR
python scripts/pr-skill.py create --description "Update API docs" --type docs

# Create a draft PR (work in progress)
python scripts/pr-skill.py create --description "WIP: Dashboard redesign" --type feat --scope ui --draft

# Custom title (rarely needed)
python scripts/pr-skill.py create --title "My Custom Title"
```

## Conventional Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | Add authentication |
| `fix` | Bug fix | Fix memory leak |
| `docs` | Documentation | Update README |
| `chore` | Maintenance | Update dependencies |
| `refactor` | Code restructuring | Simplify data handling |
| `test` | Test changes | Add unit tests |
| `perf` | Performance | Optimize queries |
| `style` | Formatting | Fix linting issues |
| `ci` | CI/CD changes | Update GitHub Actions |

## Common Scopes

| Scope | Files | Purpose |
|-------|-------|---------|
| `auth` | auth-related | Authentication/authorization |
| `api` | endpoints | API changes |
| `data` | data processing | Data pipeline |
| `ui` | notebooks | User interface |
| `analytics` | analytics code | Analytics tracking |
| `docs` | documentation | Documentation updates |
| `ci` | workflow files | CI/CD pipeline |
| `deps` | requirements.txt | Dependency changes |

## Before & After

### Before PR Creation
```bash
git checkout -b feat/my-feature
# ...make changes...
git add .
git commit -m "working changes"
git push origin feat/my-feature
```

### Create the PR
```bash
python scripts/pr-skill.py validate
# Review output
python scripts/pr-skill.py create \
  --description "My feature description" \
  --type feat \
  --scope feature
# Approve prompt
```

### After PR Creation
- Review on GitHub
- Ensure CI passes
- Request reviewers
- Merge when approved

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Already on main" | `git checkout -b feature/name` first |
| "No changes" | `git add .` and `git commit` changes |
| "gh not found" | Install: `brew install gh` (macOS) or `apt install gh` (Linux) |
| "Not authenticated" | Run: `gh auth login` |
| "Can't find files" | Ensure git branch is pushed: `git push origin branch-name` |

## File Changes Display

**Small change (≤10 files):** Shows all files
```
- file1.py
- file2.py
- file3.py
```

**Large change (>10 files):** Groups by scope
```
**data** (5 files)
- data/file1.csv
- ... and 4 more

**ui** (8 files)
- notebooks/notebook1.ipynb
- ... and 7 more
```

## PR Template Sections

Your PR will include:
1. **Summary** - What changed and why
2. **Type of Change** - Check the relevant box
3. **Scope** - Check affected areas
4. **Files Changed** - Auto-populated
5. **Diff Summary** - Lines added/removed
6. **Validation** - How was it tested
7. **Screenshots** - If UI changes
8. **Risks** - Any side effects
9. **Checklist** - Verification items

## Environment Setup

```bash
# Install prerequisites
pip install -r requirements.txt  # If using Python packages

# Ensure gh CLI is available
gh --version  # Should show version

# Verify git setup
git config user.name  # Should show your name
git config user.email  # Should show your email
```

## Full Help

```bash
python scripts/pr-skill.py --help
python scripts/pr-skill.py create --help
python scripts/pr-skill.py validate --help
python scripts/pr-skill.py summary --help
```

---

**For detailed guide:** See `scripts/PR_SKILL_GUIDE.md`
