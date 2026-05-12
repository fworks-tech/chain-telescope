#!/usr/bin/env python3
"""
Pull Request Skill - Validate diffs and create PRs with proper formatting.

This skill automates the creation of pull requests by:
1. Validating the current branch diff against main
2. Describing changed files (grouping if there are many)
3. Generating conventional commit formatted title
4. Creating a PR with the proper template
5. Following conventional commits standards

Usage:
    python scripts/pr-skill.py create [--title "title"] [--description "desc"]
    python scripts/pr-skill.py validate
    python scripts/pr-skill.py summary

Conventional Commits Format:
    <type>[optional scope]: <description>
    
    Types: feat, fix, docs, chore, refactor, test, perf, style, ci
    Example: feat(auth): add JWT token validation
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from enum import Enum


class CommitType(Enum):
    """Conventional commit types."""
    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    CHORE = "chore"
    REFACTOR = "refactor"
    TEST = "test"
    PERF = "perf"
    STYLE = "style"
    CI = "ci"


class FileChangeAnalyzer:
    """Analyze and group changed files from git diff."""
    
    # Mapping of file patterns to scope/category
    SCOPE_MAPPING = {
        "data/": "data",
        "notebooks/": "ui",
        "docs/": "docs",
        ".github/": "ci",
        "scripts/": "automation",
        "requirements.txt": "automation",
        "README.md": "docs",
    }
    
    MAX_FILES_DISPLAY = 10
    
    @classmethod
    def get_changed_files(cls) -> Tuple[List[str], int]:
        """Get list of changed files between current branch and main."""
        try:
            # Get current branch
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True
            ).strip()
            
            # Get list of changed files
            result = subprocess.check_output(
                ["git", "diff", "--name-only", f"main...{branch}"],
                text=True
            ).strip()
            
            files = result.split("\n") if result else []
            return files, len(files)
        except subprocess.CalledProcessError as e:
            print(f"Error getting changed files: {e}", file=sys.stderr)
            return [], 0
    
    @classmethod
    def categorize_files(cls, files: List[str]) -> Dict[str, List[str]]:
        """Group files by scope/category."""
        categories = {}
        
        for file in files:
            category = "other"
            for pattern, scope in cls.SCOPE_MAPPING.items():
                if file.startswith(pattern):
                    category = scope
                    break
            
            if category not in categories:
                categories[category] = []
            categories[category].append(file)
        
        return categories
    
    @classmethod
    def format_file_summary(cls, files: List[str]) -> str:
        """Format changed files for PR description."""
        if not files:
            return "No files changed"
        
        if len(files) <= cls.MAX_FILES_DISPLAY:
            # List all files
            file_list = "\n".join(f"- `{f}`" for f in sorted(files))
            return f"**Changed files:**\n{file_list}"
        else:
            # Group by scope
            categories = cls.categorize_files(files)
            summary = "**Changed files (grouped by scope):**\n"
            
            for category in sorted(categories.keys()):
                files_in_cat = categories[category]
                summary += f"\n**{category.title()}** ({len(files_in_cat)} files)\n"
                
                # Show first few, then ellipsis if too many
                shown = files_in_cat[:3]
                summary += "\n".join(f"- `{f}`" for f in sorted(shown))
                
                if len(files_in_cat) > 3:
                    summary += f"\n- ... and {len(files_in_cat) - 3} more"
                
                summary += "\n"
            
            return summary
    
    @classmethod
    def get_diff_stats(cls) -> Dict[str, int]:
        """Get diff statistics (additions, deletions, files changed)."""
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True
            ).strip()
            
            result = subprocess.check_output(
                ["git", "diff", "--stat", f"main...{branch}"],
                text=True
            ).strip()
            
            # Parse output
            lines = result.split("\n")
            total_line = lines[-1] if lines else ""
            
            stats = {"files": 0, "additions": 0, "deletions": 0}
            
            # Parse the summary line
            if "changed" in total_line:
                parts = total_line.split(",")
                for part in parts:
                    try:
                        if "insertion" in part:
                            stats["additions"] = int(part.split()[0])
                        elif "deletion" in part:
                            stats["deletions"] = int(part.split()[0])
                        elif "changed" in part:
                            stats["files"] = int(part.split()[0])
                    except (ValueError, IndexError) as parse_error:
                        print(f"Warning: Could not parse diff stat from '{part}': {parse_error}", file=sys.stderr)
            
            return stats
        except Exception as e:
            print(f"Warning: Could not get diff stats: {e}", file=sys.stderr)
            return {"files": 0, "additions": 0, "deletions": 0}


class PRTemplateGenerator:
    """Generate PR descriptions from template."""
    
    TEMPLATE = """## Summary
{summary}

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
{files_changed}

## Diff Summary
- Files changed: {files_count}
- Additions: +{additions}
- Deletions: -{deletions}

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
- [ ] Ready for review"""
    
    @classmethod
    def generate(
        cls,
        summary: str = "",
        commit_type: CommitType = CommitType.FEAT,
        scope: str = ""
    ) -> Tuple[str, str]:
        """
        Generate PR title and body.
        
        Returns:
            Tuple of (title, body)
        """
        files, file_count = FileChangeAnalyzer.get_changed_files()
        stats = FileChangeAnalyzer.get_diff_stats()
        
        # Generate title in conventional commit format
        scope_str = f"({scope})" if scope else ""
        if not summary:
            summary = "Auto-generated PR from branch diff"
        
        title = f"{commit_type.value}{scope_str}: {summary}"
        
        # Generate body
        body = cls.TEMPLATE.format(
            summary=summary,
            files_changed=FileChangeAnalyzer.format_file_summary(files),
            files_count=stats.get("files", file_count),
            additions=stats.get("additions", 0),
            deletions=stats.get("deletions", 0)
        )
        
        return title, body


def validate_branch_diff() -> bool:
    """Validate the current branch has differences from main."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
        
        if branch == "main":
            print("Error: Already on main branch. Create a feature branch first.", file=sys.stderr)
            return False
        
        # Check if there are differences
        result = subprocess.run(
            ["git", "diff", "--quiet", f"main...{branch}"],
            capture_output=True
        )
        return result.returncode != 0  # Has differences
    except Exception as e:
        print(f"Error validating branch: {e}", file=sys.stderr)
        return False


def create_pull_request(title: str, body: str, draft: bool = False) -> bool:
    """Create pull request using gh CLI."""
    try:
        cmd = ["gh", "pr", "create", "--title", title, "--body", body]
        if draft:
            cmd.append("--draft")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Pull request created!\n{result.stdout}")
            return True
        else:
            print(f"✗ Error creating PR:\n{result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def show_summary() -> None:
    """Show summary of changes."""
    files, file_count = FileChangeAnalyzer.get_changed_files()
    stats = FileChangeAnalyzer.get_diff_stats()
    
    print("\n" + "="*60)
    print("PR SUMMARY")
    print("="*60)
    
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
    except Exception as e:
        branch = "unknown"
    
    print(f"\nBranch: {branch}")
    print(f"Files changed: {file_count}")
    print(f"Additions: +{stats.get('additions', 0)}")
    print(f"Deletions: -{stats.get('deletions', 0)}")
    
    print(f"\nChanged files:\n{FileChangeAnalyzer.format_file_summary(files)}")
    print("\n" + "="*60 + "\n")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Pull Request Skill - Validate diffs and create PRs"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a pull request")
    create_parser.add_argument(
        "--title",
        help="PR title (will auto-generate if not provided)"
    )
    create_parser.add_argument(
        "--description",
        help="PR description summary"
    )
    create_parser.add_argument(
        "--type",
        choices=[t.value for t in CommitType],
        default="feat",
        help="Conventional commit type"
    )
    create_parser.add_argument(
        "--scope",
        help="Conventional commit scope (e.g., auth, api)"
    )
    create_parser.add_argument(
        "--draft",
        action="store_true",
        help="Create as draft PR"
    )
    
    # Validate command
    subparsers.add_parser("validate", help="Validate branch diff against main")
    
    # Summary command
    subparsers.add_parser("summary", help="Show PR summary")
    
    args = parser.parse_args()
    
    if args.command == "create":
        if not validate_branch_diff():
            sys.exit(1)
        
        title, body = PRTemplateGenerator.generate(
            summary=args.description,
            commit_type=CommitType(args.type),
            scope=args.scope
        )
        
        print(f"\nGenerated PR Title: {title}\n")
        print("Generated PR Description:\n" + "-"*60)
        print(body)
        print("-"*60 + "\n")
        
        # Confirm before creating
        response = input("Create this pull request? (y/n): ").strip().lower()
        if response == "y":
            if create_pull_request(title, body, draft=args.draft):
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print("Cancelled.")
            sys.exit(0)
    
    elif args.command == "validate":
        if validate_branch_diff():
            print("✓ Branch has valid differences from main")
            show_summary()
            sys.exit(0)
        else:
            print("✗ Validation failed")
            sys.exit(1)
    
    elif args.command == "summary":
        show_summary()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
