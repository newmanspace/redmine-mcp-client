# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Redmine MCP Client is a Claude Code plugin that provides integration with Redmine MCP Server. It enables users to manage Issues, Wiki pages, Projects, search across Redmine, and build AI-powered reports.

**MCP Server**: `http://YOUR_SERVER_IP:8000/mcp`

## Architecture

```
redmine-mcp-client/
├── .claude-plugin/plugin.json   # Plugin manifest
├── .mcp.json                    # MCP server configuration
├── commands/redmine.md          # /redmine command entry point
├── skills/redmine-assistant/    # Auto-triggered skill
│   ├── SKILL.md
│   ├── references/
│   │   ├── mcp-tools.md         # MCP tools reference
│   │   └── workflows.md         # Workflow examples
│   └── examples/
└── README.md
```

## Available Commands

### Test Plugin
```bash
cc --plugin-dir /docker/redmine-mcp-client
```

### Use Commands
```
/redmine issues list
/redmine issues search "bug"
/redmine wiki get <project> <title>
/redmine reports templates list
```

## MCP Tools (38 total)

- **Issue Management**: 5 tools (get, list, search, create, update)
- **Wiki Management**: 3 tools (get, create, update)
- **Project Management**: 2 tools (list projects, search issues)
- **Search**: 1 tool (global search across issues+wiki)
- **Report Builder**: 10 tools (SQL, templates, preview, execute)
- **Template Versioning**: 5 tools (versions, rollback, compare, activate)
- **Subscriptions**: 4 tools (subscribe, list, unsubscribe, test)
- **ETL Management**: 4 tools (backfill, rerun, dashboard, history)

## Development Guidelines

- Plugin structure follows Claude Code plugin conventions
- Skills use progressive disclosure (SKILL.md lean, details in references/)
- All tool calls should handle errors gracefully
- Use pagination for large result sets (limit=25 default)

## Reference

- Full tool documentation: `skills/redmine-assistant/references/mcp-tools.md`
- Workflow examples: `skills/redmine-assistant/references/workflows.md`
