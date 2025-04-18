# Fuzzing Prompt Injection Tool

A Python-based script for using LLMs to automate fuzzing of prompt‑injection attacks against a locally hosted LLM model via the Ollama CLI.

## Table of Contents

- [Fuzzing Prompt Injection Tool](#fuzzing-prompt-injection-tool)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Customization](#customization)
  - [Results Interpretation](#results-interpretation)

## Overview

This tool first generates a set number of “injection” prompts—each crafted according to different methods (Ignore Instructions, Role Play, Comment Injection, etc.)—via your chosen prompt‑generation model. It then feeds each generated prompt back into a defensive instance of the same (or a different) model to see if the secret credentials slip through. Results are summarized on-screen and dumped into a JSON file.

## Features

- **Balanced methods**: Evenly distributes prompt count across six injection styles plus “Other.”
- **Parallelism**: Uses `ThreadPoolExecutor` to generate and test prompts concurrently.
- **Progress bars**: Live feedback on generation and testing phases with `tqdm`.
- **Timing metrics**: Reports total time for generation and testing separately.
- **Structured output**: Prints a summary of “full,” “partial” (username‑only or password‑only), and “none” successes, and writes all results to JSON.

## Prerequisites

- **Python 3.8+**
- **Ollama CLI** (install via [https://ollama.com/download](https://ollama.com/download))
- **Models pulled locally** (e.g., `ollama pull llama3.2:1b`)
- **Python packages**:
  ```bash
  pip install ollama tqdm
  ```

## Installation

```bash
git clone https://github.com/YourUser/Prompt-Injection-Fuzzer.git
cd Prompt-Injection-Fuzzer
```

## Usage

1. **Ensure Ollama is running** (if needed):
   ```bash
   ollama run llama3.2:1b
   ```
2. **Run the fuzzer** (replace secrets and settings):
   ```bash
   python3 fuzz_prompt_injection.py \
     --num-prompts 350 \
     --workers 6 \
     --prompt-model llama3.2:1b \
     --fuzz-model llama3.2:1b \
     --username ctf_user \
     --password s3cr3t_flag \
     --output results/fuzz_results.json
   ```

## Customization

You can tweak behavior via CLI flags or by editing constants in the script:

- **CLI flags**
  - `--num-prompts` (int) – total prompts to generate (default `70`)
  - `--workers` (int) – number of threads used/LLM instances (default `4`)
  - `--prompt-model` (str) – model for prompt generation (default `llama3.2:1b`)
  - `--fuzz-model` (str) – model for injection testing (default `llama3.2:1b`)
  - `--username`/`--password` (str) – secrets under test (default `ctf_user`/`s3cr3t_flag`)
  - `--output` (str) – JSON filepath for results

- **In‑code constants**
  - `METHODS` – list of injection styles
  - `SPECS` – system‑message templates for each method
  - Progress‑bar settings

## Results Interpretation

At the end you’ll see a summary like:

```
Tested 350 prompts → 10 full, 5 username‑only partial, 2 password‑only partial, 333 none returned.
```

- **Full**: both username & password leaked.
- **Username‑only**: partial leak of username.
- **Password‑only**: partial leak of password.
- **None**: defensive model held both secrets.

All individual entries (with their method tags) are saved in your specified JSON file for further analysis.
