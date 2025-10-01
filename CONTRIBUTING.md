# Contributing to Civitai CLI

Thank you for your interest in improving `civitcli`! This document outlines the basic workflow for contributing to the
project during the early milestones.

## Getting Started

1. Fork and clone the repository.
2. Create a feature branch from the latest `main` branch.
3. Install development dependencies:

   ```bash
   pip install -e .[dev]
   ```

4. Run the test suite to verify your environment:

   ```bash
   pytest
   ```

## Development Guidelines

- Follow the milestones defined in `docs/implementation-plan.md` to keep work incremental.
- Write tests for new functionality and ensure `pytest` passes before opening a pull request.
- Use descriptive commit messages and reference the milestone you are addressing when possible.
- Keep the CLI entry point (`civitcli`) stable to preserve compatibility with pipx installations.

## Pull Request Process

1. Ensure your branch is up to date with `main`.
2. Provide a clear summary of your changes and any testing performed.
3. Request a review from a maintainer.
4. Address feedback promptly and keep the conversation in the pull request.

By contributing you agree to license your work under the repository's MIT License.
