# AGENTS

## Project overview

Anata-no-minato packages [Ananta](https://github.com/cwt/ananta) and its runtime in a hardened container. It also provides an SSH configuration converter and a host-side wrapper that can generate Ananta host files from `~/.ssh/config`.

## Documentation

- Keep `README.md` and its translations focused on installation, configuration, operation, and user-visible behavior.
- Keep this file focused on development rules and project architecture.
- Update the document that owns a changed decision in the same change as the code.
- Write directly, use established terms, and do not hard-wrap prose.

## Engineering rules

- Never commit real credentials, private addresses, private source URLs, generated content, or runtime state. Use dummy public test data.
- Validate configuration at its input boundary instead of silently coercing invalid values.
- Keep dependencies minimal and prefer maintained libraries over custom infrastructure.
- Keep comments concise and in English.
- Preserve compatibility between build and runtime environments.
- Keep pull requests focused on one concern. Cover behavior introduced by the pull request, and put unrelated coverage improvements in a separate pull request.

## Tools and workspace

- Use the configured environment and tool managers. Do not install substitute environments without approval.
- Use the authenticated host `gh` for live GitHub state.
- Preserve unexpected staged, unstaged, and untracked user work.

## Git and review

- Follow Conventional Commits and do not add co-author trailers.
- Before publishing, run local checks and manually review the complete diff.
- Fix and validate all known findings before requesting a CodeRabbit review.
- Evaluate every review finding. Fix valid findings, explain rejected findings, and resolve adjudicated threads.
- Confirm that completed reviews apply to the current commit. Do not merge with unresolved actionable findings.
- Do not push, force-push, or open a pull request without explicit approval.

## Verification

- Start with focused tests, then run the full checks required by the change.
- Use containers for container-specific behavior and verify observable runtime behavior.
- Use mocks and dummy configuration for routine tests. Never expose private inputs.
- Report exact limitations when a check cannot run locally.
- Before pushing, run:

```bash
prek run --all-files
uv run --with pytest --with pytest-cov -- pytest --cov --cov-branch --cov-report=xml
```

- Hooks do not compare coverage. Check it separately and do not reduce coverage relative to `master`.

## Development commands

- `pdm install` - Install dependencies.
- `pdm run pytest` - Run tests.
- `prek run --all-files` - Run repository hooks.
- `ruff check` - Run the Python linter.
- `ruff format` - Format Python code.
- `pdm build` - Build the Python package.
- `docker build -t anata-no-minato .` - Build the container image.

## Architecture

- `src/sshconfig_to_ananta/ssh_config_converter.py` parses SSH configuration and Ananta `#tags` comments.
- `src/sshconfig_to_ananta/ananta_host.py` validates and serializes host records and relocates key paths.
- `src/sshconfig_to_ananta/main.py` owns the converter CLI and output handling.
- `docker-entrypoint.sh` parses Ananta arguments and generates a host file when needed.
- `script/dummy_ananta.sh` is the source for the downloadable host-side wrapper.
- `.github/workflows/ananta.yml` builds the image and wrapper release asset.
