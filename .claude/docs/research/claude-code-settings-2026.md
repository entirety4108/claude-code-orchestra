# Claude Code settings.json Configuration Reference (2026)

**Research Date:** February 7, 2026
**Source:** Official Claude Code documentation and recent announcements

---

## Executive Summary

Claude Code settings.json has been significantly enhanced in 2026 with new features including:

- **Agent Teams** (Research Preview) - Multi-agent orchestration
- **Fast Mode** - 2.5x faster Opus 4.6 responses
- **New Hook Events** - TeammateIdle, TaskCompleted, PreCompact
- **Enhanced Permission System** - Managed settings, sandbox controls
- **Extended Thinking** - Configurable thinking tokens
- **1M Token Context Window** - Available with `[1m]` suffix

---

## Table of Contents

1. [Configuration Scopes & Precedence](#configuration-scopes--precedence)
2. [Core Settings Keys](#core-settings-keys)
3. [NEW: Agent Teams Configuration](#new-agent-teams-configuration)
4. [NEW: Fast Mode Settings](#new-fast-mode-settings)
5. [Model Configuration](#model-configuration)
6. [Permission Settings](#permission-settings)
7. [Sandbox Settings](#sandbox-settings)
8. [Hook Events](#hook-events)
9. [Environment Variables](#environment-variables)
10. [MCP Server Configuration](#mcp-server-configuration)
11. [Plugin Settings](#plugin-settings)
12. [Context Management](#context-management)

---

## Configuration Scopes & Precedence

Settings follow a strict hierarchy (highest to lowest priority):

1. **Managed** - `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS) - Enterprise policies, cannot be overridden
2. **Command line arguments** - Temporary session overrides
3. **Local** - `.claude/settings.local.json` - Personal project settings (gitignored)
4. **Project** - `.claude/settings.json` - Team-shared settings (committed to repo)
5. **User** - `~/.claude/settings.json` - Personal global settings

**JSON Schema URL:** `https://json.schemastore.org/claude-code-settings.json`

Add this to your settings.json for autocomplete and validation:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

---

## Core Settings Keys

### Complete Settings Reference

| Key | Type | Description | Default | New in 2026? |
|-----|------|-------------|---------|--------------|
| `$schema` | string | JSON schema URL for validation | - | No |
| `model` | string | Default model (alias or full name) | `"default"` | No |
| `effortLevel` | string | Opus 4.6 effort: `low`, `medium`, `high` | `"high"` | **YES** |
| `fastMode` | boolean | Enable fast mode for Opus 4.6 | `false` | **YES** |
| `permissions` | object | Allow/deny/ask rules for tool access | `{}` | Enhanced |
| `env` | object | Environment variables for every session | `{}` | No |
| `hooks` | object | Custom commands at lifecycle events | `{}` | Enhanced |
| `disableAllHooks` | boolean | Disable all hooks | `false` | No |
| `allowManagedHooksOnly` | boolean | Only managed & SDK hooks | `false` | **YES** |
| `allowManagedPermissionRulesOnly` | boolean | Only managed permission rules | `false` | **YES** |
| `sandbox` | object | Bash sandbox configuration | `{}` | Enhanced |
| `teammateMode` | string | Agent team display mode | `"auto"` | **YES** |
| `attribution` | object | Git commit/PR attribution | See below | Enhanced |
| `statusLine` | object | Custom status line | `null` | No |
| `fileSuggestion` | object | Custom `@` file autocomplete | `null` | No |
| `respectGitignore` | boolean | Exclude .gitignore patterns | `true` | No |
| `outputStyle` | string | System prompt output style | `null` | No |
| `language` | string | Response language preference | `null` | No |
| `alwaysThinkingEnabled` | boolean | Enable extended thinking by default | `false` | **YES** |
| `plansDirectory` | string | Custom plan files directory | `"./plans"` | No |
| `cleanupPeriodDays` | number | Days before session deletion | `30` | No |
| `showTurnDuration` | boolean | Show turn duration | `true` | No |
| `spinnerVerbs` | object | Customize spinner verbs | `null` | No |
| `spinnerTipsEnabled` | boolean | Show tips in spinner | `true` | No |
| `terminalProgressBarEnabled` | boolean | Enable progress bar | `true` | No |
| `prefersReducedMotion` | boolean | Reduce UI animations | `false` | No |
| `autoUpdatesChannel` | string | Update channel: `stable` or `latest` | `"latest"` | No |
| `forceLoginMethod` | string | Restrict login method | `null` | No |
| `forceLoginOrgUUID` | string | Auto-select org UUID | `null` | No |
| `apiKeyHelper` | string | Script for API key generation | `null` | No |
| `otelHeadersHelper` | string | OpenTelemetry headers script | `null` | No |
| `awsAuthRefresh` | string | AWS credential refresh script | `null` | No |
| `awsCredentialExport` | string | AWS credential export script | `null` | No |
| `companyAnnouncements` | array | Startup announcements | `[]` | No |
| `enabledPlugins` | object | Plugin enable/disable map | `{}` | No |
| `extraKnownMarketplaces` | object | Custom marketplace sources | `{}` | No |
| `strictKnownMarketplaces` | array | Managed: marketplace allowlist | `null` | **YES** |
| `enableAllProjectMcpServers` | boolean | Auto-approve `.mcp.json` servers | `false` | No |
| `enabledMcpjsonServers` | array | Whitelist MCP servers | `null` | No |
| `disabledMcpjsonServers` | array | Blacklist MCP servers | `null` | No |
| `allowedMcpServers` | array | Managed: MCP server allowlist | `null` | **YES** |
| `deniedMcpServers` | array | Managed: MCP server denylist | `null` | **YES** |

---

## NEW: Agent Teams Configuration

**Status:** Research Preview (February 2026)
**Announcement:** https://www.anthropic.com/news/claude-opus-4-6

### Enable Agent Teams

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Display Mode Configuration

```json
{
  "teammateMode": "auto"  // "auto" | "in-process" | "tmux"
}
```

| Mode | Description | Requirements |
|------|-------------|--------------|
| `auto` | Split panes if in tmux, otherwise in-process | None |
| `in-process` | All teammates in main terminal | None |
| `tmux` | Each teammate in separate pane | tmux or iTerm2 + it2 CLI |

### Agent Teams Architecture

- **Team Lead** - Main session that creates team and coordinates
- **Teammates** - Independent Claude Code instances
- **Task List** - Shared work items at `~/.claude/tasks/{team-name}/`
- **Mailbox** - Inter-agent messaging system
- **Team Config** - `~/.claude/teams/{team-name}/config.json`

### Usage Patterns

**Start a team:**
```
Create an agent team with 3 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

**Require plan approval:**
```
Spawn an architect teammate to refactor auth. Require plan approval before changes.
```

**Delegate mode:** Press `Shift+Tab` to prevent lead from implementing (coordination only)

**Interact with teammates:**
- In-process: `Shift+Up/Down` to select, then type to message
- Split-pane: Click into pane to interact directly

### Limitations (Research Preview)

- No session resumption with in-process teammates
- One team per session
- No nested teams (teammates can't spawn teams)
- Lead is fixed (can't transfer leadership)
- Permissions set at spawn time
- Split panes not supported in VS Code terminal, Windows Terminal, Ghostty

---

## NEW: Fast Mode Settings

**Status:** Research Preview (February 2026)
**Speed:** 2.5x faster output tokens
**Pricing:** $30/$150 MTok (50% discount until Feb 16, 2026)

### Enable Fast Mode

```json
{
  "fastMode": true
}
```

Or use `/fast` command to toggle during session.

### Requirements

- Extra usage enabled in billing settings
- **NOT** available on Bedrock, Vertex AI, Azure Foundry
- Teams/Enterprise: Admin must enable in settings

### Fast Mode Behavior

- Automatically switches to Opus 4.6 when enabled
- Persists across sessions
- Shows `↯` icon next to prompt
- Auto-fallback to standard speed on rate limit
- Compatible with 1M token extended context

### Cost Considerations

| Mode | Input (MTok) | Output (MTok) |
|------|--------------|---------------|
| Fast (<200K) | $30 | $150 |
| Fast (>200K) | $60 | $225 |

**Important:** Switching mid-conversation re-bills entire context at fast mode rates.

---

## Model Configuration

### Model Aliases (Always Latest Version)

| Alias | Current Model | Use Case |
|-------|---------------|----------|
| `default` | Opus 4.6 (Max/Teams/Pro) | Account-specific default |
| `opus` | Opus 4.6 | Complex reasoning tasks |
| `sonnet` | Sonnet 4.5 | Daily coding tasks |
| `haiku` | Haiku | Fast, simple tasks |
| `sonnet[1m]` | Sonnet 4.5 (1M context) | Long sessions |
| `opusplan` | Opus → Sonnet | Planning with Opus, execution with Sonnet |

### Configuration Methods (Priority Order)

1. `/model <alias|name>` - During session
2. `claude --model <alias|name>` - At startup
3. `ANTHROPIC_MODEL=<alias|name>` - Environment variable
4. `"model": "opus"` - settings.json

### Example settings.json

```json
{
  "model": "opus",
  "effortLevel": "high"
}
```

### Effort Levels (Opus 4.6 Only)

Controls adaptive reasoning allocation:

- `low` - Faster, cheaper for straightforward tasks
- `medium` - Balanced
- `high` (default) - Deeper reasoning for complex problems

**Configure via:**
- `/model` menu (use arrow keys to adjust slider)
- `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high`
- `"effortLevel": "high"` in settings.json

### Extended Context Windows

```bash
# Use 1M token context
/model sonnet[1m]
/model claude-sonnet-4-5-20250929[1m]
```

**Note:** Opus 4.6 1M context available for API/pay-as-you-go users only (not Pro/Max/Teams/Enterprise at launch)

### Model Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override `opus` alias |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override `sonnet` alias |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override `haiku` alias |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents |

### Prompt Caching Configuration

```bash
DISABLE_PROMPT_CACHING=1          # Disable all caching
DISABLE_PROMPT_CACHING_HAIKU=1    # Disable for Haiku only
DISABLE_PROMPT_CACHING_SONNET=1   # Disable for Sonnet only
DISABLE_PROMPT_CACHING_OPUS=1     # Disable for Opus only
```

---

## Permission Settings

### Structure

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "WebFetch"
    ],
    "additionalDirectories": ["../docs/"],
    "defaultMode": "acceptEdits",
    "disableBypassPermissionsMode": "disable"
  }
}
```

### Permission Evaluation Flow

1. **Hooks** - Run first, can allow/deny/continue
2. **Deny rules** - Block regardless of other rules
3. **Allow rules** - Permit if matched
4. **Ask rules** - Prompt for approval
5. **Permission mode** - Apply default behavior
6. **canUseTool callback** - Final decision point (SDK only)

### Permission Modes

| Mode | Description |
|------|-------------|
| `default` | No auto-approvals |
| `acceptEdits` | Auto-approve file edits & filesystem ops |
| `bypassPermissions` | Auto-approve all tools (dangerous!) |
| `plan` | No execution, planning only |

### Permission Rule Syntax

```json
"Tool"                    // All uses of tool
"Tool(pattern)"           // Matches pattern
"Bash(npm run *)"         // Commands starting with "npm run"
"Read(./.env)"            // Specific file
"Write(src/**)"           // Directory pattern
"WebFetch(domain:*.com)"  // Domain pattern
"mcp__github__*"          // All GitHub MCP tools
```

### NEW: Managed Permission Settings

**Managed settings only:**

```json
{
  "allowManagedPermissionRulesOnly": true,
  "permissions": {
    "deny": ["WebFetch", "Bash(rm *)"],
    "allow": ["Read", "Write(src/**)"]
  }
}
```

When enabled, user/project permission rules are ignored.

### Known Issue (v1.0.93)

**CRITICAL SECURITY BUG:** `deny` permissions are not enforced. Track at:
- https://github.com/anthropics/claude-code/issues/6631
- https://github.com/anthropics/claude-code/issues/6699

**Workaround:** Use PreToolUse hooks to block dangerous operations.

---

## Sandbox Settings

**Platforms:** macOS, Linux, WSL2

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "allowUnsandboxedCommands": false,
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"],
      "allowAllUnixSockets": false,
      "allowLocalBinding": true,
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    },
    "enableWeakerNestedSandbox": false
  }
}
```

### Network Isolation

- **Default:** Network disabled in sandbox
- **allowedDomains:** Whitelist outbound connections (supports wildcards)
- **allowLocalBinding:** Bind to localhost ports (macOS only)
- **allowUnixSockets:** Specific socket paths
- **Proxy ports:** Auto-assigned if not specified

### Command Exclusions

Commands in `excludedCommands` run outside sandbox (use carefully).

---

## Hook Events

### Complete Hook Event List

| Event | When it fires | Matchers | New in 2026? |
|-------|---------------|----------|--------------|
| `SessionStart` | Session begins/resumes | Session source | No |
| `UserPromptSubmit` | User submits prompt | None | No |
| `PreToolUse` | Before tool execution | Tool name | No |
| `PermissionRequest` | Permission dialog | Tool name | No |
| `PostToolUse` | After tool succeeds | Tool name | No |
| `PostToolUseFailure` | After tool fails | Tool name | No |
| `Notification` | Notification sent | Notification type | No |
| `SubagentStart` | Subagent spawned | Agent type | No |
| `SubagentStop` | Subagent finished | Agent type | No |
| `Stop` | Claude finishes response | None | No |
| `TeammateIdle` | Teammate about to go idle | None | **YES** |
| `TaskCompleted` | Task being marked complete | None | **YES** |
| `PreCompact` | Before context compaction | Trigger type | **YES** |
| `SessionEnd` | Session terminates | End reason | No |

### NEW: TeammateIdle Hook

Runs when an agent team teammate is about to go idle.

```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Teammate idle check' | tee -a ~/.claude/teammate-log.txt"
          }
        ]
      }
    ]
  }
}
```

**Exit code 2:** Send feedback and keep teammate working

### NEW: TaskCompleted Hook

Runs when a task is being marked as completed.

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify all tests pass before marking task complete. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

**Exit code 2:** Prevent completion and send feedback

### NEW: PreCompact Hook

Runs just before context compaction.

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/save-context.sh"
          }
        ]
      }
    ]
  }
}
```

**Matchers:** `manual` or `auto`

**Note:** Cannot stop compaction, only run side effects.

### Hook Types

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          // Command hook
          {
            "type": "command",
            "command": "prettier --write $(jq -r '.tool_input.file_path')",
            "timeout": 30
          },
          // Prompt hook (uses LLM)
          {
            "type": "prompt",
            "prompt": "Check if file formatting is correct",
            "model": "haiku"
          },
          // Agent hook (multi-turn with tools)
          {
            "type": "agent",
            "prompt": "Verify code quality meets standards",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### Hook Input/Output

**Input (stdin):** JSON with event data
```json
{
  "session_id": "abc123",
  "cwd": "/Users/sarah/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {"command": "npm test"}
}
```

**Output (exit codes):**
- **0** - Allow action (stdout added to context for SessionStart/UserPromptSubmit)
- **2** - Block action (stderr becomes feedback to Claude)
- **Other** - Allow action (stderr logged, not shown)

**Structured JSON output (exit 0):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep"
  }
}
```

### Matcher Examples

```json
// Tool name matchers
"Bash"              // Exact match
"Edit|Write"        // Multiple tools
"mcp__.*"           // All MCP tools
"mcp__github__.*"   // All GitHub MCP tools

// SessionStart matchers
"startup"           // New session
"resume"            // Resumed session
"compact"           // After compaction
"clear"             // After /clear

// Notification matchers
"permission_prompt"
"idle_prompt"
"auth_success"
```

### Disabling Hooks

```json
{
  "disableAllHooks": true
}
```

Or use `/hooks` menu toggle.

**NEW:** Managed settings can use:
```json
{
  "allowManagedHooksOnly": true
}
```

---

## Environment Variables

### Complete Variable Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| **Authentication** |
| `ANTHROPIC_API_KEY` | API key for Claude SDK | API token |
| `ANTHROPIC_AUTH_TOKEN` | Custom auth header | Bearer token |
| **Model Configuration** |
| `ANTHROPIC_MODEL` | Override default model | `claude-opus-4-6-20250514` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus alias target | Model ID |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet alias target | Model ID |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku alias target | Model ID |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Subagent model | Model ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort level | `low`/`medium`/`high` |
| **NEW: Agent Teams** |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Enable agent teams | `1` |
| **Output Configuration** |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens | `32000` (max: `64000`) |
| `MAX_THINKING_TOKENS` | Extended thinking budget | `10000` or `0` |
| **Context Management** |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Compaction threshold % | `95` |
| `DISABLE_COMPACT` | Disable auto-compaction | `1` |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | Disable auto memory | `1` |
| **Prompt Caching** |
| `DISABLE_PROMPT_CACHING` | Disable all caching | `1` |
| `DISABLE_PROMPT_CACHING_HAIKU` | Disable Haiku caching | `1` |
| `DISABLE_PROMPT_CACHING_SONNET` | Disable Sonnet caching | `1` |
| `DISABLE_PROMPT_CACHING_OPUS` | Disable Opus caching | `1` |
| **MCP Configuration** |
| `MAX_MCP_OUTPUT_TOKENS` | MCP tool output limit | `50000` (default) |
| **System Configuration** |
| `CLAUDE_CODE_SHELL` | Override shell detection | `bash` |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable OpenTelemetry | `1` |
| `DISABLE_TELEMETRY` | Opt out of telemetry | `1` |
| `DISABLE_AUTOUPDATER` | Disable auto-updates | `1` |

### Setting Environment Variables

**In settings.json:**
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
    "MAX_THINKING_TOKENS": "10000",
    "ANTHROPIC_MODEL": "claude-opus-4-6-20250514"
  }
}
```

**Precedence:** Shell environment > settings.json env object

---

## MCP Server Configuration

### Project-Level MCP (`.mcp.json`)

```json
{
  "enableAllProjectMcpServers": true
}
```

Or whitelist/blacklist specific servers:

```json
{
  "enabledMcpjsonServers": ["memory", "github"],
  "disabledMcpjsonServers": ["filesystem"]
}
```

### NEW: Managed MCP Settings

**Managed settings only:**

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "memory"}
  ],
  "deniedMcpServers": [
    {"serverName": "filesystem"}
  ]
}
```

**Precedence:** Deny > Allow

---

## Plugin Settings

### Enable/Disable Plugins

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  }
}
```

Format: `"plugin-name@marketplace": boolean`

### Extra Marketplaces

```json
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  }
}
```

### NEW: Strict Known Marketplaces (Managed)

**Enterprise lockdown:**

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/plugins",
      "ref": "v2.0",
      "path": "marketplace"
    },
    {
      "source": "git",
      "url": "https://gitlab.example.com/tools/plugins.git",
      "ref": "main"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json",
      "headers": {"Authorization": "Bearer ${TOKEN}"}
    },
    {
      "source": "npm",
      "package": "@acme-corp/claude-plugins"
    },
    {
      "source": "file",
      "path": "/usr/local/share/claude/marketplace.json"
    },
    {
      "source": "directory",
      "path": "/usr/local/share/claude/plugins"
    },
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Behavior:**
- `undefined` - No restrictions
- `[]` - Complete lockdown
- Array - Allowlist (exact matching required)

---

## Context Management

### Auto-Compaction Settings

**Trigger threshold:** ~95% context capacity (or 25% remaining)

**Environment variables:**
```bash
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=90  # Adjust threshold
DISABLE_COMPACT=1                    # Disable auto-compact
```

**Settings.json:**
```json
{
  "autoCompactEnabled": false  // Equivalent to DISABLE_COMPACT=1
}
```

**Buffer:** 13,000 tokens reserved for Session Memory compression

### Session Memory

```json
{
  "sessionMemoryEnabled": true
}
```

Or:
```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # Disable
```

### NEW: Extended Thinking

```json
{
  "alwaysThinkingEnabled": true
}
```

**Configure thinking budget:**
```bash
MAX_THINKING_TOKENS=10000  # Set budget
MAX_THINKING_TOKENS=0      # Disable extended thinking
```

### Re-inject Context After Compaction

Use SessionStart hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run tests before commit.'"
          }
        ]
      }
    ]
  }
}
```

---

## Attribution Settings

### Git Commit & PR Attribution

```json
{
  "attribution": {
    "commit": "🤖 Generated with Claude Code\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
    "pr": "🤖 Generated with Claude Code"
  }
}
```

**Hide attribution:**
```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

**DEPRECATED:** `includeCoAuthoredBy` (use `attribution` instead)

---

## File Suggestion Settings

Custom script for `@` file autocomplete in large monorepos:

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  },
  "respectGitignore": true
}
```

**Script input (stdin):**
```json
{"query": "controller"}
```

**Script output (stdout):**
Newline-separated file paths (max 15)

**Environment variables available:**
- `CLAUDE_PROJECT_DIR`
- All other hook environment variables

---

## Status Line Settings

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh"
  }
}
```

Script runs periodically, output displayed in status bar.

---

## Advanced Settings

### Cleanup Period

```json
{
  "cleanupPeriodDays": 20  // Default: 30
}
```

Days before inactive sessions are deleted.

### Company Announcements

```json
{
  "companyAnnouncements": [
    "Welcome to Acme Corp!",
    "Remember to run security scans before deploying"
  ]
}
```

Displayed at Claude Code startup.

### Output Style

```json
{
  "outputStyle": "Explanatory"
}
```

Adjusts system prompt to influence response style.

### Language Preference

```json
{
  "language": "japanese"
}
```

Claude's preferred response language.

### UI Customization

```json
{
  "showTurnDuration": false,
  "spinnerTipsEnabled": false,
  "terminalProgressBarEnabled": false,
  "prefersReducedMotion": true,
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting", "Analyzing"]
  }
}
```

### Auto-Updates

```json
{
  "autoUpdatesChannel": "stable"  // "stable" or "latest" (default)
}
```

Or disable:
```bash
DISABLE_AUTOUPDATER=1
```

### Login Configuration

```json
{
  "forceLoginMethod": "claudeai",  // "claudeai" or "console"
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### Plans Directory

```json
{
  "plansDirectory": "./project-plans"
}
```

Custom directory for plan files (relative to project root).

---

## Example Configurations

### Minimal Development Setup

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "sonnet",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff *)"
    ],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)", "WebFetch"]
  }
}
```

### Production Team Configuration

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "opus",
  "effortLevel": "high",
  "permissions": {
    "defaultMode": "acceptEdits",
    "deny": [
      "Read(./.env*)",
      "Read(./secrets/**)",
      "Bash(rm -rf *)",
      "Bash(curl *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $(jq -r '.tool_input.file_path')"
          }
        ]
      }
    ]
  },
  "attribution": {
    "commit": "Co-Authored-By: Claude Code <noreply@anthropic.com>",
    "pr": "Generated with Claude Code"
  }
}
```

### Enterprise Managed Settings

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "allowManagedHooksOnly": true,
  "allowManagedPermissionRulesOnly": true,
  "permissions": {
    "deny": ["WebFetch", "Bash(curl *)", "Read(./.env*)"],
    "disableBypassPermissionsMode": "disable"
  },
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    }
  ],
  "deniedMcpServers": [
    {"serverName": "filesystem"}
  ],
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false,
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

### Agent Teams Research Setup

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux",
  "model": "opus",
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": ["Bash(git *)", "Read", "Write(src/**)"]
  },
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Teammate idle at $(date)' >> ~/.claude/team-activity.log"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify all tests pass before marking complete",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## Migration Notes

### Deprecated Settings

- `includeCoAuthoredBy` → Use `attribution.commit` instead
- `ANTHROPIC_SMALL_FAST_MODEL` → Use `ANTHROPIC_DEFAULT_HAIKU_MODEL`

### Breaking Changes in 2026

None reported. New features are opt-in (agent teams, fast mode).

### Known Issues

1. **Deny permissions not enforced** (v1.0.93) - Use PreToolUse hooks as workaround
2. **Agent teams session resumption** - In-process teammates not restored on `/resume`
3. **Fast mode availability** - Not available on third-party cloud providers

---

## Resources

### Official Documentation

- [Settings Reference](https://code.claude.com/docs/en/settings)
- [Model Configuration](https://code.claude.com/docs/en/model-config)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- [Fast Mode](https://code.claude.com/docs/en/fast-mode)
- [Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)
- [Complete Documentation Index](https://code.claude.com/docs/llms.txt)

### Announcements

- [Claude Opus 4.6 Release](https://www.anthropic.com/news/claude-opus-4-6) (Feb 5, 2026)
- [Agent Teams TechCrunch](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/)
- [Release Notes](https://support.claude.com/en/articles/12138966-release-notes)

### Community Resources

- [Claude Code Settings Guide (eesel.ai)](https://www.eesel.ai/blog/settings-json-claude-code)
- [Hooks Mastery (GitHub)](https://github.com/disler/claude-code-hooks-mastery)
- [Claude Code Settings Examples (GitHub)](https://github.com/feiskyer/claude-code-settings)
- [Agent Teams Guide](https://addyosmani.com/blog/claude-code-agent-teams/)

### Developer Tools

- JSON Schema: `https://json.schemastore.org/claude-code-settings.json`
- Settings UI: Use `/config` command in Claude Code REPL
- Hooks UI: Use `/hooks` command for interactive hook configuration
- Model Selection: Use `/model` command to switch models with UI

---

**Document Version:** 1.0
**Last Updated:** February 7, 2026
**Compiled by:** Claude Code Subagent (Research Task)
