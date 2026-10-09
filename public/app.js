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

// Multilingual UI Dictionary (English, Kannada, Hindi, Marathi)
const I18N = {
  en: {
    brandSub: "Sapthagiri NPS University · Incident Triage System",
    panelTitle: "Report an Issue",
    panelDesc: "Submit details in your preferred language. Photos are analysed using Gemini Vision.",
    labelProblem: "What is the problem?",
    placeholderProblem: "e.g. Lift stuck between floors in Academic Block, two people inside... (or in Hindi, Kannada, Marathi)",
    labelPhoto: "Photo Evidence (Optional)",
    btnUpload: "Upload Image",
    btnCamera: "Use Camera",
    btnSubmit: "Analyse & Submit",
    btnAnalysing: "Analysing...",
    queueTitle: "Campus Queue & Analytics",
    queueDesc: "Real-time status overview and location incident clustering.",
    statOpen: "Open Tickets",
    statCritical: "Critical Safety",
    statResolved: "Resolved",
    clusterTitle: "Location Cluster Analysis",
    incidentQueueTitle: "Incident Queue",
    chips: [
      { label: "🚨 Stuck in Lift", text: "Lift stuck between floors in the Academic Block, two people inside" },
      { label: "🔥 Smoke in Lab", text: "Smoke coming from AC in Computer Labs, students evacuating" },
      { label: "💧 Water Leak", text: "Severe water pipe burst flooding the cafeteria wash area" },
      { label: "📶 Library Wi-Fi", text: "Wi-Fi keeps disconnecting in the Library reading hall" }
    ]
  },
  kn: {
    brandSub: "ಸಪ್ತಗಿರಿ ಎನ್‌ಪಿಎಸ್ ವಿಶ್ವವಿದ್ಯಾಲಯ · ತುರ್ತು ರವಾನೆ ಮತ್ತು ಘಟನೆ ವಿಶ್ಲೇಷಣೆ ವ್ಯವಸ್ಥೆ",
    panelTitle: "ಸಮಸ್ಯೆಯನ್ನು ವರದಿ ಮಾಡಿ",
    panelDesc: "ಕನ್ನಡ ಅಥವಾ ಯಾವುದೇ ಭಾಷೆಯಲ್ಲಿ ವರದಿ ಸಲ್ಲಿಸಿ. ಭಾವಚಿತ್ರಗಳನ್ನು ಜೆಮಿನಿ ಎಐ ಮೂಲಕ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತದೆ.",
    labelProblem: "ಸಮಸ್ಯೆ ಏನು?",
    placeholderProblem: "ಉದಾ: ಅಕಾಡೆಮಿಕ್ ಬ್ಲಾಕ್‌ನಲ್ಲಿ ಲಿಫ್ಟ್ ಮಧ್ಯದಲ್ಲಿ ಸಿಕ್ಕಿಹಾಕಿಕೊಂಡಿದೆ, ಇಬ್ಬರು ವಿದ್ಯಾರ್ಥಿಗಳು ಒಳಗಿದ್ದಾರೆ...",
    labelPhoto: "ಭಾವಚಿತ್ರ ಪುರಾವೆ (ಐಚ್ಛಿಕ)",
    btnUpload: "ಫೋಟೋ ಅಪ್‌ಲೋಡ್",
    btnCamera: "ಕ್ಯಾಮರಾ ಬಳಸಿ",
    btnSubmit: "ವಿಶ್ಲೇಷಿಸಿ ಮತ್ತು ಸಲ್ಲಿಸಿ",
    btnAnalysing: "ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
    queueTitle: "ಕ್ಯಾಂಪಸ್ ಘಟನೆಗಳ ಸರದಿ ಮತ್ತು ವಿಶ್ಲೇಷಣೆ",
    queueDesc: "ನೈಜ-ಸಮಯದ ಸ್ಥಿತಿ ಅವಲೋಕನ ಮತ್ತು ಸ್ಥಳೀಯ ಘಟನೆಗಳ ಕ್ಲಸ್ಟರ್.",
    statOpen: "ತೆರೆದಿರುವ ದೂರುಗಳು",
    statCritical: "ತುರ್ತು ಸುರಕ್ಷತೆ",
    statResolved: "ಪರಿಹರಿಸಲಾಗಿದೆ",
    clusterTitle: "ಸ್ಥಳೀಯ ಕ್ಲಸ್ಟರ್ ವಿಶ್ಲೇಷಣೆ",
    incidentQueueTitle: "ಘಟನೆಗಳ ಸರದಿ (Queue)",
    chips: [
      { label: "🚨 ಲಿಫ್ಟ್‌ನಲ್ಲಿ ಸಿಲುಕಿದ್ದಾರೆ", text: "ಅಕಾಡೆಮಿಕ್ ಬ್ಲಾಕ್‌ನಲ್ಲಿ ಲಿಫ್ಟ್ ಮಧ್ಯದಲ್ಲಿ ಸಿಕ್ಕಿಹಾಕಿಕೊಂಡಿದೆ, ಇಬ್ಬರು ಒಳಗಿದ್ದಾರೆ" },
      { label: "🔥 ಲ್ಯಾಬ್‌ನಲ್ಲಿ ಹೊಗೆ", text: "ಕಂಪ್ಯೂಟರ್ ಲ್ಯಾಬ್‌ನಲ್ಲಿ ಎಸಿ ಯಿಂದ ಹೊಗೆ ಬರುತ್ತಿದೆ, ವಿದ್ಯಾರ್ಥಿಗಳು ಹೊರಬರುತ್ತಿದ್ದಾರೆ" },
      { label: "💧 ನೀರು ಸೋರಿಕೆ", text: "ಕ್ಯಾಂಟೀನ್ ವಾಶ್ ಪ್ರದೇಶದಲ್ಲಿ ಪೈಪ್ ಒಡೆದು ನೀರು ಸೋರುತ್ತಿದೆ" },
      { label: "📶 ಲೈಬ್ರರಿ ವೈಫೈ", text: "ಲೈಬ್ರರಿ ರೀಡಿಂಗ್ ಹಾಲ್‌ನಲ್ಲಿ ವೈಫೈ ಸಂಪರ್ಕ ಕಡಿತಗೊಳ್ಳುತ್ತಿದೆ" }
    ]
  },
  hi: {
    brandSub: "सप्तगिरि एनपीएस विश्वविद्यालय · घटना रिपोर्टिंग और सुरक्षा प्रबंधन प्रणाली",
    panelTitle: "समस्या की रिपोर्ट करें",
    panelDesc: "अपनी पसंदीदा भाषा में विवरण दर्ज करें। जेमिनी विज़न द्वारा फोटो का विश्लेषण किया जाता है।",
    labelProblem: "समस्या क्या है?",
    placeholderProblem: "उदा: अकादमिक ब्लॉक में लिफ्ट मंजिलों के बीच फंस गई है, दो लोग अंदर हैं...",
    labelPhoto: "फोटो साक्ष्य (वैकल्पिक)",
    btnUpload: "फोटो अपलोड करें",
    btnCamera: "कैमरा उपयोग करें",
    btnSubmit: "विश्लेषण करें और सबमिट करें",
    btnAnalysing: "विश्लेषण हो रहा है...",
    queueTitle: "परिसर कतार और विश्लेषण",
    queueDesc: "वास्तविक समय स्थिति और स्थान संकुल विश्लेषण।",
    statOpen: "लंबित शिकायतें",
    statCritical: "अति गंभीर",
    statResolved: "सुलझाया गया",
    clusterTitle: "स्थान क्लस्टर विश्लेषण",
    incidentQueueTitle: "घटना कतार (Queue)",
    chips: [
      { label: "🚨 लिफ्ट में फंसे लोग", text: "अकादमिक ब्लॉक में लिफ्ट मंजिलों के बीच फंस गई है, दो लोग अंदर हैं" },
      { label: "🔥 लैब में धुआं", text: "कंप्यूटर लैब में एसी से धुआं निकल रहा है, छात्र बाहर निकल रहे हैं" },
      { label: "💧 पानी का रिसाव", text: "कैंटीन वॉश एरिया में पाइप से पानी का भारी रिसाव हो रहा है" },
      { label: "📶 लाइब्रेरी वाई-फाई", text: "लाइब्रेरी रीडिंग हॉल में वाई-फाई बार-बार डिस्कनेक्ट हो रहा है" }
    ]
  },
  mr: {
    brandSub: "सप्तगिरी एनपीएस विद्यापीठ · घटना तक्रार आणि सुरक्षा व्यवस्थापन",
    panelTitle: "समस्येची नोंद करा",
    panelDesc: "आपल्या पसंतीच्या भाषेत तपशील द्या. जेमिनी व्हिजनद्वारे फोटोचे विश्लेषण केले जाते.",
    labelProblem: "समस्या काय आहे?",
    placeholderProblem: "उदा: अकॅडेमिक ब्लॉकमध्ये लिफ्ट अडकली आहे, दोन जण आत आहेत...",
    labelPhoto: "छायाचित्र पुरावा (पर्यायी)",
    btnUpload: "फोटो अपलोड",
    btnCamera: "कॅमेरा वापरा",
    btnSubmit: "विश्लेषण करा आणि सबमिट करा",
    btnAnalysing: "विश्लेषण करत आहे...",
    queueTitle: "कॅम्पस तक्रार रांग आणि विश्लेषण",
    queueDesc: "थेट स्थिती आणि परिसर क्लस्टर विश्लेषण.",
    statOpen: "प्रलंबित तक्रारी",
    statCritical: "गंभीर",
    statResolved: "सोडवले",
    clusterTitle: "स्थान क्लस्टर विश्लेषण",
    incidentQueueTitle: "घटना रांग (Queue)",
    chips: [
      { label: "🚨 लिफ्टमध्ये अडकले", text: "अकॅडेमिक ब्लॉकमध्ये लिफ्ट अडकली आहे, दोन जण आत आहेत" },
      { label: "🔥 लॅबमध्ये धूर", text: "कॉम्प्युटर लॅबमध्ये एसीतून धूर येत आहे, विद्यार्थी बाहेर पडत आहेत" },
      { label: "💧 पाण्याची गळती", text: "कॅन्टीन वॉश भागात पाईप फुटून पाणी वाहत आहे" },
      { label: "📶 लायब्ररी वाय-फाय", text: "लायब्ररी रीडिंग हॉलमध्ये वाय-फाय वारंवार बंद पडत आहे" }
    ]
  }
};

// State
let state = {
  lang: localStorage.getItem("campuspulse_lang") || "en",
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
const brandSub = document.querySelector(".brand-sub");
const reportPanelTitle = document.querySelector(".report-panel .panel-header h2");
const reportPanelDesc = document.querySelector(".report-panel .panel-desc");
const problemText = document.getElementById("problem-text");
const problemLabel = document.querySelector('label[for="problem-text"]');
const photoLabel = document.querySelector(".report-form .form-group:nth-of-type(2) label");
const uploadBtnSpan = document.querySelector(".upload-trigger span");
const cameraBtnSpan = document.querySelector(".camera-trigger span");
const quickChipsContainer = document.querySelector(".quick-chips");
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

// Queue & stats
const queuePanelTitle = document.querySelector(".queue-panel .panel-header h2");
const queuePanelDesc = document.querySelector(".queue-panel .panel-desc");
const statOpenTitle = document.querySelector(".stat-card:nth-child(1) .stat-title");
const statCriticalTitle = document.querySelector(".stat-card:nth-child(2) .stat-title");
const statResolvedTitle = document.querySelector(".stat-card:nth-child(3) .stat-title");
const clusterHeader = document.querySelector(".cluster-section h3");
const queueSectionHeader = document.querySelector(".queue-header h3");
const statOpen = document.getElementById("stat-open");
const statCritical = document.getElementById("stat-critical");
const statResolved = document.getElementById("stat-resolved");
const clusterAlert = document.getElementById("cluster-alert");
const clusterBars = document.getElementById("cluster-bars");
const ticketsContainer = document.getElementById("tickets-container");

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
const resFacility = document.getElementById("res-facility");
const resHotline = document.getElementById("res-hotline");
const exportCsvBtn = document.getElementById("export-csv-btn");

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
  applyLanguage(state.lang);
  loadSettingsIntoModal();
  renderStatsAndQueue();
  bindEvents();
}

function applyLanguage(lang) {
  state.lang = lang || "en";
  localStorage.setItem("campuspulse_lang", state.lang);
  const cur = I18N[state.lang] || I18N.en;

  // Update active chip button
  document.querySelectorAll(".lang-chip").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.lang === state.lang);
  });

  if (brandSub) brandSub.textContent = cur.brandSub;
  if (reportPanelTitle) reportPanelTitle.textContent = cur.panelTitle;
  if (reportPanelDesc) reportPanelDesc.textContent = cur.panelDesc;
  if (problemLabel) problemLabel.textContent = cur.labelProblem;
  if (problemText) problemText.placeholder = cur.placeholderProblem;
  if (photoLabel) photoLabel.textContent = cur.labelPhoto;
  if (uploadBtnSpan) uploadBtnSpan.textContent = cur.btnUpload;
  if (cameraBtnSpan) cameraBtnSpan.textContent = cur.btnCamera;
  if (btnText) btnText.textContent = cur.btnSubmit;

  if (queuePanelTitle) queuePanelTitle.textContent = cur.queueTitle;
  if (queuePanelDesc) queuePanelDesc.textContent = cur.queueDesc;
  if (statOpenTitle) statOpenTitle.textContent = cur.statOpen;
  if (statCriticalTitle) statCriticalTitle.textContent = cur.statCritical;
  if (statResolvedTitle) statResolvedTitle.textContent = cur.statResolved;
  if (clusterHeader) clusterHeader.textContent = cur.clusterTitle;
  if (queueSectionHeader) queueSectionHeader.textContent = cur.incidentQueueTitle;

  // Render quick chips for this language
  renderChips(cur.chips);
}

function renderChips(chips) {
  if (!quickChipsContainer) return;
  quickChipsContainer.innerHTML = "";
  chips.forEach(c => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip-btn";
    btn.textContent = c.label;
    btn.dataset.text = c.text;
    btn.addEventListener("click", () => {
      problemText.value = c.text;
      problemText.focus();
    });
    quickChipsContainer.appendChild(btn);
  });
}

function bindEvents() {
  // Language switcher
  document.querySelectorAll(".lang-chip").forEach(btn => {
    btn.addEventListener("click", () => {
      applyLanguage(btn.dataset.lang);
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

  // Export CSV button
  if (exportCsvBtn) {
    exportCsvBtn.addEventListener("click", exportIncidentsToCsv);
  }

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
    alert(state.lang === "kn" ? "ದಯವಿಟ್ಟು ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ ಅಥವಾ ಫೋಟೋ ಸೇರಿಸಿ." :
          state.lang === "hi" ? "कृपया पहले समस्या का वर्णन करें या फोटो जोड़ें।" :
          state.lang === "mr" ? "कृपया समस्येचे वर्णन करा किंवा फोटो जोडा." :
          "Please describe the issue or attach a photo.");
    return;
  }

  // Loading UI
  submitBtn.disabled = true;
  btnText.textContent = (I18N[state.lang] || I18N.en).btnAnalysing;
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
    btnText.textContent = (I18N[state.lang] || I18N.en).btnSubmit;
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
  if (resFacility) resFacility.textContent = r.facility_code || "CAMPUS-GEN";

  if (r.priority === "Critical" && r.emergency_hotline) {
    resHotline.textContent = `📞 Immediate Campus Emergency Dispatch: ${r.emergency_hotline}`;
    resHotline.classList.remove("hidden");
  } else if (resHotline) {
    resHotline.classList.add("hidden");
  }

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

  const resolveLabel = (state.lang === "kn" ? "ಪರಿಹರಿಸಿ" : state.lang === "hi" ? "सुलझाएं" : state.lang === "mr" ? "सोडवा" : "Resolve");
  const resolvedText = (state.lang === "kn" ? "ಪರಿಹರಿಸಲಾಗಿದೆ ✓" : state.lang === "hi" ? "सुलझाया गया ✓" : state.lang === "mr" ? "सोडवले ✓" : "Resolved ✓");

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
            <button class="btn btn-sm btn-secondary" onclick="resolveTicket(${t.id})">${resolveLabel}</button>
          ` : `
            <span class="text-dim" style="font-size:12px;">${resolvedText}</span>
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

function exportIncidentsToCsv() {
  if (state.tickets.length === 0) {
    alert(state.lang === "kn" ? "ರಫ್ತು ಮಾಡಲು ಯಾವುದೇ ಘಟನೆಗಳಿಲ್ಲ." :
          state.lang === "hi" ? "कतार में निर्यात करने के लिए कोई घटना नहीं है।" :
          "No incidents in queue to export.");
    return;
  }
  const headers = ["ID", "Priority", "Category", "Location", "Department", "Status", "Summary", "Reported Text"];
  const rows = state.tickets.map(t => [
    t.id,
    t.priority,
    (t.category || "General").replace("_", " "),
    t.location || "Unknown",
    t.department || "General",
    t.done ? "Resolved" : "Open",
    `"${(t.summary || "").replace(/"/g, '""')}"`,
    `"${(t.text || "").replace(/"/g, '""')}"`
  ]);
  const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(r => r.join(","))].join("\r\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `campus_pulse_incidents_${Date.now()}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
window.exportIncidentsToCsv = exportIncidentsToCsv;

function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[m]));
}

// Start app
init();
