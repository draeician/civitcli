# Civitai CLI Tool - MVP PRD (v0.1)

## 1. Purpose & Scope

**Purpose:**
A Python-based CLI utility that takes metadata from a Civitai “Generation data” block (or equivalent structured JSON) and outputs:

* A working **Stable Diffusion CLI command** compatible with `stable-diffusion.cpp`.
* The ability to **download resources from a provided URL** (e.g., model checkpoint, LoRA, embedding) directly from Civitai.

This tool reduces human error, automates repetitive tasks, and simplifies integrating Civitai assets into scriptable Stable Diffusion workflows.

**Scope:**

* CLI-only utility (no GUI/web interface)
* Works with `stable-diffusion.cpp` only
* Initial support for checkpoint and LoRA usage
* Direct download from URL provided by the user
* Does **not** execute diffusion inference itself

---

## 2. Stakeholders & Users

* **Prompt Engineers & Hobbyists:** Quickly convert Civitai metadata into runnable commands.
* **DevOps / Automation:** Integrate into batch jobs or pipelines.
* **LLM / Codex Agents:** Use the CLI as part of automated generation pipelines.

---

## 3. Features & Requirements

### 3.1 CLI Interface (Core)

| Flag / Argument      | Description                                                                    |
| -------------------- | ------------------------------------------------------------------------------ |
| `--download <URL>`   | Download a model, LoRA, or embedding from a provided Civitai URL.              |
| `--render`           | Parse generation metadata and emit a working `stable-diffusion.cpp` command.   |
| `-v` / `--verbose`   | Add verbose flag to generated command.                                         |
| `-V` / `--version`   | Output the tool version and exit.                                              |
| Input (stdin / file) | Accept a Civitai “Generation data” block or structured JSON metadata as input. |

---

### 3.2 Download Functionality (MVP Priority)

The first deliverable must be the download feature.

* Accept a **direct download URL** from the user.
* Perform the download automatically using Python (`requests` or `httpx`).
* Support authentication with `$CIVITAI_API` if present in the environment.
* Validate download success, handle errors gracefully, and display meaningful messages.
* Save files to the configured model directory by type:

  * Checkpoints → `/opt/md2/backup/civitai/models`
  * LoRAs → `/opt/md2/backup/civitai/models/loras`
  * Embeddings → `/opt/md2/backup/civitai/models/embeddings`

Future enhancement: resolve a **model page URL** into the direct download link automatically.

---

### 3.3 Generation Data Parsing & Command Generation

* Parse Civitai “Generation data” blocks:

  * Positive / negative prompts
  * Steps, sampler, CFG, seed, size, clip skip
  * Base model and “Resources used” lines
* Map sampler names to `--sampling-method` (and optional `--scheduler`)
* Detect model family (SD1.x vs SDXL)
* Auto-enable `--vae-tiling` if width or height ≥ 1024
* Generate:

  ```bash
  ./sd -m /opt/md2/backup/civitai/models/<model>.safetensors \
      -p "<prompt>" -n "<negative>" \
      --steps 30 --cfg-scale 7 --seed 123456 \
      -W 1024 -H 1024 --clip-skip 2 \
      --sampling-method euler_a --vae-tiling \
      -o <uuid>-<timestamp>.png
  ```
* Properly escape prompt strings for shell safety.
* Include warnings if:

  * Sampler not recognized (fallback to `euler_a`)
  * Model family mismatches resources
  * VAE tiling required but not enabled

---

### 3.4 Configuration & Defaults

* Default paths:

  * Models: `/opt/md2/backup/civitai/models`
  * LoRAs: `/opt/md2/backup/civitai/models/loras`
  * Embeddings: `/opt/md2/backup/civitai/models/embeddings`
* Default output filename: `<uuid>-<timestamp>.png`
* Override defaults via environment variables or config file.

---

## 4. Non-Functional Requirements

* **Language:** Python 3.10+
* **Dependencies:** Minimal (`argparse`, `requests`/`httpx`, `uuid`, `datetime`, `re`)
* **Security:** Proper shell escaping to avoid injection.
* **Maintainability:** Modular design (parsing, mapping, downloading, rendering).
* **Extensibility:** Architected to support future backends and Civitai page resolution.

---

## 5. MVP Milestones & Deliverables

### Milestone 1 – Download Capability (v0.1.0)

* [ ] Implement `--download <URL>`
* [ ] Python-based download system
* [ ] Auth support with `$CIVITAI_API`
* [ ] Basic error handling and validation

### Milestone 2 – Generation Block Parsing (v0.1.1)

* [ ] Parse Civitai metadata block from stdin/file
* [ ] Extract prompt, sampler, steps, size, etc.
* [ ] Implement sampler mapping and fallback logic
* [ ] Add model family detection

### Milestone 3 – Command Generation (v0.1.2)

* [ ] Build full `stable-diffusion.cpp` command
* [ ] Implement shell-safe escaping
* [ ] Add `--vae-tiling` logic
* [ ] Generate UUID + timestamp filenames
* [ ] Support `-v` and `-V` flags

### Milestone 4 – Configuration & Defaults (v0.1.3)

* [ ] Default path support
* [ ] Config file & environment overrides
* [ ] Notes and warnings output

### Milestone 5 – Testing & Documentation (v0.1.4)

* [ ] Unit tests for sampler mapping & prompt parsing
* [ ] Integration tests for end-to-end workflow
* [ ] README with examples and usage patterns
* [ ] Troubleshooting guide

---

## 6. Deferred Features (Post-MVP)

* LoRA and embedding injection into prompts
* File existence validation for LoRAs/embeddings
* Civitai page → download URL auto-resolution
* Resume/retry for interrupted downloads
* Backend plugin support (AUTOMATIC1111, InvokeAI)
* Plugin architecture for extensibility

