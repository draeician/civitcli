# Civitai CLI MVP Implementation Plan

## Overview
This plan decomposes the requirements from `PRD.md` into incremental engineering tasks. The sequencing favours early delivery of the download capability and isolates features to reduce merge conflicts between contributors. Every milestone is scoped so that it can be developed, reviewed, and released independently. The package will be distributed via `pipx install`, so each milestone includes packaging considerations to keep the CLI entry point stable.

## Guiding Principles
- **Single-responsibility milestones:** Ship one major capability per milestone to avoid overlapping edits.
- **Stable public interface:** Reserve `civitcli` as the console script name from the first release to minimise downstream churn.
- **Config-driven paths:** Centralise configuration (default directories, environment overrides) so new resource types only touch one module.
- **pipx-first distribution:** Ensure `pyproject.toml` and minimal dependencies are in place from Milestone 0 so each feature branch can be installed with `pipx install .` for testing.
- **Test scaffolding early:** Introduce the test harness during Milestone 1 to keep later milestones focused on feature logic instead of plumbing.

## Milestone 0 – Project Scaffolding (v0.0.1)
*Purpose: establish the repository skeleton so feature work can proceed in parallel.*

### Deliverables
- `pyproject.toml` with CLI entry point (`civitcli = civitcli.__main__:main`).
- `civitcli/` package with placeholder modules:
  - `__init__.py` for version metadata.
  - `__main__.py` delegating to a `cli` module.
  - `cli.py` defining the `argparse` interface skeleton.
  - `config.py` for default paths and environment overrides.
  - `downloader.py` (stub) and `renderer/` package (stubs for parsing/command generation).
- `tests/` directory with `pytest` configured and one smoke test ensuring CLI responds to `--help`.
- Documentation updates:
  - `README.md` stub describing pipx installation (`pipx install git+https://...`).
  - `CONTRIBUTING.md` outlining branch strategy and testing commands.

### Task Breakdown
1. Author `pyproject.toml` (set version `0.0.1`, dependencies, `project.scripts`).
2. Create package directory structure with placeholder functions returning `NotImplementedError`.
3. Implement `cli.main()` parsing basic flags (`--download`, `--render`, `-v`, `-V`) without behaviour.
4. Add version constant to `__init__.py` and make `--version` display it.
5. Configure `pytest` in `pyproject.toml` and add a smoke test invoking CLI via `subprocess`.
6. Document setup and pipx installation instructions in `README.md`.

## Milestone 1 – Download Capability (v0.1.0)
*Purpose: deliver the MVP download feature while keeping parsing stubs for future work.*

### Deliverables
- Implement `downloader.py` with:
  - `download_resource(url: str, session: Optional[requests.Session]) -> Path`.
  - Authentication via `CIVITAI_API` header when present.
  - Resource type inference (checkpoint / LoRA / embedding) from URL or filename suffix.
  - File saving into default directories from `config.py` (create directories as needed).
  - Structured result object carrying save path and metadata for future use.
- Update CLI to execute download when `--download` is provided.
- Verbose logging toggle (`-v`) controlling log level.
- Error handling with user-friendly messages and non-zero exit codes on failure.
- Unit tests using `responses` or `pytest-httpx` fixtures to mock downloads.
- README usage examples for download flow.

### Task Breakdown
1. Finalise resource type mapping logic (suffixes `.safetensors`, `.ckpt`, `.pt`, `.bin`, `.zip`).
2. Implement HTTP client wrapper applying authentication header.
3. Write download function with stream-to-file handling and checksum placeholder.
4. Extend CLI with `--download` execution path and logging setup.
5. Add tests for success, authentication, and error cases.
6. Document environment variables (`CIVITAI_API`) and directory layout.

## Milestone 2 – Generation Data Parsing (v0.1.1)
*Purpose: translate Civitai metadata into structured objects.*

### Deliverables
- New module `renderer/parser.py` responsible for parsing JSON and text blocks.
- Data classes (`PromptData`, `GenerationSettings`, `ResourceReference`).
- Input handling: read from stdin, file path argument, or `--input` flag.
- Sampler mapping table and warnings for unknown samplers.
- Detection of model family (SD1.x, SDXL) based on metadata cues.
- Unit tests covering parsing variations and malformed input.
- CLI integration to parse input when `--render` is passed (still stub command output).

### Task Breakdown
1. Define parsing entry point accepting raw string and returning dataclasses.
2. Implement JSON detection vs. plain text parsing using regex.
3. Populate sampler mapping dictionary and fallback.
4. Hook parser into CLI with `--render` flow that prints parsed structure (temporary).
5. Write tests for positive/negative prompts, sampler detection, dimension parsing.
6. Update documentation with input examples.

## Milestone 3 – Command Generation (v0.1.2)
*Purpose: output executable `stable-diffusion.cpp` commands from parsed data.*

### Deliverables
- `renderer/command_builder.py` module constructing command arguments list.
- Shell-safe escaping using `shlex.quote`.
- VAE tiling logic when width/height ≥ 1024.
- Output file naming `<uuid>-<timestamp>.png` (configurable via `config.py`).
- Verbose flag appended to generated command when requested.
- CLI prints final command or writes to file (future-proof).
- Integration tests verifying command string given fixture metadata.

### Task Breakdown
1. Implement `build_command(parsed_data, config, verbose=False)` returning list/str.
2. Add utilities for uuid/timestamp generation and override via env vars.
3. Insert warnings for sampler fallback, model family mismatch, missing VAE tiling.
4. Update CLI `--render` path to call builder and print command.
5. Extend tests to cover tiling logic, verbose flag, negative prompt escaping.
6. Document usage examples in README.

## Milestone 4 – Configuration & Defaults (v0.1.3)
*Purpose: centralise configuration overrides and surface warnings.*

### Deliverables
- Expand `config.py` to read environment variables and optional `~/.config/civitcli/config.toml`.
- Provide dataclass `AppConfig` consumed by downloader and renderer modules.
- Implement warning system (e.g., `logging` warnings or structured output) for mismatches.
- Add tests covering configuration precedence (defaults < env < config file).
- Documentation for configuration file format and default paths.

### Task Breakdown
1. Define config dataclass and loader functions.
2. Implement TOML parsing with graceful fallback when file absent.
3. Refactor downloader and renderer to accept `AppConfig` instead of module globals.
4. Add logging configuration to central place.
5. Write tests verifying overrides and directory creation.
6. Update README/CONTRIBUTING with configuration guidance.

## Milestone 5 – Testing & Documentation (v0.1.4)
*Purpose: polish project for public consumption.*

### Deliverables
- Expand unit tests for sampler mapping, prompt parsing, and command building edge cases.
- Add integration test running CLI end-to-end with sample metadata and mocked download.
- Write `docs/usage.md` with scenarios and troubleshooting section.
- Ensure README includes badges, changelog link, and pipx installation command.
- Set up GitHub Actions workflow for lint/test (if repository supports CI).

### Task Breakdown
1. Identify coverage gaps and add targeted tests.
2. Create integration test harness using temporary directories.
3. Draft documentation pages (usage, troubleshooting).
4. Introduce `CHANGELOG.md` following Keep a Changelog format.
5. Add or update CI configuration (GitHub Actions) invoking `pytest`.

## Cross-cutting Concerns
- **Versioning:** Increment `civitcli.__version__` and `pyproject.toml` per milestone.
- **Logging:** Use Python `logging` module with CLI switch for verbosity.
- **Error Handling:** Custom exception hierarchy (e.g., `CivitCLIError`) to standardise exit codes.
- **Dependency Management:** Keep dependencies minimal; prefer stdlib unless PRD mandates otherwise.
- **pipx Compatibility:** Ensure no optional dependencies require system-wide installs; document `pipx install .` and `pipx run civitcli --help` for validation.

## Task Coordination Tips
- Developers working on different milestones should branch from latest main and limit edits to their module to prevent merge conflicts.
- Shared assets (config, cli) should expose extension points (e.g., function hooks) instead of direct modifications where possible.
- Use feature flags or stub implementations to unblock parallel work without merging incomplete features into main.

## Next Steps
1. Approve this implementation plan with stakeholders.
2. Begin Milestone 0 scaffolding on a dedicated branch.
3. Verify pipx installation (`pipx install .`) using the scaffold before starting feature development.
