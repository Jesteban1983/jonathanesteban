#!/usr/bin/env python3
"""list-drafts.py — Lista drafts como JSON para consumo por n8n.

Uso:
  python3 list-drafts.py <drafts_dir>
"""

import json
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"drafts": []}))
        return

    drafts_dir = Path(sys.argv[1])
    if not drafts_dir.is_dir():
        print(json.dumps({"drafts": []}))
        return

    drafts = []
    for f in sorted(drafts_dir.glob("*.mdx")):
        content = f.read_text(encoding="utf-8")
        title = ""
        m = re.search(r'^title:\s*["\'](.+?)["\']', content, re.M)
        if m:
            title = m.group(1)
        drafts.append({
            "slug": f.stem,
            "title": title,
            "path": str(f)
        })

    print(json.dumps({"drafts": drafts}, ensure_ascii=False))


if __name__ == "__main__":
    main()