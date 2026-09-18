/**
 * Darukaa.Earth AI Biodiversity Intelligence Frontend Application
 */

document.addEventListener('DOMContentLoaded', () => {
  // Session tracking
  let sessionId = localStorage.getItem('darukaa_session_id');
  if (!sessionId) {
    sessionId = 'session-' + Math.random().toString(36).substring(2, 11);
    localStorage.setItem('darukaa_session_id', sessionId);
  }

  // DOM Elements
  const chatStream = document.getElementById('chat-stream');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const resetSessionBtn = document.getElementById('reset-session-btn');
  const benchmarkBtn = document.getElementById('benchmark-btn');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  // Diagnostics DOM
  const resultsEmpty = document.getElementById('results-empty');
  const resultsContainer = document.getElementById('results-container');
  const bannerSummary = document.getElementById('banner-summary');
  const bannerMeta = document.getElementById('banner-meta');
  const vulnerabilitiesList = document.getElementById('vulnerabilities-list');
  const recommendationsList = document.getElementById('recommendations-list');

  // State DOM
  const paramSoc = document.getElementById('param-soc');
  const paramPh = document.getElementById('param-ph');
  const paramRainfall = document.getElementById('param-rainfall');
  const paramCrop = document.getElementById('param-crop');
  const paramRegion = document.getElementById('param-region');
  const paramActiveCount = document.getElementById('param-active-count');
  const applyManualBtn = document.getElementById('apply-manual-btn');

  // Literature DOM
  const litSearchInput = document.getElementById('lit-search-input');
  const litSearchBtn = document.getElementById('lit-search-btn');
  const literatureResults = document.getElementById('literature-results');

  // Causal DOM
  const causalEdgesContainer = document.getElementById('causal-edges-container');

  // --- Tab Navigation ---
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');

      if (btn.dataset.tab === 'tab-causal' && !causalEdgesContainer.hasChildNodes()) {
        loadCausalGraph();
      }
      if (btn.dataset.tab === 'tab-literature' && !literatureResults.hasChildNodes()) {
        loadLiterature('soil organic carbon agroforestry');
      }
    });
  });

  // --- Chat Message Rendering ---
  function appendMessage(role, text, quickReplies = []) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role === 'user' ? 'user-message' : 'assistant-message'}`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = role === 'user' ? '👤' : '🔬';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const senderDiv = document.createElement('div');
    senderDiv.className = 'message-sender';
    senderDiv.textContent = role === 'user' ? 'You' : 'Darukaa Environmental Scientist';

    const bodyDiv = document.createElement('div');
    bodyDiv.className = 'message-body';
    bodyDiv.innerHTML = formatMarkdownText(text);

    contentDiv.appendChild(senderDiv);
    contentDiv.appendChild(bodyDiv);

    // Quick replies
    if (quickReplies && quickReplies.length > 0) {
      const chipsDiv = document.createElement('div');
      chipsDiv.className = 'quick-chips';
      quickReplies.forEach(qr => {
        const chip = document.createElement('button');
        chip.className = 'chip';
        chip.textContent = qr;
        chip.addEventListener('click', () => {
          chatInput.value = qr;
          chatForm.dispatchEvent(new Event('submit'));
        });
        chipsDiv.appendChild(chip);
      });
      contentDiv.appendChild(chipsDiv);
    }

    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(contentDiv);
    chatStream.appendChild(msgDiv);
    chatStream.scrollTop = chatStream.scrollHeight;
  }

  function formatMarkdownText(text) {
    if (!text) return '';
    let formatted = text
      .replace(/###\s+(.*)/g, '<h4 style="color:#34d399;margin-bottom:0.4rem;">$1</h4>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n-\s+(.*)/g, '<li style="margin-left:1.2rem;margin-bottom:0.25rem;">$1</li>');

    return `<p>${formatted}</p>`;
  }

  // --- Send Message ---
  async function sendMessage(text, explicitMetrics = null) {
    if (!text || !text.trim()) return;

    appendMessage('user', text);
    chatInput.value = '';

    // Typing indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant-message loading-msg';
    loadingDiv.innerHTML = `
      <div class="message-avatar">🔬</div>
      <div class="message-content">
        <div class="message-body" style="display:flex;gap:0.5rem;align-items:center;">
          <span class="pulse-dot"></span> Analyzing multi-metric causal pathways...
        </div>
      </div>
    `;
    chatStream.appendChild(loadingDiv);
    chatStream.scrollTop = chatStream.scrollHeight;

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          explicit_metrics: explicitMetrics,
        }),
      });

      loadingDiv.remove();

      if (!response.ok) {
        appendMessage('assistant', '⚠️ An error occurred while evaluating ecological reasoning.');
        return;
      }

      const data = await response.json();

      // Render assistant message
      appendMessage('assistant', data.reply, data.suggested_quick_replies);

      // Update parameters view
      updateParametersView(data.accumulated_metrics, data.active_variables_count);

      // If recommendations generated, display them
      if (data.recommendations && data.recommendations.length > 0) {
        displayRecommendations(data.recommendations, data.accumulated_metrics, data.retrieved_evidence);
        // Switch to recommendations tab
        document.querySelector('[data-tab="tab-recommendations"]').click();
      }

    } catch (err) {
      loadingDiv.remove();
      appendMessage('assistant', '⚠️ Network or connectivity error: ' + err.message);
    }
  }

  // --- Render Recommendations ---
  function displayRecommendations(recommendations, metrics, evidence) {
    resultsEmpty.classList.add('hidden');
    resultsContainer.classList.remove('hidden');

    bannerSummary.textContent = `Ecological Diagnostic Complete (${recommendations.length} Actionable Pathways)`;
    bannerMeta.textContent = `Evidence grounded in FAO, IPCC, and IPBES literature • Calibrated Multi-Metric Impact Forecasts`;

    // Recommendations list
    recommendationsList.innerHTML = '';
    recommendations.forEach(rec => {
      const card = document.createElement('div');
      card.className = 'rec-card';

      // Impact table rows
      let impactRows = '';
      rec.impacted_metrics.forEach(imp => {
        let timeClass = 'time-med';
        if (imp.time_horizon.includes('short_term')) timeClass = 'time-short';
        if (imp.time_horizon.includes('long_term')) timeClass = 'time-long';

        impactRows += `
          <tr>
            <td><strong>${imp.metric_name}</strong></td>
            <td style="color:#fda4af;">${imp.baseline_estimate}</td>
            <td style="color:#34d399;font-weight:600;">${imp.projected_improvement}</td>
            <td><span class="time-pill ${timeClass}">${imp.time_horizon.split(' ')[0]}</span></td>
            <td style="color:#94a3b8;font-size:0.75rem;">${imp.mechanism}</td>
          </tr>
        `;
      });

      // Citations
      let citationsHtml = '';
      rec.citations.forEach(c => {
        citationsHtml += `
          <div class="citation-item">
            <span class="citation-badge">[${c.id}]</span>
            <span>${c.title} (${c.publisher_or_journal}, ${c.year})</span>
            <a href="${c.doi_or_url}" target="_blank" rel="noopener" class="citation-link">DOI ↗</a>
          </div>
        `;
      });

      card.innerHTML = `
        <div class="rec-header">
          <div class="rec-title">${rec.title}</div>
          <div class="confidence-pill">${Math.round(rec.confidence_level * 100)}% Confidence</div>
        </div>
        <div class="rec-action">
          <strong>Intervention Action:</strong> ${rec.primary_action}
        </div>
        <div class="rec-reasoning">
          <strong>Scientific Reasoning:</strong> ${rec.scientific_reasoning}
        </div>
        <div class="rec-pathway">
          ⚡ ${rec.ecological_pathway}
        </div>
        <table class="impact-table">
          <thead>
            <tr>
              <th>Metric</th>
              <th>Baseline</th>
              <th>Projected Improvement</th>
              <th>Horizon</th>
              <th>Biogeochemical Mechanism</th>
            </tr>
          </thead>
          <tbody>
            ${impactRows}
          </tbody>
        </table>
        <div class="rec-citations">
          <div style="font-size:0.78rem;font-weight:600;color:#94a3b8;margin-bottom:0.2rem;">Authoritative Grounding & Citations:</div>
          ${citationsHtml}
        </div>
      `;
      recommendationsList.appendChild(card);
    });
  }

  // --- Update Parameters View ---
  function updateParametersView(metrics, activeCount) {
    if (!metrics) return;
    const soil = metrics.soil || {};
    const climate = metrics.climate || {};
    const land = metrics.land_use || {};

    paramSoc.textContent = soil.organic_carbon_pct !== undefined ? `${soil.organic_carbon_pct}%` : '—';
    paramPh.textContent = soil.ph !== undefined ? soil.ph : '—';
    paramRainfall.textContent = climate.annual_rainfall_mm !== undefined
      ? `${climate.annual_rainfall_mm} mm`
      : (climate.rainfall_category ? climate.rainfall_category.toUpperCase() : '—');
    paramCrop.textContent = land.crop_system || '—';
    paramRegion.textContent = metrics.region_name || '—';
    paramActiveCount.textContent = activeCount || 0;
  }

  // --- Load Literature ---
  async function loadLiterature(query) {
    literatureResults.innerHTML = '<div style="color:#94a3b8;padding:1rem;">Searching indexed scientific publications...</div>';
    try {
      const resp = await fetch('/api/knowledge/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query, top_k: 5 }),
      });
      const data = await resp.json();
      literatureResults.innerHTML = '';

      data.results.forEach(res => {
        const card = document.createElement('div');
        card.className = 'lit-card';
        card.innerHTML = `
          <div class="lit-header">
            <div class="lit-title">${res.title}</div>
            <div class="lit-score">Relevance: ${(res.relevance_score * 100).toFixed(0)}%</div>
          </div>
          <div style="font-size:0.75rem;color:#38bdf8;margin-bottom:0.4rem;">
            Domain: ${res.domain.toUpperCase()} &bull; Subdomain: ${res.subdomain}
          </div>
          <div class="lit-snippet">${res.matched_snippet}</div>
          <div class="citation-item">
            <span class="citation-badge">[${res.citation.id}]</span>
            <span>${res.citation.title} (${res.citation.publisher_or_journal}, ${res.citation.year})</span>
            <a href="${res.citation.doi_or_url}" target="_blank" rel="noopener" class="citation-link">DOI ↗</a>
          </div>
        `;
        literatureResults.appendChild(card);
      });
    } catch (e) {
      literatureResults.innerHTML = '<div style="color:#f43f5e;padding:1rem;">Failed to load literature: ' + e.message + '</div>';
    }
  }

  // --- Load Causal Graph ---
  async function loadCausalGraph() {
    causalEdgesContainer.innerHTML = '<div style="color:#94a3b8;padding:1rem;">Loading ecological causal dependencies...</div>';
    try {
      const resp = await fetch('/api/metrics/correlations');
      const data = await resp.json();
      causalEdgesContainer.innerHTML = '';

      data.edges.forEach(edge => {
        const card = document.createElement('div');
        card.className = 'causal-card';
        card.innerHTML = `
          <div class="causal-header-row">
            <div class="causal-title">${edge.source_metric} ➔ ${edge.target_metric}</div>
            <span class="confidence-pill" style="font-size:0.7rem;">${edge.interaction_type} (${(edge.strength * 100).toFixed(0)}%)</span>
          </div>
          <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.3rem;">
            ${edge.scientific_mechanism}
          </div>
          <div class="causal-equation">
            📐 Governing Law: ${edge.governing_equation_or_rule}
          </div>
          <div style="font-size:0.72rem;color:#64748b;margin-top:0.4rem;">
            Evidence Citation: <strong>${edge.citation_id}</strong>
          </div>
        `;
        causalEdgesContainer.appendChild(card);
      });
    } catch (e) {
      causalEdgesContainer.innerHTML = '<div style="color:#f43f5e;padding:1rem;">Failed to load causal graph: ' + e.message + '</div>';
    }
  }

  // --- Event Listeners ---
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const val = chatInput.value.trim();
    if (val) sendMessage(val);
  });

  // Benchmark button
  benchmarkBtn.addEventListener('click', () => {
    const benchmarkQuery = "Soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid";
    chatInput.value = benchmarkQuery;
    sendMessage(benchmarkQuery);
  });

  // Reset session
  resetSessionBtn.addEventListener('click', () => {
    sessionId = 'session-' + Math.random().toString(36).substring(2, 11);
    localStorage.setItem('darukaa_session_id', sessionId);
    chatStream.innerHTML = '';
    appendMessage(
      'assistant',
      'Session memory reset. What ecosystem or agricultural land conditions would you like to evaluate?'
    );
    resultsContainer.classList.add('hidden');
    resultsEmpty.classList.remove('hidden');
    updateParametersView({}, 0);
  });

  // Chip clicks
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const q = chip.getAttribute('data-query');
      if (q) {
        chatInput.value = q;
        chatForm.dispatchEvent(new Event('submit'));
      }
    });
  });

  // Literature search
  litSearchBtn.addEventListener('click', () => {
    const q = litSearchInput.value.trim();
    if (q) loadLiterature(q);
  });
  litSearchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const q = litSearchInput.value.trim();
      if (q) loadLiterature(q);
    }
  });

  // Manual parameters apply
  applyManualBtn.addEventListener('click', () => {
    const soc = document.getElementById('input-soc').value;
    const ph = document.getElementById('input-ph').value;
    const rain = document.getElementById('input-rainfall').value;
    const crop = document.getElementById('input-crop').value;
    const region = document.getElementById('input-region').value;

    const payload = {};
    if (soc) payload.soil_organic_carbon_pct = parseFloat(soc);
    if (ph) payload.soil_ph = parseFloat(ph);
    if (rain) payload.annual_rainfall_mm = parseFloat(rain);
    if (crop) payload.crop = crop;
    if (region) payload.region = region;

    sendMessage(
      `Manual simulation update: SOC ${soc || 'unspecified'}%, rainfall ${rain || 'unspecified'}mm, crop ${crop || 'unspecified'}`,
      payload
    );
  });
});
