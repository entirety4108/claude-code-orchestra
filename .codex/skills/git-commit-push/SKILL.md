---
name: git-commit-push
description: "Stage current repository changes, create a clear commit, and push to the correct remote branch with safety checks. Use when the user asks to commit or push current work (for example: \"commit\", \"push\", \"commit current changes\", or \"push current branch\")."
---

# Git Commit Push

## Workflow

1. Confirm repository context.
- Run `git rev-parse --is-inside-work-tree`.
- Run `git status --short --branch`.
- Run `git remote -v`.
- Stop and report if not in a Git repository.

2. Inspect current changes.
- Run `git status --short`.
- Run `git diff --stat`.
- Run `git diff --cached --stat`.
- Identify whether there is anything to commit.

3. Apply safety checks before staging.
- Scan untracked and modified files for obvious secrets (e.g., `.env`, private keys, tokens).
- Stop and ask before committing suspicious secret-like files.
- Keep existing user changes intact; never revert unrelated edits.

4. Stage changes.
- Default to `git add -A` to include current tracked and untracked work.
- If the user asks for partial commit, stage only requested paths.
- If unrelated changes are already staged, include them in the same commit instead of unstaging or splitting.

5. Create commit.
- Build a concise commit message from the actual diff.
- Write the commit message in Japanese, as a single concise line.
- Run `git commit -m "<message>"`.
- If hooks fail or commit is rejected, report the error and stop.

6. Push commit.
- Detect current branch with `git branch --show-current`.
- If upstream exists, run `git push`.
- If upstream is missing, run `git push --set-upstream origin <branch>`.
- Never force push unless explicitly requested.

7. Report outcome.
- Show commit hash from `git rev-parse --short HEAD`.
- Report branch and remote target.
- Summarize staged files and commit subject clearly for the user.

## Constraints

- Use non-interactive Git commands.
- Do not run `git reset --hard`, `git checkout --`, or history-rewriting commands unless explicitly requested.
- Do not use `--amend` unless explicitly requested.
- If no changes exist, report that clearly instead of creating an empty commit.
