Inspect the specified GitHub issue with GitHub CLI and implement it.

Issue selector: `$ARGUMENTS`

Workflow:
1. Validate arguments. If empty, ask for an issue number or issue URL.
2. Run `gh issue view $ARGUMENTS --comments` and extract requirements, acceptance criteria, and discussion context.
3. Investigate related code and tests, then choose the smallest safe implementation plan.
4. Implement the changes following existing architecture, coding rules, and security constraints.
5. Run relevant tests/lint checks and report failures with cause and mitigation.
6. Report results in Japanese with:
   - One-paragraph implementation summary
   - Changed files list
   - Test/lint results
   - Remaining tasks and next actions

Safety rules:
- Do not run `git push` or `gh issue comment` without explicit user instruction.
- If requirements are ambiguous, do not proceed with assumptions; ask the user to clarify first.