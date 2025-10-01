# Civitai CLI (MVP)

`civitcli` is a command-line utility that helps you manage assets from [Civitai](https://civitai.com) and generate
`stable-diffusion.cpp` commands from the platform's metadata blocks. The project is in active development, and this
milestone delivers the first iteration of the download workflow.

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

Run the command below to explore the available options:

```bash
civitcli --help
```

### Downloading resources

Provide a direct Civitai download URL to fetch a checkpoint, LoRA, or embedding. Files are saved into the default
directories defined in the [PRD](PRD.md):

```bash
civitcli --download "https://civitai.com/api/download/models/<model-id>"
```

If you have a Civitai API token, expose it via the `CIVITAI_API` environment variable. The CLI forwards the value as an
HTTP header for authenticated downloads:

```bash
export CIVITAI_API="your-api-token"
civitcli --download "https://civitai.com/api/download/models/<model-id>"
```

Use the `-v` flag for progress information, and increase verbosity with `-vv` when diagnosing issues.

Rendering `stable-diffusion.cpp` commands will arrive in a future milestone.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
