// === TERMINAL STANDALONE — Self-executing, no ES6 modules ===
// Load as regular <script> (not type="module") right before </body>

(function() {
  'use strict';

  function initTerminal() {
    var terminal = document.getElementById('heroTerminal');
    if (!terminal) { console.log('Terminal: #heroTerminal not found'); return; }

    var codeDisplay = terminal.querySelector('[data-terminal-code]');
    var tabs = terminal.querySelectorAll('[data-terminal-tab]');
    var statusItems = terminal.querySelectorAll('[data-terminal-status]');

    if (!codeDisplay || !tabs.length) { console.log('Terminal: required elements missing'); return; }

    console.log('Terminal: found', tabs.length, 'tabs, initializing...');

    // ─── Code datasets ───
    var datasets = {
      python: {
        status: 'Python 3.12.2',
        code: [
          { text: '# OpenClaw Autonomous Agent', type: 'comment' },
          { text: 'from openclaw import Agent, Tool', type: 'normal' },
          { text: '', type: 'break' },
          { text: '# Initialize MCP server', type: 'comment' },
          { text: 'agent = Agent(model="llama-3.3-70b", verbose=True)', type: 'normal' },
          { text: '', type: 'break' },
          { text: '# Tools: Gmail, Calendar, Supabase', type: 'comment' },
          { text: 'agent.connect("gmail", mcp)', type: 'normal' },
          { text: 'agent.connect("google_calendar", mcp)', type: 'normal' },
          { text: '', type: 'break' },
          { text: '# Run autonomous workflow', type: 'comment' },
          { text: 'agent.run("Process emails, sync calendar")', type: 'normal' },
          { text: '', type: 'break' },
          { text: '>> Agent online · 3 tools active', type: 'output' },
          { text: '>> Live session · 99.9% uptime', type: 'output' },
        ],
      },
      typescript: {
        status: 'Node.js v20.11',
        code: [
          { text: '// Webhook Handler (Next.js)', type: 'comment' },
          { text: 'import { NextRequest, NextResponse } from "next/server";', type: 'normal' },
          { text: '', type: 'break' },
          { text: 'export async function POST(req: NextRequest) {', type: 'normal' },
          { text: '  const body = await req.json();', type: 'indent' },
          { text: '  const sig = process.env.SECRET;', type: 'indent' },
          { text: '', type: 'break' },
          { text: '  // Forward to n8n async queue', type: 'comment' },
          { text: '  const res = await fetch(process.env.N8N_URL, {', type: 'indent' },
          { text: '    method: "POST",', type: 'indent' },
          { text: '    headers: { "Content-Type": "application/json" },', type: 'indent' },
          { text: '    body: JSON.stringify({ data: body, sig })', type: 'indent' },
          { text: '  });', type: 'indent' },
          { text: '', type: 'break' },
          { text: '  return NextResponse.json({ queued: true });', type: 'indent' },
          { text: '}', type: 'normal' },
          { text: '', type: 'break' },
          { text: '>> Webhook active · avg 24ms', type: 'output' },
        ],
      },
      sql: {
        status: 'PostgreSQL 16.2',
        code: [
          { text: '-- Semantic Search with pgvector', type: 'comment' },
          { text: 'CREATE EXTENSION IF NOT EXISTS vector;', type: 'normal' },
          { text: '', type: 'break' },
          { text: 'CREATE TABLE documents (', type: 'normal' },
          { text: '  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),', type: 'indent' },
          { text: '  embedding VECTOR(1536),', type: 'indent' },
          { text: '  created_at TIMESTAMPTZ DEFAULT NOW()', type: 'indent' },
          { text: ');', type: 'normal' },
          { text: '', type: 'break' },
          { text: 'CREATE INDEX ON documents', type: 'normal' },
          { text: '  USING ivfflat (embedding vector_cosine_ops);', type: 'indent' },
          { text: '', type: 'break' },
          { text: '>> pgvector ready · ~8ms avg', type: 'output' },
        ],
      },
    };

    // ─── Typing state ───
    var currentLang = 'python';
    var lineIndex = 0;
    var charIndex = 0;
    var currentLineElement = null;
    var typingInterval = null;
    var restartTimeout = null;

    // ─── Escape HTML ───
    function escapeHtml(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // ─── Syntax highlighting (simplified) ───
    function highlightLine(lineDef) {
      var text = lineDef.text;
      if (lineDef.type === 'indent') text = '  ' + text;

      if (lineDef.type === 'break') return '&nbsp;';
      if (lineDef.type === 'comment') return '<span class="tk-comment">' + escapeHtml(text) + '</span>';
      if (lineDef.type === 'output') return '<span class="tk-output">' + escapeHtml(text) + '</span>';

      var html = escapeHtml(text);
      // Keywords
      html = html.replace(/\b(from|import|def|return|class|if|elif|else|for|while|try|except|async|await|True|False|None|const|let|var|function|export|interface|type|new|CREATE|TABLE|SELECT|INSERT|INTO|VALUES|UPDATE|DELETE|FROM|WHERE|INDEX|VECTOR|EXTENSION|PRIMARY|KEY|NOT|NULL|LIMIT|ORDER|BY|AS|DEFAULT|USING|WITH|IF|OR|AND|ON)\b/g, '<span class="tk-keyword">$1</span>');
      // Strings
      html = html.replace(/"([^"]*)"/g, '<span class="tk-string">"$1"</span>');
      html = html.replace(/'([^']*)'/g, "<span class='tk-string'>'$1'</span>");
      // Function calls
      html = html.replace(/\b(\w+)(\()/g, '<span class="tk-fn">$1</span>$2');
      // Numbers
      html = html.replace(/\b(\d+\.?\d*)\b/g, '<span class="tk-number">$1</span>');

      return html;
    }

    // ─── Full render (used for reduced motion) ───
    function renderFull(lang) {
      codeDisplay.innerHTML = '';
      var lines = datasets[lang].code;
      for (var i = 0; i < lines.length; i++) {
        var div = document.createElement('div');
        div.className = 'terminal-line';
        div.innerHTML = highlightLine(lines[i]);
        codeDisplay.appendChild(div);
      }
    }

    // ─── Stop typing ───
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

    // ─── Type one character ───
    function typeChar() {
      try {
        var lines = datasets[currentLang].code;

        if (lineIndex >= lines.length) {
          stopTyping();
          var cursor = document.createElement('span');
          cursor.className = 'typing-cursor';
          codeDisplay.appendChild(cursor);
          restartTimeout = setTimeout(function() { startTyping(currentLang); }, 4000);
          return;
        }

        var line = lines[lineIndex];

        if (charIndex === 0) {
          var div = document.createElement('div');
          div.className = 'terminal-line';
          codeDisplay.appendChild(div);
          currentLineElement = div;
        }

        var fullText = line.type === 'indent' ? '  ' + line.text : line.text;

        if (line.type === 'break') {
          if (currentLineElement) {
            currentLineElement.innerHTML = '&nbsp;';
          }
          lineIndex++;
          charIndex = 0;
          currentLineElement = null;
          var c = codeDisplay.querySelector('.typing-cursor');
          if (c) c.remove();
          return;
        }

        charIndex++;
        var typed = fullText.substring(0, charIndex);

        if (currentLineElement) {
          var highlighted = highlightLine({ text: typed, type: line.type });
          currentLineElement.innerHTML = highlighted + '<span class="typing-cursor"></span>';

          var prev = currentLineElement.previousElementSibling;
          if (prev) {
            var pc = prev.querySelector('.typing-cursor');
            if (pc) pc.remove();
          }
        }

        codeDisplay.scrollTop = codeDisplay.scrollHeight;

        if (charIndex >= fullText.length) {
          lineIndex++;
          charIndex = 0;
          currentLineElement = null;
        }
      } catch(e) {
        console.log('Terminal typing error:', e);
        stopTyping();
        setTimeout(function() { startTyping(currentLang); }, 2000);
      }
    }

    // ─── Start typing ───
    function startTyping(lang) {
      console.log('Terminal: starting typing for', lang);
      stopTyping();
      currentLang = lang;
      lineIndex = 0;
      charIndex = 0;
      currentLineElement = null;
      codeDisplay.innerHTML = '';
      typingInterval = setInterval(typeChar, 35);
    }

    // ─── Tab switching ───
    function switchTab(lang) {
      if (lang === currentLang && typingInterval) return;

      for (var i = 0; i < tabs.length; i++) {
        var t = tabs[i];
        if (t.getAttribute('data-terminal-tab') === lang) {
          t.classList.add('terminal-tab--active');
        } else {
          t.classList.remove('terminal-tab--active');
        }
      }

      for (var j = 0; j < statusItems.length; j++) {
        statusItems[j].textContent = datasets[lang].status;
      }

      startTyping(lang);
    }

    // ─── Bind event listeners ───
    for (var k = 0; k < tabs.length; k++) {
      tabs[k].addEventListener('click', function() {
        switchTab(this.getAttribute('data-terminal-tab'));
      });
    }

    // ─── Bootstrap ───
    for (var l = 0; l < statusItems.length; l++) {
      statusItems[l].textContent = datasets.python.status;
    }

    // Check reduced motion
    var isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (isReduced) {
      renderFull('python');
    } else {
      startTyping('python');
    }
  }

  // ─── Wait for DOM, then kick off ───
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTerminal);
  } else {
    initTerminal();
  }
})();