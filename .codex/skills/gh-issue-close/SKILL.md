---
name: gh-issue-close
description: "Post a reproducible implementation comment to a GitHub issue and close it with GitHub CLI. Use when the user asks to report implementation details on an issue and close it (for example: \"close #123 with implementation notes\", \"comment and close this issue URL\")."
---

# GH Issue Close

## Workflow

1. Validate issue selector and close intent.
- Accept issue number, `owner/repo#123`, or full issue URL.
- If selector is missing, ask the user for issue number or URL.
- If user requests comment-only, skip the close step and report that issue remains open.

2. Gather reproducibility evidence.
- Run `gh issue view <selector> --comments` with escalated execution (`sandbox_permissions=require_escalated`) and a concise `justification`.
- Collect implementation facts from local work: changed files, key behavior changes, commit hash, executed commands, and verification results.
- If evidence is missing, stop and ask the user instead of guessing.

3. Build the issue comment with reproducible details.
- Write the comment in Japanese.
- Include these sections in order:
  1. `Implementation Summary`
  2. `Changed Files`
  3. `Reproduction Steps` (exact commands, inputs, and expected outputs)
  4. `Verification Results` (tests/lint/checks actually executed)
  5. `Commit Information` (hash and branch)
  6. `Remaining Items` (if any)
- Use fenced code blocks for command sequences.
- Do not claim commands or tests that were not executed.

4. Post the comment.
- Save the comment to a temporary file.
- Run `gh issue comment <selector> --body-file <temp-file>` with escalated execution and a concise `justification`.
- Remove temporary files after posting.

5. Close the issue.
- Run `gh issue close <selector> --reason completed` with escalated execution and a concise `justification`.
- If close fails due permissions or repository policy, report the failure and keep the issue state unchanged.

6. Verify and report result in Japanese.
- Run `gh issue view <selector> --json number,title,state,url` with escalated execution.
- Report issue number/title/url, whether comment was posted, final state, and any remaining follow-up.

## Safety Rules

- Execute all `gh` commands with escalated execution (`sandbox_permissions=require_escalated`) and include a user-facing `justification`.
- Never close an issue without posting a reproducible implementation comment, unless the user explicitly requests close-only behavior.
- Never include secrets, tokens, private keys, or sensitive environment values in comments.
- Never fabricate implementation facts, command outputs, or test results.
- If unresolved blockers remain, ask the user whether to close anyway before executing `gh issue close`.
