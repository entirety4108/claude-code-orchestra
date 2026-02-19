#!/usr/bin/env python3
"""
PreToolUse hook: Suggest using Gemini or subagent for deep research tasks.

Analyzes web search/fetch operations and suggests delegating
comprehensive research to Gemini CLI (leveraging 1M context + Google Search)
or a subagent to preserve main context.
"""

import json
import sys

# Keywords that suggest deep research would benefit from Gemini or subagent
RESEARCH_INDICATORS = [
    "documentation",
    "best practice",
    "comparison",
    "library",
    "framework",
    "tutorial",
    "guide",
    "example",
    "pattern",
    "architecture",
    "migration",
    "upgrade",
    "breaking change",
    "api reference",
    "specification",
]

# Simple lookups that don't need delegation
SIMPLE_LOOKUP_PATTERNS = [
    "error message",
    "stack trace",
    "version",
    "release notes",
    "changelog",
]


def should_suggest_delegation(query: str, url: str = "") -> tuple[bool, str]:
    """Determine if Gemini or a subagent should be suggested for this research."""
    query_lower = query.lower()
    url_lower = url.lower()
    combined = f"{query_lower} {url_lower}"

    # Skip simple lookups
    for pattern in SIMPLE_LOOKUP_PATTERNS:
        if pattern in combined:
            return False, ""

    # Check for research indicators
    for indicator in RESEARCH_INDICATORS:
        if indicator in combined:
            return True, f"Research involves '{indicator}'"

    # Long queries suggest complex research
    if len(query) > 100:
        return True, "Complex research query detected"

    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Get query/url based on tool type
        query = ""
        url = ""
        if tool_name == "WebSearch":
            query = tool_input.get("query", "")
        elif tool_name == "WebFetch":
            url = tool_input.get("url", "")
            query = tool_input.get("prompt", "")

        should_suggest, reason = should_suggest_delegation(query, url)

        if should_suggest:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        f"[Research Suggestion] {reason}. "
                        "For comprehensive research, consider using Gemini CLI "
                        "(1M context + Google Search): "
                        '`gemini -p "Research: {topic}" 2>/dev/null`, '
                        "or a gemini-explore subagent for large tasks. "
                        "Save results to .claude/docs/research/. "
                        "This preserves main context."
                    )
                }
            }
            print(json.dumps(output))

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
