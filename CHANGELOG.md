# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2026-03-28

### Added
- Synchronized AI agent configurations (`.agents` and `.claude`) from `redmine-mcp-server`.
- Integrated standard software development workflows (`/feature`, `/issue`, `/refactor`).

### Changed
- Refactored `test` skill to use project-specific `tests/run_all_tests.py` diagnostic tool.
- Refactored `release` skill to use project-specific `scripts/package.sh` packaging tool.

### Removed
- Deleted unrelated server-side skills (`dba-review`, `deploy`).

## [1.1.0] - 2026-03-27
- Initial release with Issue, Wiki, Project, Search, and Report Builder capabilities.
