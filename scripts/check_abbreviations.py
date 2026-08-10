#!/usr/bin/env python3
"""Buscar abreviaturas seguidas de minúscula en el texto HTML."""
import re
import os

root = 'site'
for dirpath, _dirs, files in os.walk(root):
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(dirpath, f)
        with open(fp, encoding='utf-8') as fh:
            content = fh.read()
        # Remove script/style
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        for m in re.finditer(r'>([^<]+)<', content):
            text = m.group(1)
            # Find 'word. lowercase' where word is 1-4 chars (abbreviation pattern)
            for mm in re.finditer(r'[A-Za-z]{1,4}\. [a-z]', text):
                print(f'{os.path.relpath(fp)}: "{mm.group()[:60]}" in text="{text.strip()[:80]}"')