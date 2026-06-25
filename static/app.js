// ============================================================
// STATE
// ============================================================
let sessionScans  = 0;
let sessionSafe   = 0;
let sessionUnsafe = 0;
let activeTab     = 'text';

// ============================================================
// TABS
// ============================================================
function switchTab(tab, btn) {
  activeTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('panel-' + tab).classList.add('active');
}

// ============================================================
// CHAR COUNT
// ============================================================
function updateCharCount(el) {
  document.getElementById('char-count').textContent = el.value.length + ' chars';
}

// ============================================================
// FILE HANDLING
// ============================================================
function handleFile(input, type) {
  if (!input.files.length) return;
  const file = input.files[0];
  document.getElementById(type + '-name').textContent = file.name;
  document.getElementById(type + '-preview').classList.add('show');
}

function removeFile(type) {
  document.getElementById(type + '-file').value = '';
  document.getElementById(type + '-preview').classList.remove('show');
}

function handleDrag(e, zone) {
  e.preventDefault();
  zone.classList.add('dragover');
}

function handleDragLeave(zone) {
  zone.classList.remove('dragover');
}

function handleDrop(e, inputId) {
  e.preventDefault();
  e.currentTarget.classList.remove('dragover');
  const input = document.getElementById(inputId);
  input.files  = e.dataTransfer.files;
  const type   = inputId.includes('image') ? 'image' : 'audio';
  handleFile(input, type);
}

// ============================================================
// LOADING STEPS ANIMATION
// ============================================================
async function animateSteps() {
  const steps  = ['step-1', 'step-2', 'step-3', 'step-4'];
  const delays = [300, 900, 1600, 2400];
  for (let i = 0; i < steps.length; i++) {
    await new Promise(r => setTimeout(r, delays[i]));
    document.getElementById(steps[i]).classList.add('active');
  }
}

// ============================================================
// MAIN SCAN
// ============================================================
async function runScan() {
  const formData = new FormData();

  if (activeTab === 'text') {
    const txt = document.getElementById('text-input').value.trim();
    if (!txt) { alert('Please enter some text to scan.'); return; }
    formData.append('text', txt);

  } else if (activeTab === 'image') {
    const file = document.getElementById('image-file').files[0];
    if (!file) { alert('Please upload an image file.'); return; }
    formData.append('image', file);

  } else if (activeTab === 'audio') {
    const file = document.getElementById('audio-file').files[0];
    if (!file) { alert('Please upload an audio file.'); return; }
    formData.append('audio', file);
  }

  const meta = document.getElementById('metadata-input').value.trim();
  if (meta) formData.append('metadata', meta);

  // Show loading state
  document.getElementById('submit-btn').disabled = true;
  document.getElementById('loading').classList.add('show');
  document.getElementById('results').classList.remove('show');

  animateSteps();

  try {
    const res  = await fetch('/ingest', { method: 'POST', body: formData });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert('❌ Error connecting to API: ' + err.message);
    resetLoading();
  }
}

// ============================================================
// RENDER RESULTS
// ============================================================
function renderResults(data) {
  updateSessionStats(data.safe_to_send);
  renderVerdict(data);
  renderHeuristic(data.heuristic);
  renderModel(data.model);
  renderExtractedText(data.final_text);
  renderGemini(data.gemini_response);
  renderTiming(data);

  resetLoading();
  document.getElementById('results').classList.add('show');
  document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================================
// SESSION STATS
// ============================================================
function updateSessionStats(isSafe) {
  sessionScans++;
  if (isSafe) sessionSafe++;
  else sessionUnsafe++;
  document.getElementById('stat-scans').textContent  = sessionScans;
  document.getElementById('stat-safe').textContent   = sessionSafe;
  document.getElementById('stat-unsafe').textContent = sessionUnsafe;
}

// ============================================================
// VERDICT
// ============================================================
function renderVerdict(data) {
  const isSafe = data.safe_to_send;
  const risk   = data.heuristic?.risk || 'low';
  const banner = document.getElementById('verdict-banner');

  banner.className = 'verdict-banner fade-up ' +
    (isSafe ? 'safe' : (risk === 'medium' ? 'medium' : 'unsafe'));

  document.getElementById('verdict-icon').innerHTML = isSafe
    ? '<i class="fas fa-shield-check"></i>'
    : '<i class="fas fa-shield-exclamation"></i>';

  document.getElementById('verdict-title').textContent = isSafe
    ? '✅ Input is Safe'
    : '🚨 Threat Detected';

  document.getElementById('verdict-sub').textContent = isSafe
    ? 'Passed all security layers. Gemini response generated.'
    : 'Blocked by security pipeline. Input flagged as potentially malicious.';

  document.getElementById('verdict-id').textContent =
    'ID: ' + (data.request_id || '—');
}

// ============================================================
// HEURISTIC
// ============================================================
function renderHeuristic(heuristic) {
  const score  = heuristic?.score ?? 0;
  const risk   = heuristic?.risk  ?? 'low';
  const maxScore = 10;
  const pct    = Math.min((score / maxScore) * 100, 100);

  document.getElementById('risk-score').textContent = score.toFixed(2);

  const riskBar = document.getElementById('risk-bar');
  riskBar.style.width = '0%';
  setTimeout(() => { riskBar.style.width = pct + '%'; }, 100);
  riskBar.className = 'risk-bar-fill ' + risk;

  const riskPill = document.getElementById('risk-pill');
  riskPill.textContent = risk.toUpperCase();
  riskPill.className   = 'pill ' + risk;

  renderPatternTags(heuristic?.matched_patterns || {});

  const qs     = heuristic?.quick_safe;
  const qsPill = document.getElementById('quick-safe-pill');
  qsPill.textContent = qs ? 'Yes' : 'No';
  qsPill.className   = 'pill ' + (qs ? 'safe' : 'unsafe');
}

function renderPatternTags(matched) {
  const tagList = document.getElementById('tag-list');
  tagList.innerHTML = '';
  let hasPatterns = false;

  for (const [cat, patterns] of Object.entries(matched)) {
    patterns.forEach(p => {
      hasPatterns = true;
      const tag = document.createElement('span');
      tag.className = 'tag ' + cat;
      tag.innerHTML = `<i class="fas fa-triangle-exclamation"></i> ${p}`;
      tagList.appendChild(tag);
    });
  }

  if (!hasPatterns) {
    const tag = document.createElement('span');
    tag.className = 'tag none';
    tag.innerHTML = '<i class="fas fa-check"></i> No patterns matched';
    tagList.appendChild(tag);
  }
}

// ============================================================
// DISTILBERT MODEL
// ============================================================
function renderModel(modelData) {
  const confRing  = document.getElementById('conf-ring');
  const confPct   = document.getElementById('conf-pct');
  const modelPill = document.getElementById('model-pill');
  const skipMsg   = document.getElementById('model-skip-msg');

  if (modelData) {
    const conf = modelData.confidence;
    const pred = modelData.prediction;
    const circumference = 283;
    const offset = circumference - (conf / 100) * circumference;

    confPct.textContent = conf.toFixed(1) + '%';
    confRing.className  = 'ring-fill ' + (pred === 'Safe' ? 'safe' : 'unsafe');
    setTimeout(() => { confRing.style.strokeDashoffset = offset; }, 200);

    modelPill.textContent = pred.toUpperCase();
    modelPill.className   = 'pill ' + (pred === 'Safe' ? 'safe' : 'unsafe');
    skipMsg.textContent   = '';
  } else {
    confPct.textContent              = '—';
    confRing.style.strokeDashoffset  = 283;
    modelPill.textContent            = 'SKIPPED';
    modelPill.className              = 'pill medium';
    skipMsg.textContent              = 'Model skipped — heuristic layer blocked this input.';
  }
}

// ============================================================
// EXTRACTED TEXT
// ============================================================
function renderExtractedText(text) {
  document.getElementById('extracted-text').textContent = text || '(empty)';
}

// ============================================================
// GEMINI RESPONSE
// ============================================================
function renderGemini(geminiReply) {
  const geminiBox    = document.getElementById('gemini-box');
  const geminiStatus = document.getElementById('gemini-status');

  geminiBox.style.color = '';

  if (geminiReply?.gemini_reply) {
    geminiStatus.textContent = 'Gemini responded successfully';
    geminiBox.textContent    = geminiReply.gemini_reply;
  } else {
    geminiStatus.textContent = 'Gemini was not called';
    geminiBox.textContent    = geminiReply?.error || 'No response available.';
    geminiBox.style.color    = 'var(--text-muted)';
  }
}

// ============================================================
// TIMING METRICS
// ============================================================
function renderTiming(data) {
  const fmt = v => (v != null ? v.toFixed(4) + 's' : '—');
  document.getElementById('t-heuristic').textContent = fmt(data.heuristic?.time_sec);
  document.getElementById('t-model').textContent     = fmt(data.model?.time_sec);
  document.getElementById('t-gemini').textContent    = fmt(data.gemini_time_sec);
  document.getElementById('t-total').textContent     = fmt(data.total_time_sec);
  document.getElementById('t-ocr').textContent       = fmt(data.ocr_time_sec);
  document.getElementById('t-asr').textContent       = fmt(data.asr_time_sec);
}

// ============================================================
// RESET
// ============================================================
function resetLoading() {
  document.getElementById('loading').classList.remove('show');
  document.getElementById('submit-btn').disabled = false;
  ['step-1', 'step-2', 'step-3', 'step-4'].forEach(id => {
    document.getElementById(id).classList.remove('active', 'done');
  });
}

function resetUI() {
  document.getElementById('results').classList.remove('show');
  document.getElementById('text-input').value = '';
  document.getElementById('char-count').textContent = '0 chars';
  document.getElementById('metadata-input').value = '';
  removeFile('image');
  removeFile('audio');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}