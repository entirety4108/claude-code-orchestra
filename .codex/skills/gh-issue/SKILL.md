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
- Run `gh issue view <selector> --comments` with escalated execution (`sandbox_permissions=require_escalated`) and a short justification question.
- Extract requirements, acceptance criteria, discussion context, and unresolved questions.
- If requirements are ambiguous, stop and ask the user before implementation.

3. Choose the smallest safe implementation plan.
- Investigate related code and tests with focused searches.
- Keep changes minimal and aligned with existing architecture and coding rules.

4. Share the implementation plan and wait for user approval.
- Present a concise plan in Japanese (what to change, affected files, verification steps).
- Ask for explicit approval before implementation.
- If the user requests changes, revise the plan and ask again.

5. Implement the change.
- Apply code updates with clear separation of concerns.
- Preserve unrelated local changes; never revert user work without explicit request.

6. Verify changes.
- Run relevant tests and lint checks for modified areas.
- If checks fail, report cause and mitigation options clearly.

7. Post implementation details to the GitHub issue.
- Create a concise Japanese comment with:
  - One-paragraph implementation summary
  - Changed files list
  - Test/lint execution results
  - Remaining tasks and next actions
- Run `gh issue comment <selector> --body-file <temp-file>` with escalated execution and a concise `justification`.
- If comment posting fails, include the failure details in the final report.

8. Report results in Japanese.
- One-paragraph implementation summary.
- Changed files list.
- Test/lint execution results.
- Remaining tasks and next actions.
- Whether issue comment was posted successfully.

## Safety Rules

- Execute all `gh` commands with escalated execution (`sandbox_permissions=require_escalated`) and include a concise user-facing `justification`.
- Do not run `git push` without explicit user instruction.
- Do not implement until the user explicitly approves the plan from Workflow step 4.
- In this workflow, run `gh issue comment` after verification unless the user explicitly asks to skip it.
- Do not proceed on ambiguous requirements; ask the user to clarify first.
