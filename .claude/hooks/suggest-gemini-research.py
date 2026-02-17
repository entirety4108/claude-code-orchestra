#!/usr/bin/env python3
"""
PreToolUse hook: Suggest using subagent for deep research tasks.

Analyzes web search/fetch operations and suggests delegating
comprehensive research to a subagent to preserve main context.

NOTE: Gemini is NOT used for research. External research is done
via WebSearch/WebFetch in subagents.
"""

import json
import sys

# Keywords that suggest deep research would benefit from a subagent
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

# Simple lookups that don't need a subagent
SIMPLE_LOOKUP_PATTERNS = [
    "error message",
    "stack trace",
    "version",
    "release notes",
    "changelog",
]


def should_suggest_subagent(query: str, url: str = "") -> tuple[bool, str]:
    """Determine if a subagent should be suggested for this research."""
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

        should_suggest, reason = should_suggest_subagent(query, url)

        if should_suggest:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        f"[Research Suggestion] {reason}. "
                        "For comprehensive research, consider using a subagent "
                        "(Task tool with subagent_type='general-purpose') "
                        "to gather and organize findings, saving results to "
                        ".claude/docs/research/. This preserves main context."
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
