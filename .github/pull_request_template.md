## Summary
What changed and why?

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

## Instructions
How can a reviewer run and verify this change locally?

```powershell
git fetch origin
git checkout <branch-name>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Add any issue-specific checks, env vars, or compile/test commands here.

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
