# Qwen3.8-27B-AEON — MTP Drafter (MLX)

The native multi-token-prediction (MTP) head of [AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-BF16](https://huggingface.co/AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-BF16) (revision `8f76e82`), split into the standalone drafter format that mlx-vlm expects for `mtp` speculative decoding.

**Weights:** [huggingface.co/VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-MLX-MTP-Drafter](https://huggingface.co/VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-MLX-MTP-Drafter)
**Companion target model:** [qwen3.8-27b-aeon-mlx-6bit](https://github.com/felix-ab/qwen3.8-27b-aeon-mlx-6bit)

This repository holds the documentation, split recipe and helper scripts. The weights (810 MB) are distributed through Hugging Face and are not tracked here.

## Overview

| Property | Value |
|---|---|
| Contents | 15 tensors, BF16 |
| Size | 810 MB |
| Block size | 3 |
| Origin | The original Qwen-trained MTP head, not retrained |
| Compatible targets | Any MLX quantization of the same base model |
| License | Apache-2.0, inherited from the base model |

AEON's BF16 release grafts the MTP head back from stock Qwen3.8 with hash-matched tensors. The drafter distributed here is therefore the head Qwen trained, unchanged.

Speculative decoding with this drafter is lossless. Rejected drafts fall back to the target model's own tokens, and the output distribution is unchanged by construction.

## Requirements

- An Apple Silicon Mac with `mlx-vlm` installed.
- A compatible target model, for example the [6-bit multimodal quantization](https://huggingface.co/VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-Multimodal-MLX-6bit).

## Installation

```bash
pip install -U mlx-vlm huggingface_hub
python scripts/download.py          # fetches the drafter
python scripts/download.py --target # also fetches the 6-bit target model
```

## Usage

```bash
python -m mlx_vlm generate \
  --model VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-Multimodal-MLX-6bit \
  --draft-model VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-MLX-MTP-Drafter \
  --draft-kind mtp --draft-block-size 3 \
  --prompt "..."
```

Block size 3 is the general-purpose setting. Block size 4 is marginally better on code. Block sizes of 5 or more regress, since draft accuracy decays beyond two to three tokens.

## Measured effect

Test machine: Mac mini M4 Pro, 48 GB unified memory, with the companion 6-bit target model. The drafter's relative overhead is small, so the speedups carry across chips.

| Workload | Serial | With drafter |
|---|---|---|
| Coding (temp 0.2, block 4) | 11.4 tok/s | 21.5 tok/s (1.90×) |
| Document QA at 13k context (block 3) | ~11 tok/s | 16.9 tok/s |
| Creative prose (temp 0.7, block 3) | 11.4 tok/s | 15.9 tok/s (1.4×) |

Draft acceptance is approximately 46% on open-ended prose and higher on structured output.

## How it was made

See `scripts/split.sh`.

```bash
python -m mlx_vlm.speculative.drafters.qwen3_5_mtp.split \
  --model AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-BF16 \
  --output Qwen3.8-27B-AEON-Ultimate-Uncensored-MLX-MTP-Drafter
```

Use the official split tool. Extracting the `mtp.*` tensors by hand produces a broken drafter with 0% acceptance: the tool applies the RMSNorm weight-convention shift and stamps the `format: mlx` metadata that mlx-vlm requires.

## Files

| Path | Purpose |
|---|---|
| `scripts/download.py` | Fetch the weights from Hugging Face |
| `scripts/split.sh` | The split recipe used to produce the release |
| `LICENSE` | Apache-2.0 |
