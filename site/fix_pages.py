#!/usr/bin/env python3
"""Fix all HTML pages: add Google Fonts, Tailwind, skip-to-content, hamburger, mobile nav"""

import os, re

SITE = "/workspaces/jonathanesteban/site"

# Pages that already have tailwind/hamburger and don't need full fix
already_done = {
    "/workspaces/jonathanesteban/site/index.html",         # Home - already has everything
    "/workspaces/jonathanesteban/site/servicios/index.html",  # Already fixed
    "/workspaces/jonathanesteban/site/sobre-mi/index.html",   # Already fixed
}

# Pages that SHOULD NOT be touched (redirects, auth callbacks)
skip_pages = {
    "/workspaces/jonathanesteban/site/soporte-it/index.html",
}

pages = []
for root, dirs, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            if path not in already_done and path not in skip_pages:
                pages.append(path)

print(f"Found {len(pages)} pages to fix")

for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        content = f.read()

    # Already has tailwind? Skip
    if 'cdn.tailwindcss.com' in content:
        print(f"  SKIP (has tailwind): {page}")
        continue

    rel_path = os.path.relpath(page, SITE)
    print(f"  FIXING: {rel_path}")

    # 1. Add Google Fonts + Tailwind after the canonical link or description meta
    # Find </head> position
    head_end = content.find("</head>")
    if head_end == -1:
        print(f"    ERROR: no </head> found")
        continue

    head_part = content[:head_end]
    body_part = content[head_end:]

    # Insert fonts + tailwind before the last CSS link or before </head>
    css_links = ['<link rel="stylesheet" href="/assets/css/tokens.css"']
    for cl in css_links:
        idx = head_part.find(cl)
        if idx != -1:
            # Insert before this link
            insert = (
                '  <!-- Google Fonts -->\n'
                '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">\n'
                '\n'
                '  <!-- Tailwind CSS -->\n'
                '  <script src="https://cdn.tailwindcss.com"></script>\n'
                '\n'
            )
            head_part = head_part[:idx] + insert + head_part[idx:]
            break

    # 2. Add skip-to-content link
    body_open = head_part.rfind("<body")
    if body_open == -1:
        body_close = head_part.rfind(">")
        if body_close == -1:
            continue
        # find the next < after body tag
        rest = head_part[body_close+1:]
        skip = '\n  <a href="#main-content" class="sr-only-focusable">Saltar al contenido principal</a>'
        head_part = head_part[:body_close+1] + skip + rest
    else:
        close_brace = head_part.find(">", body_open)
        if close_brace != -1:
            skip = '\n  <a href="#main-content" class="sr-only-focusable">Saltar al contenido principal</a>'
            head_part = head_part[:close_brace+1] + skip + head_part[close_brace+1:]

    # 3. Add hamburger menu button (if not present)
    if 'hamburger-btn' not in head_part:
        # Find theme-toggle-btn area
        theme_btn_end = head_part.rfind('aria-label="Cambiar tema"')
        if theme_btn_end != -1:
            line_end = head_part.find("\n", theme_btn_end)
            if line_end != -1:
                hamburger = '\n        <button class="hamburger-btn" id="hamburger" aria-label="Abrir menú" aria-expanded="false">\n          <span></span><span></span><span></span>\n        </button>'
                head_part = head_part[:line_end] + hamburger + head_part[line_end:]

    # 4. Add mobile nav drawer (if not present)
    if 'nav-mobile' not in head_part and 'mobileNav' not in head_part:
        # Find where the header nav ends (after nav-actions div close)
        nav_actions_end = head_part.rfind('</div>')
        if nav_actions_end != -1:
            second_last_div = head_part.rfind('</div>', 0, nav_actions_end)
            if second_last_div != -1:
                mobile_nav = (
                    '\n\n  <!-- Mobile Nav Drawer -->\n'
                    '  <nav class="nav-mobile" id="mobileNav" aria-label="Menú móvil">\n'
                    '    <a href="/servicios/">Servicios & Presupuesto</a>\n'
                    '    <a href="/proyectos/">Proyectos & Casos</a>\n'
                    '    <a href="/certificaciones/">Certificaciones</a>\n'
                    '    <a href="/sobre-mi/">Sobre Mí</a>\n'
                    '    <a href="/faq/">Preguntas Frecuentes</a>\n'
                    '    <a href="/contacto/">Contacto</a>\n'
                    '  </nav>'
                )
                # Insert after the last </div> which closes header
                head_part = head_part[:second_last_div] + head_part[second_last_div:]
                # Find the header close </header>
                header_close = head_part.rfind("</header>")
                if header_close != -1:
                    head_part = head_part[:header_close] + mobile_nav + "\n  " + head_part[header_close:]

    # Reassemble
    content = head_part + body_part

    with open(page, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"    ✅ Fixed")

print("\nDone!")