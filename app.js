// CampusPulse Web Frontend Logic
const DEFAULT_PLACES = [
  "Main Gate & Bus Bay",
  "Academic Block",
  "Computer Labs",
  "Library",
  "Cafeteria",
  "Auditorium",
  "Medical Centre",
  "Girls Hostel",
  "Boys Hostel",
  "Sports Ground & Gym"
];

// State
let state = {
  tickets: JSON.parse(localStorage.getItem("campuspulse_tickets") || "[]"),
  filter: "all",
  attachedImage: null, // { base64, mime }
  cameraStream: null,
  settings: {
    apiKey: localStorage.getItem("campuspulse_api_key") || "",
    model: localStorage.getItem("campuspulse_model") || "gemini-2.0-flash",
    useAi: localStorage.getItem("campuspulse_use_ai") !== "false",
    places: JSON.parse(localStorage.getItem("campuspulse_places") || JSON.stringify(DEFAULT_PLACES))
  }
};

// DOM References
const problemText = document.getElementById("problem-text");
const photoFileInput = document.getElementById("photo-file");
const cameraToggleBtn = document.getElementById("camera-toggle-btn");
const cameraModal = document.getElementById("camera-modal");
const cameraStreamVideo = document.getElementById("camera-stream");
const snapBtn = document.getElementById("snap-btn");
const closeCameraBtn = document.getElementById("close-camera-btn");
const imagePreviewContainer = document.getElementById("image-preview-container");
const imagePreview = document.getElementById("image-preview");
const removeImageBtn = document.getElementById("remove-image-btn");
const reportForm = document.getElementById("report-form");
const submitBtn = document.getElementById("submit-btn");
const btnText = submitBtn.querySelector(".btn-text");
const btnSpinner = submitBtn.querySelector(".btn-spinner");

// Triage card elements
const triageResult = document.getElementById("triage-result");
const safetyBanner = document.getElementById("safety-banner");
const resPriority = document.getElementById("res-priority");
const resCategory = document.getElementById("res-category");
const resSla = document.getElementById("res-sla");
const resDept = document.getElementById("res-dept");
const resLocation = document.getElementById("res-location");
const resLanguage = document.getElementById("res-language");
const resSummary = document.getElementById("res-summary");
const resPhotoNoteRow = document.getElementById("res-photo-note-row");
const resPhotoNote = document.getElementById("res-photo-note");
const resSafetyElevation = document.getElementById("res-safety-elevation");
const resReply = document.getElementById("res-reply");
const resDraft = document.getElementById("res-draft");
const copyDraftBtn = document.getElementById("copy-draft-btn");

// Queue & stats
const statOpen = document.getElementById("stat-open");
const statCritical = document.getElementById("stat-critical");
const statResolved = document.getElementById("stat-resolved");
const clusterAlert = document.getElementById("cluster-alert");
const clusterBars = document.getElementById("cluster-bars");
const ticketsContainer = document.getElementById("tickets-container");

// Settings Modal
const settingsModal = document.getElementById("settings-modal");
const openSettingsBtn = document.getElementById("open-settings-btn");
const closeSettingsBtn = document.getElementById("close-settings-btn");
const saveSettingsBtn = document.getElementById("save-settings-btn");
const cfgApiKey = document.getElementById("cfg-api-key");
const cfgModel = document.getElementById("cfg-model");
const cfgUseAi = document.getElementById("cfg-use-ai");
const cfgPlaces = document.getElementById("cfg-places");

// Initialize UI
function init() {
  loadSettingsIntoModal();
  renderStatsAndQueue();
  bindEvents();
}

function bindEvents() {
  // Quick suggestion chips
  document.querySelectorAll(".chip-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      problemText.value = btn.dataset.text;
      problemText.focus();
    });
  });

  // Photo file upload
  photoFileInput.addEventListener("change", handleFileUpload);
  removeImageBtn.addEventListener("click", clearAttachedImage);

  // Camera handling
  cameraToggleBtn.addEventListener("click", startCamera);
  closeCameraBtn.addEventListener("click", stopCamera);
  snapBtn.addEventListener("click", captureSnapshot);

  // Form submission
  reportForm.addEventListener("submit", handleSubmitReport);

  // Copy draft button
  copyDraftBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(resDraft.textContent);
    const orig = copyDraftBtn.textContent;
    copyDraftBtn.textContent = "Copied!";
    setTimeout(() => (copyDraftBtn.textContent = orig), 2000);
  });

  // Filters
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.filter = btn.dataset.filter;
      renderQueue();
    });
  });

  // Settings modal controls
  openSettingsBtn.addEventListener("click", () => {
    loadSettingsIntoModal();
    settingsModal.classList.remove("hidden");
  });
  closeSettingsBtn.addEventListener("click", () => settingsModal.classList.add("hidden"));
  saveSettingsBtn.addEventListener("click", saveSettings);
}

// Settings management
function loadSettingsIntoModal() {
  cfgApiKey.value = state.settings.apiKey;
  cfgModel.value = state.settings.model;
  cfgUseAi.checked = state.settings.useAi;
  cfgPlaces.value = state.settings.places.join("\n");
}

function saveSettings() {
  state.settings.apiKey = cfgApiKey.value.trim();
  state.settings.model = cfgModel.value.trim() || "gemini-2.0-flash";
  state.settings.useAi = cfgUseAi.checked;
  state.settings.places = cfgPlaces.value.split("\n").map(s => s.trim()).filter(Boolean);

  localStorage.setItem("campuspulse_api_key", state.settings.apiKey);
  localStorage.setItem("campuspulse_model", state.settings.model);
  localStorage.setItem("campuspulse_use_ai", String(state.settings.useAi));
  localStorage.setItem("campuspulse_places", JSON.stringify(state.settings.places));

  settingsModal.classList.add("hidden");
}

// Media Handling
function handleFileUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(evt) {
    state.attachedImage = {
      base64: evt.target.result,
      mime: file.type || "image/jpeg"
    };
    imagePreview.src = evt.target.result;
    imagePreviewContainer.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
}

function clearAttachedImage() {
  state.attachedImage = null;
  photoFileInput.value = "";
  imagePreview.src = "";
  imagePreviewContainer.classList.add("hidden");
}

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
    state.cameraStream = stream;
    cameraStreamVideo.srcObject = stream;
    cameraModal.classList.remove("hidden");
  } catch (err) {
    alert("Camera access denied or unavailable: " + err.message);
  }
}

function stopCamera() {
  if (state.cameraStream) {
    state.cameraStream.getTracks().forEach(track => track.stop());
    state.cameraStream = null;
  }
  cameraModal.classList.add("hidden");
}

function captureSnapshot() {
  if (!state.cameraStream) return;
  const canvas = document.createElement("canvas");
  canvas.width = cameraStreamVideo.videoWidth || 640;
  canvas.height = cameraStreamVideo.videoHeight || 480;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(cameraStreamVideo, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.85);

  state.attachedImage = {
    base64: dataUrl,
    mime: "image/jpeg"
  };
  imagePreview.src = dataUrl;
  imagePreviewContainer.classList.remove("hidden");
  stopCamera();
}

// Submit & Triage
async function handleSubmitReport(e) {
  e.preventDefault();
  const text = problemText.value.trim();
  const image = state.attachedImage ? state.attachedImage.base64 : null;
  const mime = state.attachedImage ? state.attachedImage.mime : null;

  if (!text && !image) {
    alert("Please describe the issue or attach a photo.");
    return;
  }

  // Loading UI
  submitBtn.disabled = true;
  btnText.textContent = "Analysing...";
  btnSpinner.classList.remove("hidden");

  try {
    const res = await fetch("/api/triage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: text,
        image: image,
        mime: mime,
        places: state.settings.places,
        api_key: state.settings.apiKey,
        model: state.settings.model,
        use_ai: state.settings.useAi
      })
    });

    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status}`);
    }

    const data = await res.json();
    renderTriageResult(data);

    // Save ticket into queue
    const newTicket = {
      id: Date.now(),
      text: text || "Photo report",
      image: image,
      priority: data.priority,
      category: data.category,
      department: data.department,
      location: data.location,
      sla: data.sla,
      summary: data.summary,
      done: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    state.tickets.unshift(newTicket);
    localStorage.setItem("campuspulse_tickets", JSON.stringify(state.tickets));
    renderStatsAndQueue();

    // Reset form inputs (retain result card)
    problemText.value = "";
    clearAttachedImage();
  } catch (err) {
    alert("Triage analysis failed: " + err.message + "\nPlease verify your API key or network connection.");
  } finally {
    submitBtn.disabled = false;
    btnText.textContent = "Analyse & Submit";
    btnSpinner.classList.add("hidden");
  }
}

// Render Triage Result Card
function renderTriageResult(r) {
  triageResult.classList.remove("hidden");

  // Safety escalation banner
  if (r.priority === "Critical") {
    safetyBanner.className = "triage-banner banner-critical";
    safetyBanner.textContent = `🚨 Safety Escalation: Campus Security & Emergency Teams Alerted! ${r.people_at_risk ? (r.reply_to_reporter || "") : ""}`;
    safetyBanner.classList.remove("hidden");
  } else {
    safetyBanner.classList.add("hidden");
  }

  // Priority badge styling
  resPriority.textContent = r.priority;
  resPriority.className = `metric-val priority-badge pri-${r.priority.toLowerCase()}`;

  resCategory.textContent = (r.category || "General").replace("_", " ");
  resSla.textContent = r.sla || "Standard";
  resDept.textContent = r.department || "General Administration";
  resLocation.textContent = r.location || "Campus wide / Unknown";
  resLanguage.textContent = (r.language && r.language !== "none") ? r.language.toUpperCase() : "N/A";
  resSummary.textContent = r.summary || "";

  if (r.photo_note) {
    resPhotoNote.textContent = r.photo_note;
    resPhotoNoteRow.classList.remove("hidden");
  } else {
    resPhotoNoteRow.classList.add("hidden");
  }

  if (r.raised_by_rules) {
    resSafetyElevation.classList.remove("hidden");
  } else {
    resSafetyElevation.classList.add("hidden");
  }

  resReply.textContent = r.reply_to_reporter || "Your report has been logged and received.";
  resDraft.textContent = r.complaint_draft || "";

  triageResult.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Queue, Stats & Cluster Render
function renderStatsAndQueue() {
  const tickets = state.tickets;
  const openTickets = tickets.filter(t => !t.done);
  const criticalTickets = openTickets.filter(t => t.priority === "Critical");
  const resolvedTickets = tickets.filter(t => t.done);

  statOpen.textContent = openTickets.length;
  statCritical.textContent = criticalTickets.length;
  statResolved.textContent = resolvedTickets.length;

  renderClusterBars(openTickets);
  renderQueue();
}

function renderClusterBars(openTickets) {
  if (openTickets.length === 0) {
    clusterBars.innerHTML = '<p class="empty-state-text">No active incidents reported yet.</p>';
    clusterAlert.classList.add("hidden");
    return;
  }

  const byLoc = {};
  openTickets.forEach(t => {
    const loc = t.location || "Unknown";
    byLoc[loc] = (byLoc[loc] || 0) + 1;
  });

  const sorted = Object.entries(byLoc).sort((a, b) => b[1] - a[1]);
  const maxVal = Math.max(...Object.values(byLoc));

  // Top cluster alert
  const [topLoc, topCount] = sorted[0];
  if (topCount > 1 && topLoc.toLowerCase() !== "unknown") {
    clusterAlert.textContent = `⚠️ ${topLoc} has ${topCount} open issues. Repeated reports often share a cause, send a unified response team.`;
    clusterAlert.classList.remove("hidden");
  } else {
    clusterAlert.classList.add("hidden");
  }

  clusterBars.innerHTML = sorted.map(([loc, count]) => {
    const pct = Math.round((count / maxVal) * 100);
    return `
      <div class="cluster-bar-item">
        <div class="cluster-meta">
          <span>${loc}</span>
          <strong>${count} issue${count > 1 ? 's' : ''}</strong>
        </div>
        <div class="progress-track">
          <div class="progress-fill" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderQueue() {
  let list = state.tickets;
  if (state.filter === "critical") {
    list = list.filter(t => !t.done && t.priority === "Critical");
  } else if (state.filter === "active") {
    list = list.filter(t => !t.done);
  } else if (state.filter === "resolved") {
    list = list.filter(t => t.done);
  }

  if (list.length === 0) {
    ticketsContainer.innerHTML = '<p class="empty-state-text">No incidents in this view.</p>';
    return;
  }

  // Priority order
  const priRank = { Critical: 0, High: 1, Medium: 2, Low: 3 };
  const sorted = [...list].sort((a, b) => {
    if (a.done !== b.done) return a.done ? 1 : -1;
    return (priRank[a.priority] ?? 4) - (priRank[b.priority] ?? 4);
  });

  ticketsContainer.innerHTML = sorted.map(t => {
    const priClass = `pri-${(t.priority || "medium").toLowerCase()}`;
    return `
      <div class="ticket-card ${t.done ? 'ticket-resolved' : ''}">
        ${t.image ? `<img src="${t.image}" alt="Attachment" class="ticket-thumb">` : ''}
        <div class="ticket-content">
          <div class="ticket-meta">
            <span class="priority-badge ${priClass}">${t.priority}</span>
            <span>· ${(t.category || "General").replace("_", " ")}</span>
            <span>· 📍 ${t.location}</span>
          </div>
          <p class="ticket-body">${escapeHtml(t.text)}</p>
          <span class="ticket-dept">Department: ${t.department} · Target: ${t.sla}</span>
        </div>
        <div class="ticket-actions">
          ${!t.done ? `
            <button class="btn btn-sm btn-secondary" onclick="resolveTicket(${t.id})">Resolve</button>
          ` : `
            <span class="text-dim" style="font-size:12px;">Resolved ✓</span>
          `}
        </div>
      </div>
    `;
  }).join("");
}

function resolveTicket(id) {
  const ticket = state.tickets.find(t => t.id === id);
  if (ticket) {
    ticket.done = true;
    localStorage.setItem("campuspulse_tickets", JSON.stringify(state.tickets));
    renderStatsAndQueue();
  }
}
window.resolveTicket = resolveTicket;

function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[m]));
}

// Start app
init();
