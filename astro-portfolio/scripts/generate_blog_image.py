#!/usr/bin/env python3
"""Blog-specific wrapper around the shared IA-ENGINEERING-LAB image generator."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[4]
SHARED_GENERATOR = LAB_ROOT / "tools" / "gemini-image" / "generate_image.py"
BLOG_STYLE = (
    "Premium editorial photograph for a technology support blog. Contemporary 2026 hardware, "
    "calm Mediterranean workspace, natural soft morning light, full-frame 35mm photography, "
    "sharp subject and subtle depth of field. Main subject on the right two-thirds; clean darker "
    "negative space on the left for title overlay. Restrained deep petrol teal (#0D3C46) shadows "
    "and one small amber (#F2A72A) accent. Realistic, tasteful and uncluttered. No text, letters, "
    "numbers, logos, watermarks, brand names, recognizable faces, stock clichés, cartoon style, "
    "hacker imagery, obsolete hardware, excessive glow, oversaturation or malformed objects."
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="article slug, e.g. ordenador-lento")
    parser.add_argument("--scene", required=True, help="specific scene description, preferably in English")
    parser.add_argument("--output", type=Path, help="optional output path; defaults to public/assets/img/blog/<slug>.png")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("slug must contain lowercase ASCII letters, digits, and hyphens only")
    if not SHARED_GENERATOR.is_file():
        print(f"Shared image generator not found: {SHARED_GENERATOR}", file=sys.stderr)
        return 2

    project_root = Path(__file__).resolve().parents[1]
    output = args.output or Path("public/assets/img/blog") / f"{args.slug}.png"
    if not output.is_absolute():
        output = project_root / output
    prompt = f"Specific scene: {args.scene.strip()}\n\nBlog visual direction: {BLOG_STYLE}"
    command = [
        sys.executable,
        str(SHARED_GENERATOR),
        prompt,
        "--output",
        str(output),
        "--aspect-ratio",
        "16:9",
        "--format",
        "png",
        "--size",
        "2K",
        "--min-width",
        "1600",
        "--min-height",
        "900",
    ]
    return subprocess.run(command, cwd=project_root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
