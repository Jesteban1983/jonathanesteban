// === INTERACTIVE PROJECT COST CALCULATOR ===

export function initCalculator() {
  const calcForm = document.getElementById('calculatorForm');
  const estimatedPriceEl = document.getElementById('estimatedPrice');
  const estimatedTimeEl = document.getElementById('estimatedTime');
  const requestProposalBtn = document.getElementById('requestProposalBtn');

  if (!calcForm || !estimatedPriceEl || !estimatedTimeEl) return;

  const serviceLabels = {
    landing: 'Landing page web',
    fullstack: 'Web profesional multipagina',
    backend: 'APIs REST y Backend',
    'ai-agent': 'Asistente IA para negocio',
    'it-support': 'Soporte IT'
  };

  const addonLabels = {
    auth: 'Area privada para clientes',
    database: 'Base de datos y formularios avanzados',
    automation: 'Automatizaciones de tareas (n8n)',
    'seo-geo': 'SEO + GEO'
  };

  function getProposalData() {
    let basePrice = 0;
    let baseDays = 0;

    const serviceType = calcForm.querySelector('input[name="service_type"]:checked');
    const serviceKey = serviceType?.value || 'landing';

    switch (serviceKey) {
      case 'landing': basePrice += 450; baseDays += 5; break;
      case 'fullstack': basePrice += 950; baseDays += 14; break;
      case 'backend': basePrice += 750; baseDays += 10; break;
      case 'ai-agent': basePrice += 850; baseDays += 12; break;
      case 'it-support': basePrice += 300; baseDays += 3; break;
      default: basePrice += 450; baseDays += 5;
    }

    const checkedAddons = Array.from(calcForm.querySelectorAll('input[name="addons"]:checked'));
    checkedAddons.forEach(addon => {
      switch (addon.value) {
        case 'auth': basePrice += 200; baseDays += 3; break;
        case 'database': basePrice += 250; baseDays += 4; break;
        case 'automation': basePrice += 300; baseDays += 5; break;
        case 'seo-geo': basePrice += 150; baseDays += 2; break;
      }
    });

    const urgency = calcForm.querySelector('select[name="urgency"]');
    if (urgency && urgency.value === 'urgent') {
      basePrice = Math.round(basePrice * 1.25);
      baseDays = Math.max(3, Math.round(baseDays * 0.7));
    }

    const addonsText = checkedAddons.length
      ? checkedAddons.map(item => addonLabels[item.value] || item.value).join(', ')
      : 'Sin módulos adicionales';

    return {
      serviceKey,
      serviceLabel: serviceLabels[serviceKey] || serviceKey,
      addonsText,
      price: basePrice,
      days: baseDays
    };
  }

  function updateProposalCta() {
    if (!requestProposalBtn) return;

    const proposal = getProposalData();
    const subject = `Solicitud de presupuesto: ${proposal.serviceLabel}`;
    const message = [
      'Hola Jonathan, quiero solicitar presupuesto para este servicio:',
      `- Servicio principal: ${proposal.serviceLabel}`,
      `- Módulos adicionales: ${proposal.addonsText}`,
      `- Presupuesto estimado mostrado: ${proposal.price} EUR`,
      `- Plazo estimado mostrado: ${proposal.days} días hábiles`,
      '',
      'Me gustaría que me compartieras una propuesta formal y próximos pasos.'
    ].join('\n');

    const params = new URLSearchParams({
      prefill: 'budget',
      subject,
      message
    });

    requestProposalBtn.href = `/contacto/?${params.toString()}`;

    // Backup for very long URLs or navigation edge cases.
    localStorage.setItem('budgetPrefill', JSON.stringify({ subject, message }));
  }

  function calculate() {
    const proposal = getProposalData();
    estimatedPriceEl.textContent = `${proposal.price} €`;
    estimatedTimeEl.textContent = `${proposal.days} días hábiles`;
    updateProposalCta();
  }

  calcForm.addEventListener('change', calculate);
  calculate();
}
