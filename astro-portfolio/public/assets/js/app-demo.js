// === INTERACTIVE DEMO APP LOGIC ===

export function initDemoApp() {
  const demoInput = document.getElementById('demoInput');
  const demoRunBtn = document.getElementById('demoRunBtn');
  const demoOutput = document.getElementById('demoOutput');

  if (!demoInput || !demoRunBtn || !demoOutput) return;

  demoRunBtn.addEventListener('click', () => {
    const text = demoInput.value.trim();
    if (!text) {
      demoOutput.innerHTML = `<p class="text-error">⚠️ Por favor, introduce un comando o texto de prueba.</p>`;
      return;
    }

    demoOutput.innerHTML = `<p style="color: var(--primary);">🤖 Procesando entrada mediante Agente de IA simulación...</p>`;

    setTimeout(() => {
      const charCount = text.length;
      const wordCount = text.split(/\s+/).length;
      
      demoOutput.innerHTML = `
        <div style="background: var(--surface-2-color); padding: 1.25rem; border-radius: 0.75rem; border: 1px solid var(--border-color);">
          <h4 style="color: var(--success); margin-bottom: 0.5rem;">✅ Análisis Completado Exitosamente</h4>
          <p><strong>Comando recibido:</strong> "${text}"</p>
          <p><strong>Métricas:</strong> ${wordCount} palabras | ${charCount} caracteres</p>
          <p><strong>Estado del Agente:</strong> Simulación de pipeline en tiempo real — Conectado a la API de demostración.</p>
        </div>
      `;
    }, 1200);
  });
}
