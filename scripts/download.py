#!/usr/bin/env python3
"""Download the MTP drafter (and optionally the 6-bit target model) from Hugging Face."""
import argparse
from huggingface_hub import snapshot_download

DRAFTER = "VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-MLX-MTP-Drafter"
TARGET = "VisualInference/Qwen3.8-27B-AEON-Ultimate-Uncensored-Multimodal-MLX-6bit"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", action="store_true", help="also download the 6-bit target model")
    p.add_argument("--local-dir", default=None, help="write to this directory instead of the HF cache")
    a = p.parse_args()

    repos = [DRAFTER] + ([TARGET] if a.target else [])
    for repo in repos:
        dest = None if a.local_dir is None else f"{a.local_dir}/{repo.split('/')[-1]}"
        path = snapshot_download(repo, local_dir=dest)
        print(f"{repo}\n  -> {path}")


if __name__ == "__main__":
    main()
