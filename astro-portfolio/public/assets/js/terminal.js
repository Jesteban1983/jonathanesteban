// === TERMINAL INTERACTIVE — Multi-Language Code Typing with Tab Switching ===
// Click tabs to switch between Python, TypeScript, and SQL code demos

export function initTerminal() {
  const terminal = document.getElementById('heroTerminal');
  if (!terminal) return;

  const codeDisplay = terminal.querySelector('[data-terminal-code]');
  const tabs = terminal.querySelectorAll('[data-terminal-tab]');
  const statusItems = terminal.querySelectorAll('[data-terminal-status]');

  if (!codeDisplay || !tabs.length) return;

  // ─── Code datasets ───

  const datasets = {
    python: {
      status: 'Python 3.12.2',
      code: [
        { text: '# OpenClaw Autonomous Agent', type: 'comment' },
        { text: 'from openclaw import Agent, Tool', type: 'normal' },
        { text: 'from composio import ComposioMCP', type: 'normal' },
        { text: '', type: 'break' },
        { text: '# Initialize MCP server', type: 'comment' },
        { text: 'mcp = ComposioMCP(', type: 'normal' },
        { text: '    api_key=os.getenv("COMPOSIO_KEY")', type: 'indent' },
        { text: ')', type: 'normal' },
        { text: '', type: 'break' },
        { text: '# Tools: Gmail, Calendar, Supabase', type: 'comment' },
        { text: 'tools = [', type: 'normal' },
        { text: '    Tool("gmail", mcp),', type: 'indent' },
        { text: '    Tool("google_calendar", mcp),', type: 'indent' },
        { text: '    Tool("supabase_db", mcp),', type: 'indent' },
        { text: ']', type: 'normal' },
        { text: '', type: 'break' },
        { text: '# Agent config with Llama 3.3', type: 'comment' },
        { text: 'agent = Agent(', type: 'normal' },
        { text: '    model="llama-3.3-70b",', type: 'indent' },
        { text: '    tools=tools,', type: 'indent' },
        { text: '    max_iterations=10,', type: 'indent' },
        { text: '    verbose=True', type: 'indent' },
        { text: ')', type: 'normal' },
        { text: '', type: 'break' },
        { text: '# Run autonomous workflow', type: 'comment' },
        { text: 'agent.run(', type: 'normal' },
        { text: '    "Process emails, sync calendar, update DB"', type: 'indent' },
        { text: ')', type: 'normal' },
        { text: '', type: 'break' },
        { text: '# n8n webhook relay — event logged', type: 'comment' },
        { text: '>> Agent online · 3 tools connected', type: 'output' },
        { text: '>> Live session · 99.9% uptime', type: 'output' },
      ],
    },
    typescript: {
      status: 'Node.js v20.11',
      code: [
        { text: '// API Route: Webhook Handler (Next.js)', type: 'comment' },
        { text: 'import { NextRequest, NextResponse } from "next/server";', type: 'normal' },
        { text: 'import { createHmac } from "node:crypto";', type: 'normal' },
        { text: '', type: 'break' },
        { text: 'const QUEUE_URL = process.env.N8N_WEBHOOK_URL!;', type: 'normal' },
        { text: '', type: 'break' },
        { text: 'export async function POST(req: NextRequest) {', type: 'normal' },
        { text: '  const body = await req.json();', type: 'indent' },
        { text: '  const signature = createHmac("sha256", process.env.SECRET!)', type: 'indent' },
        { text: '    .update(JSON.stringify(body))', type: 'indent' },
        { text: '    .digest("hex");', type: 'indent' },
        { text: '', type: 'break' },
        { text: '  // Forward to n8n async job queue', type: 'comment' },
        { text: '  const response = await fetch(QUEUE_URL, {', type: 'indent' },
        { text: '    method: "POST",', type: 'indent' },
        { text: '    headers: { "Content-Type": "application/json" },', type: 'indent' },
        { text: '    body: JSON.stringify({ data: body, signature }),', type: 'indent' },
        { text: '  });', type: 'indent' },
        { text: '', type: 'break' },
        { text: '  if (!response.ok) {', type: 'indent' },
        { text: "    return NextResponse.json({ error: 'Queue failed' }, { status: 502 });", type: 'indent' },
        { text: '  }', type: 'indent' },
        { text: '', type: 'break' },
        { text: '  return NextResponse.json({ queued: true, latency: "24ms" });', type: 'indent' },
        { text: '}', type: 'normal' },
        { text: '', type: 'break' },
        { text: '>> Webhook active · queue: n8n', type: 'output' },
        { text: '>> Avg latency: 24ms · 200 OK', type: 'output' },
      ],
    },
    sql: {
      status: 'PostgreSQL 16.2',
      code: [
        { text: '-- Schema: Semantic Search with pgvector', type: 'comment' },
        { text: 'CREATE EXTENSION IF NOT EXISTS vector;', type: 'normal' },
        { text: '', type: 'break' },
        { text: '-- Documents table with embeddings', type: 'comment' },
        { text: 'CREATE TABLE documents (', type: 'normal' },
        { text: '  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),', type: 'indent' },
        { text: '  title TEXT NOT NULL,', type: 'indent' },
        { text: '  content TEXT,', type: 'indent' },
        { text: '  embedding VECTOR(1536),', type: 'indent' },
        { text: '  created_at TIMESTAMPTZ DEFAULT NOW()', type: 'indent' },
        { text: ');', type: 'normal' },
        { text: '', type: 'break' },
        { text: '-- IVFFlat index for semantic search', type: 'comment' },
        { text: 'CREATE INDEX idx_doc_embedding', type: 'normal' },
        { text: '  ON documents', type: 'indent' },
        { text: '  USING ivfflat (embedding vector_cosine_ops)', type: 'indent' },
        { text: '  WITH (lists = 100);', type: 'indent' },
        { text: '', type: 'break' },
        { text: '-- Similarity search query', type: 'comment' },
        { text: 'SELECT title, content,', type: 'normal' },
        { text: '       1 - (embedding <=> $1) AS similarity', type: 'indent' },
        { text: 'FROM documents', type: 'normal' },
        { text: 'ORDER BY embedding <=> $1', type: 'normal' },
        { text: 'LIMIT 10;', type: 'normal' },
        { text: '', type: 'break' },
        { text: '>> pgvector ready · 1536d index', type: 'output' },
        { text: '>> Semantic search: ~8ms avg', type: 'output' },
      ],
    },
  };

  // ─── Typing state ───
  let currentLang = 'python';
  let lineIndex = 0;
  let charIndex = 0;
  let currentLineElement = null;
  let typingInterval = null;
  let restartTimeout = null;
  let isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ─── Syntax highlighting ───

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function highlightLine(lineDef) {
    let text = lineDef.text;
    if (lineDef.type === 'indent') text = '  ' + text;

    if (lineDef.type === 'break') return '&nbsp;';
    if (lineDef.type === 'comment') return `<span class="tk-comment">${escapeHtml(text)}</span>`;
    if (lineDef.type === 'output') return `<span class="tk-output">${escapeHtml(text)}</span>`;

    let html = escapeHtml(text);
    // Python / general keywords
    html = html.replace(/\b(from|import|def|return|class|if|elif|else|for|while|try|except|with|as|async|await|True|False|None)\b/g, '<span class="tk-keyword">$1</span>');
    // Strings
    html = html.replace(/"([^"]*)"/g, '<span class="tk-string">"$1"</span>');
    html = html.replace(/'([^']*)'/g, "<span class='tk-string'>'$1'</span>");
    // Function calls
    html = html.replace(/\b(\w+)(\()/g, '<span class="tk-fn">$1</span>$2');
    // Decorators
    html = html.replace(/(@\w+)/g, '<span class="tk-decorator">$1</span>');
    // Numbers
    html = html.replace(/\b(\d+\.?\d*)\b/g, '<span class="tk-number">$1</span>');
    // TS/JS keywords
    html = html.replace(/\b(const|let|var|function|export|import|async|await|if|else|return|interface|type|typeof|new)\b/g, '<span class="tk-keyword">$1</span>');
    // SQL keywords (case-insensitive)
    html = html.replace(/\b(CREATE|TABLE|SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|INDEX|VECTOR|EXTENSION|NOT|NULL|PRIMARY|KEY|REFERENCES|ON|CASCADE|FOREIGN|LIMIT|ORDER|BY|AS|DEFAULT|USING|WITH|IF)\b/g, '<span class="tk-keyword">$1</span>');

    return html;
  }

  // ─── Full render (for reduced motion) ───

  function renderFull(lang) {
    codeDisplay.innerHTML = '';
    const lines = datasets[lang].code;
    lines.forEach(line => {
      const div = document.createElement('div');
      div.className = 'terminal-line';
      div.innerHTML = highlightLine(line);
      codeDisplay.appendChild(div);
    });
  }

  // ─── Typing via setInterval ───

  function stopTyping() {
    if (typingInterval) {
      clearInterval(typingInterval);
      typingInterval = null;
    }
    if (restartTimeout) {
      clearTimeout(restartTimeout);
      restartTimeout = null;
    }
  }

  function typeChar() {
    try {
      const lines = datasets[currentLang].code;

      // If we finished all lines, restart after a pause
      if (lineIndex >= lines.length) {
        stopTyping();
        // Add blinking cursor at the end
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        codeDisplay.appendChild(cursor);
        restartTimeout = setTimeout(() => startTyping(currentLang), 4000);
        return;
      }

      const line = lines[lineIndex];

      // Create a new line element when starting a line
      if (charIndex === 0) {
        const div = document.createElement('div');
        div.className = 'terminal-line';
        codeDisplay.appendChild(div);
        currentLineElement = div;
      }

      const fullText = line.type === 'indent' ? '  ' + line.text : line.text;

      if (line.type === 'break') {
        // Empty line — just add a blank line
        if (currentLineElement) {
          currentLineElement.innerHTML = '&nbsp;';
        }
        lineIndex++;
        charIndex = 0;
        currentLineElement = null;
        // Remove any cursor
        const c = codeDisplay.querySelector('.typing-cursor');
        if (c) c.remove();
        return;
      }

      // Type the next character
      charIndex++;
      const typed = fullText.substring(0, charIndex);

      if (currentLineElement) {
        // Build highlighted HTML for the typed portion
        const highlighted = highlightLine({ ...line, text: typed });
        // Append blinking cursor
        currentLineElement.innerHTML = highlighted + '<span class="typing-cursor"></span>';

        // Remove cursor from previous line
        const prev = currentLineElement.previousElementSibling;
        if (prev) {
          const c = prev.querySelector('.typing-cursor');
          if (c) c.remove();
        }
      }

      // Scroll to bottom
      codeDisplay.scrollTop = codeDisplay.scrollHeight;

      // If line is complete, advance
      if (charIndex >= fullText.length) {
        lineIndex++;
        charIndex = 0;
        currentLineElement = null;
      }
    } catch (e) {
      // On error, restart
      stopTyping();
      setTimeout(() => startTyping(currentLang), 2000);
    }
  }

  function startTyping(lang) {
    stopTyping();
    currentLang = lang;
    lineIndex = 0;
    charIndex = 0;
    currentLineElement = null;
    codeDisplay.innerHTML = '';
    // Type one character every 35ms (~28 chars/sec) — clearly visible
    typingInterval = setInterval(typeChar, 35);
  }

  // ─── Tab switching ───

  function switchTab(lang) {
    if (lang === currentLang && typingInterval) return;

    tabs.forEach(t => {
      t.classList.toggle('terminal-tab--active', t.dataset.terminalTab === lang);
    });

    statusItems.forEach(el => {
      el.textContent = datasets[lang].status;
    });

    if (isReducedMotion) {
      renderFull(lang);
    } else {
      startTyping(lang);
    }
  }

  // ─── Event binding ───

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      switchTab(tab.dataset.terminalTab);
    });
  });

  // ─── Initialization ───

  statusItems.forEach(el => {
    el.textContent = datasets.python.status;
  });

  if (isReducedMotion) {
    renderFull('python');
  } else {
    startTyping('python');
  }
}