Inspect the specified GitHub issue with GitHub CLI and implement it.

Issue selector: `$ARGUMENTS`

Workflow:
1. Validate arguments. If empty, ask for an issue number or issue URL.
2. Run `gh issue view $ARGUMENTS --comments` and extract requirements, acceptance criteria, and discussion context.
3. Investigate related code and tests, then choose the smallest safe implementation plan.
4. Implement the changes following existing architecture, coding rules, and security constraints.
5. Run relevant tests/lint checks and report failures with cause and mitigation.
6. Post implementation details to the GitHub issue (Japanese comment) including:
   - One-paragraph implementation summary
   - Changed files list
   - Test/lint results
   - Remaining tasks and next actions
7. Report results in Japanese with:
   - One-paragraph implementation summary
   - Changed files list
   - Test/lint results
   - Remaining tasks and next actions
   - Whether issue comment posting succeeded

Safety rules:
- Do not run `git push` without explicit user instruction.
- In this workflow, run `gh issue comment` after verification unless the user explicitly asks to skip it.
- If requirements are ambiguous, do not proceed with assumptions; ask the user to clarify first.
