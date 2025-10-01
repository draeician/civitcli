# Civitai CLI (MVP)

`civitcli` is a command-line utility that helps you manage assets from [Civitai](https://civitai.com) and generate
`stable-diffusion.cpp` commands from the platform's metadata blocks. The project is in active development, and this
milestone provides the initial package scaffolding.

## Installation

The CLI is designed for use with [pipx](https://pipx.pypa.io/). To install directly from a git checkout:

```bash
pipx install git+https://github.com/your-org/civitcli.git
```

During development you can run the tool in-place:

```bash
pipx run --spec . civitcli --help
```

## Usage

This milestone focuses on the CLI interface scaffolding. Run the command below to explore the available options:

```bash
civitcli --help
```

Future milestones will enable downloading Civitai resources and rendering `stable-diffusion.cpp` commands.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
