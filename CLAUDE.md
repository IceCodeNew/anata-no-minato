# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Anata-no-minato is a Docker packaging of [Ananta](https://github.com/cwt/ananta) with runtime components. It provides SSH configuration parsing and conversion to Ananta's hosts format (CSV or TOML). The project includes a helper script for easy deployment and automatic hosts.toml generation from ~/.ssh/config.

## Development Commands

### Python Package Management
- `pdm install` - Install dependencies
- `pdm run <command>` - Run commands defined in pyproject.toml
- `pdm lock` - Update lock file
- `pdm sync` - Sync environment with lock file

### Code Quality
- `pre-commit run --all-files` - Run all pre-commit hooks
- `ruff check` - Run linter
- `ruff format` - Format code
- `ruff check --fix` - Auto-fix linting issues

### Testing
- `pdm run pytest` - Run all tests
- `pdm run pytest tests/` - Run tests in specific directory
- `pdm run pytest tests/test_file.py` - Run specific test file
- `pdm run pytest -v` - Run tests with verbose output

### Building
- `pdm build` - Build Python package
- `docker build -t anata-no-minato .` - Build Docker image

## Architecture

### Core Components
1. **SSH Config Parser** (`src/sshconfig_to_ananta/ssh_config_converter.py`):
   - Parses SSH config files using regex patterns
   - Handles special Ananta tags (`#tags`) for host categorization
   - Supports host exclusion with `!ananta` tag
   - Converts SSH config entries to AnantaHost objects

2. **AnantaHost Model** (`src/sshconfig_to_ananta/ananta_host.py`):
   - Represents SSH host configuration for Ananta
   - Handles path relocation for container environments
   - Supports both CSV and TOML output formats
   - Validates port numbers and required fields

3. **CLI Interface** (`src/sshconfig_to_ananta/main.py`):
   - Command-line argument parsing
   - File I/O operations
   - Optional TOML output via tomli-w dependency

### Docker Integration
- **Entry Point** (`docker-entrypoint.sh`):
  - Parses command-line arguments for Ananta
  - Auto-generates hosts.toml from SSH config
  - Handles key path relocation for mounted SSH directories
  - Uses catatonit as PID 1 init system

### SSH Config Features
- **Tag System**: Use `#tags` comments to categorize hosts
- **Host Exclusion**: Add `!ananta` tag to exclude hosts
- **Path Relocation**: Container-aware SSH key path resolution
- **Proxy Warnings**: Logs warnings for ProxyCommand/ProxyJump configs

## Package Structure
```
src/sshconfig_to_ananta/
├── __init__.py
├── __main__.py
├── main.py           # CLI entry point
├── ssh_config_converter.py  # SSH config parsing logic
└── ananta_host.py    # Host representation model
```

## Configuration
- **pyproject.toml**: PDM-based Python packaging with optional tomli-w dependency
- **.pre-commit-config.yaml**: Pre-commit hooks for code quality
- **Dockerfile**: Multi-stage build with uv package manager
- **GitHub Actions**: CI/CD for testing, linting, and PyPI publishing

## Testing
- Tests located in `tests/` directory
- Unit tests for SSH config parsing and host conversion
- Test coverage via codecov
- pytest as test runner
