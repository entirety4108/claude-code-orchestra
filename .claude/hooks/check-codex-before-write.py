#!/usr/bin/env python
"""
PreToolUse hook: Check if Codex consultation is recommended before Write/Edit.

This hook analyzes the file being modified and suggests Codex consultation
for design decisions, complex implementations, or architectural changes.
"""

import json
import os
import sys
from pathlib import Path

# Input validation constants
MAX_PATH_LENGTH = 4096
MAX_CONTENT_LENGTH = 1_000_000


def validate_input(file_path: str, content: str) -> bool:
    """Validate input for security."""
    if not file_path or len(file_path) > MAX_PATH_LENGTH:
        return False
    if len(content) > MAX_CONTENT_LENGTH:
        return False
    # Check for path traversal
    if ".." in file_path:
        return False
    return True


# Patterns that suggest design/architecture decisions
DESIGN_INDICATORS = [
    # File patterns
    "DESIGN.md",
    "ARCHITECTURE.md",
    "architecture",
    "design",
    "schema",
    "model",
    "interface",
    "abstract",
    "base_",
    "core/",
    "/core/",
    "config",
    "settings",

    # Code patterns in content
    "class ",
    "interface ",
    "abstract class",
    "def __init__",
    "from abc import",
    "Protocol",
    "@dataclass",
    "TypedDict",
]

# Files that are typically simple edits (skip suggestion)
SIMPLE_EDIT_PATTERNS = [
    ".gitignore",
    "README.md",
    "CHANGELOG.md",
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    ".env.example",
]


SOURCE_EXTENSIONS = [".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs", ".java", ".cpp", ".c"]


def should_suggest_codex(file_path: str, content: str | None = None) -> tuple[bool, str]:
    """Determine if Codex should be used for this write/edit."""
    path = Path(file_path)
    filepath_lower = file_path.lower()

    # Skip simple edits
    for pattern in SIMPLE_EDIT_PATTERNS:
        if pattern.lower() in filepath_lower:
            return False, ""

    # Check file path for design indicators
    for indicator in DESIGN_INDICATORS:
        if indicator.lower() in filepath_lower:
            return True, f"File path contains '{indicator}' - delegate to Codex for design decisions"

    is_source = any(file_path.endswith(ext) for ext in SOURCE_EXTENSIONS)

    # Check content if available
    if content:
        # Any source file with meaningful content → delegate to Codex
        if is_source and len(content) > 100:
            return True, f"Source file implementation ({len(content)} chars)"

        # Non-source new file with significant content
        if len(content) > 200:
            return True, "Creating file with significant content"

        # Check for design patterns in content
        for indicator in DESIGN_INDICATORS:
            if indicator in content:
                return True, f"Content contains '{indicator}' - likely architectural code"

    # Source files in src/ directory
    if "/src/" in file_path or file_path.startswith("src/"):
        if is_source:
            return True, "Source file in src/ - delegate implementation to Codex"

    # Any source file write
    if is_source:
        return True, "Source file modification - consider Codex implementation"

    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "") or tool_input.get("new_string", "")

        # Validate input
        if not validate_input(file_path, content):
            sys.exit(0)

        should_suggest, reason = should_suggest_codex(file_path, content)

        if should_suggest:
            # Return additional context to Claude
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": (
                        f"[Codex Implementation Required] {reason}. "
                        "**STOP**: Do NOT write this code yourself. Delegate to Codex instead: "
                        "`codex exec --model gpt-5.3-codex --sandbox workspace-write --full-auto "
                        "'{describe the implementation task in detail}'` "
                        "Use Task tool with subagent_type='general-purpose' to run Codex and "
                        "preserve main context. Only write directly if the change is trivial "
                        "(typo fix, single-line constant, doc update)."
                    )
                }
            }
            print(json.dumps(output))

        sys.exit(0)  # Always allow, just add context

    except Exception as e:
        # Don't block on errors
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
