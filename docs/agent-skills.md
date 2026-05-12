# Agent Skills Playbook

## Goal
Keep this repository reliable, readable, and automatable.

## Skills

### 1. Cleanup Guard
- Detect obsolete demo assets in active folders
- Remove template leftovers that are not part of the Streamlit app

### 2. Validation Runner
- Execute lightweight syntax and smoke checks
- Fail fast on broken entrypoints

### 3. Dependency Maintenance
- Propose periodic package updates
- Validate boot after updates

### 4. Report Automation
- Generate trend summary artifacts
- Standardize report naming and cadence

### 5. Release Gate
- Confirm README clarity
- Confirm CI passing
- Confirm `CHANGELOG.md` is updated for release milestones


### 6. Pull Request Skill
- Validate current branch diff against main branch
- Automatically analyze and describe changed files
- Group files by scope (data, ui, docs, ci, automation, other) if many changes
- Generate conventional commit formatted PR titles
- Populate PR description with structured template
- Enforce template requirements (Summary, Type of Change, Scope, Validation, etc)
- Validate conventional commits standards compliance

**Usage:**
```bash
python scripts/pr-skill.py create --description "..." --type feat --scope auth
python scripts/pr-skill.py validate
python scripts/pr-skill.py summary
```

**Features:**
- Automatic file grouping for large changesets (10+ files)
- Conventional commits format: `<type>[scope]: <description>`
- Diff statistics (files, additions, deletions)
- Pre-creation review and approval step
- Draft PR option for work-in-progress
