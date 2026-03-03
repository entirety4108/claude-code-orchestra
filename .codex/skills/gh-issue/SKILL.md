---
name: gh-issue
description: "Inspect a GitHub issue with GitHub CLI and implement the requested change with minimal safe scope. Use when the user asks to handle an issue number or issue URL (for example: \"fix #123\", \"implement this issue\", or \"handle https://github.com/openai/skills/issues/45\")."
---

# GH Issue

## Workflow

1. Validate issue selector.
- Accept issue number, `owner/repo#123`, or full issue URL.
- If selector is missing, ask the user for issue number or URL.

2. Read issue context with GitHub CLI.
- Run `gh issue view <selector> --comments`.
- Extract requirements, acceptance criteria, discussion context, and unresolved questions.
- If requirements are ambiguous, stop and ask the user before implementation.

3. Choose the smallest safe implementation plan.
- Investigate related code and tests with focused searches.
- Keep changes minimal and aligned with existing architecture and coding rules.

4. Implement the change.
- Apply code updates with clear separation of concerns.
- Preserve unrelated local changes; never revert user work without explicit request.

5. Verify changes.
- Run relevant tests and lint checks for modified areas.
- If checks fail, report cause and mitigation options clearly.

6. Report results in Japanese.
- One-paragraph implementation summary.
- Changed files list.
- Test/lint execution results.
- Remaining tasks and next actions.

## Safety Rules

- Do not run `git push` without explicit user instruction.
- Do not run `gh issue comment` without explicit user instruction.
- Do not proceed on ambiguous requirements; ask the user to clarify first.
- If `gh` authentication or repository access fails, stop and report the required setup command.
