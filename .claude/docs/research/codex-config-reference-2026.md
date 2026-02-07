# Codex CLI Configuration Reference (2026)

**Last Updated:** February 2026
**Research Date:** 2026-02-07

Complete reference for Codex CLI `.codex/config.toml` configuration options based on official documentation and latest features.

---

## Table of Contents

1. [Configuration File Locations](#configuration-file-locations)
2. [Core Settings](#core-settings)
3. [Model & Provider Settings](#model--provider-settings)
4. [Approval Policies](#approval-policies)
5. [Sandbox Modes](#sandbox-modes)
6. [Features](#features)
7. [MCP Servers](#mcp-servers)
8. [Profiles](#profiles)
9. [Environment Variables](#environment-variables)
10. [Skills](#skills)
11. [GPT-5.3-Codex Specific](#gpt-53-codex-specific)
12. [Complete Example](#complete-example)

---

## Configuration File Locations

**User-level (global):**
```
~/.codex/config.toml
```

**Project-level (scoped):**
```
.codex/config.toml
```

**Important Notes:**
- Project-scoped configs only load when you trust the project
- CLI and IDE extension share the same configuration
- Project settings override global settings
- Schema available at: `codex-rs/core/config.schema.json`

**VS Code Integration:**
Install "Even Better TOML" extension for autocomplete and diagnostics when editing config.toml.

---

## Core Settings

### Basic Configuration Keys

```toml
# Model selection
model = "gpt-5.2-codex"  # Default: gpt-5.2-codex

# Model provider (from [model_providers])
model_provider = "openai"  # Default: openai

# Approval policy
approval_policy = "on-request"  # Options: untrusted, on-failure, on-request, never

# Sandbox mode
sandbox_mode = "workspace-write"  # Options: read-only, workspace-write, danger-full-access

# Model reasoning effort
model_reasoning_effort = "medium"  # Options: minimal, low, medium, high, xhigh

# Model verbosity
model_verbosity = "medium"  # Options: low, medium, high

# Web search
web_search = "disabled"  # Options: disabled, enabled

# Suppress warnings
suppress_unstable_features_warning = false  # Default: false
```

---

## Model & Provider Settings

### Model Configuration

```toml
model = "gpt-5.3-codex"  # Available models:
                          # - gpt-5.3-codex (latest, Feb 2026)
                          # - gpt-5.2-codex
                          # - gpt-5.2
                          # - gpt-4o
                          # - custom via providers

model_reasoning_effort = "xhigh"  # xhigh available on gpt-5.2-codex and gpt-5.2
model_verbosity = "high"
```

### Model Provider Configuration

```toml
[model_providers.<provider_id>]
name = "Provider Name"
base_url = "https://api.provider.com"  # API base URL
api_key_env = "PROVIDER_API_KEY"       # Environment variable for API key
retry_count = 4                         # HTTP request retry count (default: 4)
idle_timeout_ms = 300000                # SSE stream timeout (default: 300000)
wire_api = "responses"                  # Wire protocol type

# HTTP headers (optional)
[model_providers.<provider_id>.http_headers]
Authorization = "Bearer ${PROVIDER_API_KEY}"
```

**Example Providers:**

```toml
# OpenAI (default)
[model_providers.openai]
name = "OpenAI"
api_key_env = "OPENAI_API_KEY"

# Azure OpenAI
[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://your-resource.openai.azure.com"
api_key_env = "AZURE_OPENAI_API_KEY"

# Ollama (local)
[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434"

# LiteLLM Proxy
[model_providers.litellm]
name = "LiteLLM"
base_url = "http://localhost:4000"
http_headers = { "Authorization"= "Bearer sk-dummy" }
wire_api = "responses"
```

---

## Approval Policies

Controls when Codex pauses for approval before executing commands.

```toml
approval_policy = "on-request"  # Choose one:
```

**Available Policies:**

| Policy | Description | Use Case |
|--------|-------------|----------|
| `untrusted` | Only known-safe read-only commands auto-run | Untrusted environments, maximum safety |
| `on-failure` | Auto-run in sandbox, prompt only on failure | Development with safety net |
| `on-request` | Model decides when to ask (default) | Balanced control |
| `never` | Never prompt, auto-execute everything | Trusted scripts, CI/CD (⚠️ use with caution) |

**Smart Approvals:**
- Stable feature (on by default)
- Provides `prefix_rule` suggestions on escalation requests
- Helps refine approval behavior over time

**Command-line Override:**
```bash
codex --ask-for-approval never
codex --ask-for-approval on-failure
```

---

## Sandbox Modes

Controls what Codex can technically do (file access, network access).

```toml
sandbox_mode = "workspace-write"  # Choose one
```

**Available Modes:**

| Mode | File Access | Network | Use Case |
|------|-------------|---------|----------|
| `read-only` | Read only, no writes | ❌ No | Analysis, review, debugging |
| `workspace-write` | Write in workspace + temp dirs | ❌ No (default) | Development, safe execution |
| `danger-full-access` | Write anywhere, full system access | ✅ Yes | ⚠️ Use extreme caution |

### Workspace-Write Configuration

```toml
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false  # Set true to enable outbound network
additional_writable_roots = [
    "/tmp",
    "/path/to/additional/dir"
]
```

**Enable Network Access:**

```bash
# Command-line
codex --sandbox workspace-write -c 'sandbox_workspace_write.network_access=true'

# Config file
[sandbox_workspace_write]
network_access = true
```

### Convenience Flags

```bash
# Low-friction local work (on-request + workspace-write)
codex --full-auto

# Completely unrestricted (⚠️ DANGEROUS)
codex --sandbox danger-full-access
codex --dangerously-bypass-approvals-and-sandbox
```

---

## Features

Use `[features]` to toggle optional and experimental capabilities.

```toml
[features]
skills = true                  # Enable agent skills
unified_exec = true            # Unified execution model
shell_snapshot = true          # Beta: Snapshot shell environment
steer = true                   # Stable: Mid-turn steering
collab = true                  # Collaboration features
collaboration_modes = true     # Team collaboration
apps = true                    # App/connector support
personality = true             # Stable: Personality configuration
apply_patch = false            # Experimental: Freeform apply_patch tool
shell_tool = true              # Stable: Default shell tool (on by default)
app_server = false             # Experimental: App-server API
remote_compaction = true       # Experimental: Remote compaction (on by default, ChatGPT auth only)
elevated_windows_sandbox = false  # Experimental: Windows elevated sandbox
windows_restricted_token = false  # Experimental: Windows restricted-token sandbox
agents_md_scope = false        # Experimental: AGENTS.md scope/precedence
```

**Enable via CLI:**
```bash
codex --enable feature_name
codex --enable skills --enable steer
```

**Feature Maturity Levels (2026):**

| Feature | Status | Description |
|---------|--------|-------------|
| `steer` | ✅ Stable | Send messages during running tasks |
| `personality` | ✅ Stable | Personality configuration |
| `shell_tool` | ✅ Stable | Default shell tool (on by default) |
| `shell_snapshot` | 🔶 Beta | Snapshot shell environment for speed |
| `apply_patch` | 🧪 Experimental | Freeform apply_patch tool |
| `app_server` | 🧪 Experimental | App-server API (requires opt-in) |
| `remote_compaction` | 🧪 Experimental | Remote compaction (on by default) |

---

## MCP Servers

Configure Model Context Protocol servers for extending Codex capabilities.

```toml
[mcp_servers.<server-name>]
command = "command-to-start-server"  # Required
args = ["arg1", "arg2"]              # Optional
startup_timeout_sec = 10             # Default: 10
tool_timeout_sec = 60                # Default: 60
enabled = true                       # Set false to disable without deleting

# Environment variables
[mcp_servers.<server-name>.env]
ENV_VAR_NAME = "value"

# Reference env vars
env_vars = ["API_KEY", "OTHER_VAR"]
```

**Example Configurations:**

```toml
# Chrome DevTools MCP
[mcp_servers.chrome]
command = "npx"
args = ["-y", "chrome-devtools-mcp@latest"]
startup_timeout_sec = 30

# CircleCI MCP (2026 example)
[mcp_servers.circleci]
startup_timeout_sec = 30
command = "npx"
args = ["-y", "@circleci/mcp-server-circleci@latest"]
env_vars = ["CIRCLECI_TOKEN"]

[mcp_servers.circleci.env]
CIRCLECI_BASE_URL = "https://circleci.com"

# Claude MCP (migrated to skills)
[mcp_servers.claude]
command = "claude"
args = ["mcp", "serve"]

# Custom Python MCP Server
[mcp_servers.my_tool]
command = "uv"
args = ["run", "python", "-m", "my_tool.server"]
tool_timeout_sec = 120
enabled = true

[mcp_servers.my_tool.env]
API_KEY = "${MY_TOOL_API_KEY}"  # References environment variable
```

**Important Notes:**
- MCP config shared between CLI and IDE extension
- Project-scoped MCP servers only in trusted projects
- Environment variables must be referenced, not hardcoded
- Use `enabled = false` to temporarily disable

---

## Profiles

Save named sets of configuration values and switch between them.

**⚠️ Status:** Experimental (may change or be removed)

```toml
[profiles.deep-review]
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
model_verbosity = "high"
approval_policy = "on-request"

[profiles.lightweight]
model = "gpt-5.2-codex"
model_reasoning_effort = "medium"
model_verbosity = "low"
sandbox_mode = "read-only"

[profiles.fast-dev]
model = "gpt-5.2-codex"
approval_policy = "on-failure"
sandbox_mode = "workspace-write"
model_reasoning_effort = "low"

[profiles.dangerous]
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

**Usage:**
```bash
codex --profile deep-review
codex --profile lightweight
```

---

## Environment Variables

Control which environment variables Codex forwards to spawned commands.

```toml
[shell_environment_policy]
inherit = "core"  # Options: "none", "core", "all"

# Include only specific variables (whitelist)
include_only = ["PATH", "HOME", "USER"]

# Exclude specific variables (blacklist)
exclude = ["AWS_*", "SECRET_*"]

# Explicitly set variables
[shell_environment_policy.set]
MY_VAR = "custom_value"
EDITOR = "vim"
```

**Inherit Options:**

| Option | Description | Variables Included |
|--------|-------------|-------------------|
| `none` | Clean start, no inherited vars | None |
| `core` | Minimal essential set | PATH, HOME, USER, SHELL, etc. |
| `all` | All parent environment vars | Everything |

**Glob Patterns:**
- Case-insensitive
- Supports `*`, `?`, `[A-Z]` wildcards
- Example: `AWS_*`, `*_TOKEN`, `SECRET_[A-Z]*`

**Example Configurations:**

```toml
# Minimal security-conscious setup
[shell_environment_policy]
inherit = "core"
exclude = ["*_TOKEN", "*_SECRET", "*_KEY"]

# Whitelist-only approach
[shell_environment_policy]
inherit = "none"
include_only = ["PATH", "HOME", "LANG"]

# Development with custom settings
[shell_environment_policy]
inherit = "core"

[shell_environment_policy.set]
NODE_ENV = "development"
RUST_LOG = "debug"
```

---

## Skills

Agent skills extend Codex with task-specific capabilities.

**Skill Directory Structure:**
```
~/.codex/skills/
├── skill-name/
│   ├── SKILL.md        # Required: name, description, instructions
│   ├── script.sh       # Optional: helper scripts
│   └── resources/      # Optional: additional files
```

**SKILL.md Format:**
```markdown
# Skill Name

## Description
Brief description of what this skill does.

## Instructions
Step-by-step instructions for the agent to follow.

## Examples
Optional usage examples.
```

**Enable Skills:**
```toml
[features]
skills = true
```

**Invoke Skills:**
```bash
codex --skill skill-name
/skill skill-name  # In interactive mode
```

**Built-in Skills Examples:**
- Code review workflows
- Testing patterns
- Deployment procedures
- Documentation generation

---

## GPT-5.3-Codex Specific

**Released:** February 5, 2026

### Key Features

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"  # Supported on 5.3
```

**Capabilities:**
- **25% faster** than gpt-5.2-codex
- **Agentic coding**: Long-running tasks with research and tool use
- **Mid-turn steering**: Interact while task is running (stable feature)
- **Broader scope**: General work agent (not just coding)
- **Self-developed**: First model instrumental in creating itself

### Steering Configuration

```toml
[features]
steer = true  # Stable in 2026
```

**Enable in App:**
Settings → General → Follow-up behavior

**CLI Usage:**
```bash
# Send message during execution
# (Interactive prompt appears when task is running)
```

### Performance

- **SWE-Bench Pro**: State-of-the-art
- **Terminal-Bench**: Industry high
- **Real-world tasks**: Superior to previous models

### Security

- First model under "High capability" in Cybersecurity domain
- Additional safeguards activated per Preparedness Framework
- Use appropriate sandbox and approval settings

---

## Complete Example

Comprehensive `~/.codex/config.toml` example with common settings:

```toml
# ============================================
# Codex CLI Configuration
# ============================================

# Core Settings
model = "gpt-5.3-codex"
model_provider = "openai"
model_reasoning_effort = "high"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "disabled"
suppress_unstable_features_warning = false

# ============================================
# Features
# ============================================
[features]
skills = true
unified_exec = true
shell_snapshot = true
steer = true
collab = true
collaboration_modes = true
apps = true
personality = true
shell_tool = true
remote_compaction = true

# ============================================
# Sandbox Configuration
# ============================================
[sandbox_workspace_write]
network_access = false
additional_writable_roots = [
    "/tmp",
    "/var/tmp"
]

# ============================================
# Environment Variables
# ============================================
[shell_environment_policy]
inherit = "core"
exclude = ["*_TOKEN", "*_SECRET", "*_KEY", "AWS_*"]

[shell_environment_policy.set]
EDITOR = "vim"
RUST_LOG = "info"

# ============================================
# Model Providers
# ============================================
[model_providers.openai]
name = "OpenAI"
api_key_env = "OPENAI_API_KEY"
retry_count = 4
idle_timeout_ms = 300000

[model_providers.ollama]
name = "Ollama"
base_url = "http://localhost:11434"

# ============================================
# MCP Servers
# ============================================
[mcp_servers.chrome]
command = "npx"
args = ["-y", "chrome-devtools-mcp@latest"]
startup_timeout_sec = 30

[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
tool_timeout_sec = 60

# ============================================
# Profiles
# ============================================
[profiles.review]
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
model_verbosity = "high"
approval_policy = "on-request"

[profiles.fast]
model = "gpt-5.2-codex"
model_reasoning_effort = "medium"
model_verbosity = "low"
sandbox_mode = "read-only"

# ============================================
# Notice Settings (UI "don't show again")
# ============================================
[notice]
# Automatically managed by Codex
```

---

## Command-Line Overrides

Any config.toml setting can be overridden from CLI:

```bash
# Single override
codex -c key=value

# Multiple overrides
codex -c model=gpt-5.3-codex -c approval_policy=never

# Nested keys (dot notation)
codex -c 'sandbox_workspace_write.network_access=true'

# Profile + overrides
codex --profile review -c model_verbosity=low

# Convenience flags
codex --full-auto  # on-request + workspace-write
codex --sandbox danger-full-access
codex --ask-for-approval never
codex --enable skills --enable steer
```

---

## Additional Resources

### Official Documentation
- **Configuration Reference**: https://developers.openai.com/codex/config-reference/
- **Config Basics**: https://developers.openai.com/codex/config-basic/
- **Advanced Configuration**: https://developers.openai.com/codex/config-advanced/
- **Sample Configuration**: https://developers.openai.com/codex/config-sample/
- **Command Line Reference**: https://developers.openai.com/codex/cli/reference/
- **MCP Documentation**: https://developers.openai.com/codex/mcp
- **Skills Documentation**: https://developers.openai.com/codex/skills
- **Security**: https://developers.openai.com/codex/security/
- **Models**: https://developers.openai.com/codex/models/
- **Changelog**: https://developers.openai.com/codex/changelog/

### GitHub Repository
- **Main Repo**: https://github.com/openai/codex
- **Config Documentation**: https://github.com/openai/codex/blob/main/docs/config.md
- **Releases**: https://github.com/openai/codex/releases
- **Example Configs**: https://github.com/feiskyer/codex-settings

### Community Resources
- **Codex Forum**: https://community.openai.com/c/codex
- **Example Configs**: Various blog posts and tutorials (see web search results)

---

## Schema and Validation

**JSON Schema Location:**
```
codex-rs/core/config.schema.json
```

**VS Code Integration:**
1. Install "Even Better TOML" extension
2. Add schema line to top of config.toml:
```toml
# yaml-language-server: $schema=path/to/config.schema.json
```

---

## Best Practices

1. **Start Conservative:**
   - Begin with `approval_policy = "on-request"`
   - Use `sandbox_mode = "workspace-write"` with `network_access = false`
   - Enable features incrementally

2. **Security:**
   - Never hardcode API keys in config.toml
   - Use environment variables for secrets
   - Exclude sensitive env vars in `[shell_environment_policy]`
   - Trust project configs carefully

3. **Performance:**
   - Use `model_reasoning_effort = "medium"` for most tasks
   - Reserve `xhigh` for complex problems
   - Enable `shell_snapshot = true` for faster repeated commands

4. **Development Workflow:**
   - Create profiles for different contexts (review, dev, fast)
   - Use `--full-auto` for trusted local development
   - Keep global config minimal, use project configs for specifics

5. **MCP Servers:**
   - Set appropriate timeouts for slow operations
   - Use `enabled = false` instead of deleting configs
   - Document custom env vars needed

---

## Troubleshooting

**Config not loading:**
- Check file location: `~/.codex/config.toml`
- Verify TOML syntax (use VS Code extension)
- Check for project trust if using `.codex/config.toml`

**MCP servers not working:**
- Verify command is in PATH
- Check startup timeout (increase if needed)
- Ensure environment variables are set
- Check logs: `codex --debug`

**Network access denied:**
- Set `sandbox_workspace_write.network_access = true`
- Or use `--sandbox danger-full-access` (⚠️ careful)

**Commands require approval:**
- Check `approval_policy` setting
- Use `--ask-for-approval never` for automation
- Review sandbox mode restrictions

---

**Document Version:** 1.0
**Last Updated:** 2026-02-07
**Next Review:** When Codex updates release
