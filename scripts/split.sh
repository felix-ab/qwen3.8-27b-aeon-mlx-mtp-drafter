#!/usr/bin/env bash
# Split recipe used to produce the released drafter.
# Requires mlx-vlm with the qwen3_5_mtp drafter tooling and access to the base repository.
set -euo pipefail
python -m mlx_vlm.speculative.drafters.qwen3_5_mtp.split \
  --model AEON-7/Qwen3.8-27B-AEON-ULTIMATE-UNCENSORED-BF16 \
  --output Qwen3.8-27B-AEON-Ultimate-MLX-MTP-Drafter
