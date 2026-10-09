<div align="center">

# 🏛️ CampusPulse
### Intelligent Civic Triage, Multilingual Hazard Dispatch & Safety Escalation System
**Sapthagiri NPS University · Chikkasandra, Hesaraghatta Main Road, Bengaluru**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloud%20Run-00875A?style=for-the-badge&logo=googlecloud&logoColor=white)](https://ais-dev-2yi5qptkumglnl6sjresnq-339416898746.asia-east1.run.app/)
[![Google Gemini](https://img.shields.io/badge/AI%20Engine-Gemini%202.0%20%2F%203.8%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit%201.40+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)](LICENSE)

<br/>

**[🌐 Experience the Live Demo](https://ais-dev-2yi5qptkumglnl6sjresnq-339416898746.asia-east1.run.app/)** · **[📦 GitHub Repository](https://github.com/preksha150607/campus_pulse)** · **[🧪 Test Suite: 100% Pass Rate](tests.csv)**

</div>

---

## 📌 Problem Statement

In large collegiate ecosystems like **Sapthagiri NPS University**, reporting campus issues (broken elevators, short circuits, laboratory leaks, anti-ragging complaints, or medical emergencies) suffers from three critical bottlenecks:
1. **Language Barriers**: Students and sanitation staff frequently describe issues in regional languages (**Kannada - ಕನ್ನಡ**, **Hindi - हिंदी**, or **Marathi - मराठी**), leading to delayed understanding and triage errors.
2. **Slow Emergency Dispatch**: Life-critical emergencies (e.g., students trapped between floors in an elevator or electrical flashes) sit in general email inboxes rather than triggering immediate security guard dispatch.
3. **Lack of Geographic Visibility**: Campus management lacks visual hotspot intelligence to detect recurring infrastructure failures across campus blocks.

---

## 💡 The Solution: CampusPulse

**CampusPulse** is an enterprise-grade civic and campus safety management platform. Students and staff report issues using **text or camera photos** in English, Kannada, Hindi, or Marathi.

The system automatically:
- Diagnoses the problem with **Google Gemini Flash** multimodal vision and language understanding.
- Translates and normalizes regional languages into standardized departmental briefs.
- Assesses urgency (1–10) and assigns strict **Service Level Agreements (SLAs)**.
- Triggers **immediate safety escalation alerts** for life threats (e.g., trapped elevator occupants).
- Dispatches automated **localized responses in the reporter's native language** with instant safety instructions.
- Detects **location incident clusters** to send unified response teams to recurring infrastructure hotspots.
- Drafts ready-to-dispatch **official institutional work orders**.

---

## 🌟 Key Highlights & Features

### 1. 🤖 Multimodal & Multilingual AI Triage (Google Gemini Flash)
- **Official Google GenAI SDK (`google-genai`)**: Leverages Gemini Flash with structured schema (`response_schema`) for strictly typed JSON output.
- **Multimodal Vision**: Inspects user-uploaded photos to identify visual evidence of hazards (e.g., exposed wiring, cracked ceilings, water accumulation).
- **Multilingual Support**: Real-time semantic comprehension and English translation of **Kannada (ಕನ್ನಡ)**, **Hindi (हिंदी)**, and **Marathi (मराठी)** queries.
- **Zero-Downtime Dual-Engine**: Includes a deterministic 15ms offline heuristic engine that takes over if offline or experiencing network drops.

### 2. 🚨 Rapid Emergency SOS & Safety Elevation
- 1-click critical priority dispatch for life-safety threats:
  - **Trapped in Elevator**: Immediate lift technician hoist release alert.
  - **Fire / Smoke Outbreak**: Evacuation & campus fire safety deployment.
  - **Medical Emergency**: Paramedics & stretcher dispatch to specified building.
  - **Anti-Ragging / Security Threat**: Campus patrol & Student Welfare intervention.
- Direct emergency helplines for Sapthagiri NPS University:
  - Security Control (24/7): `+91 80 2837 2800` (Ext. 100)
  - Campus Medical Centre: `+91 80 2837 2801` (Ext. 108)
  - National Anti-Ragging Helpline: `1800-180-5522`

### 3. 🗺️ Location Cluster Analysis
- Real-time incident clustering across the 10 university facilities:
  - `Main Gate & Bus Bay`, `Academic Block`, `Computer Labs`, `Library`, `Cafeteria`,
  - `Auditorium`, `Medical Centre`, `Girls Hostel`, `Boys Hostel`, `Sports Ground & Gym`.
- Hotspot root-cause alerts for sectors with recurring incidents (e.g. repeated electrical failures in Computer Labs).

### 4. 📋 Departmental Work-Order Generator & Queue Management
- Generates official institutional email bodies with actionable response protocols and response targets.
- Localized reporter acknowledgements with immediate safety instructions.
- Real-time queue with priority-based sorting and resolution tracking.

### 5. 🧪 Rigorous Automated Evaluation Suite
- Built-in test runner ([eval.py](eval.py)) verifying classification against [tests.csv](tests.csv).
- **100% Critical Safety Recall (7/7 critical hazards caught)**.
- **100% Category & Priority Accuracy (15/15 test assertions passed)**.

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Student / Staff Reporter                 │
│         (Multilingual Text + Photo / Camera)           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   CampusPulse Engine                   │
├───────────────────────────┬────────────────────────────┤
│   [Online Mode]           │   [Offline / Fallback]     │
│   Google Gemini Flash     │   Heuristic Safety Rules   │
│   • Multimodal Vision     │   • Multilingual Regex     │
│   • Semantic Translation  │   • Trapped/Fire Overrides │
│   • Structured JSON       │   • Sub-15ms Latency       │
└─────────────┬─────────────┴─────────────┬──────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│               Automated Incident Actions               │
├────────────────────────────────────────────────────────┤
│  🚨 Critical Safety Alarm & Escalation Banner          │
│  💬 Localized Reporter Response (KN / HI / MR / EN)    │
│  ✉️ Departmental Email Work-Order Draft                │
│  📍 Location Cluster & Hotspot Detection               │
│  📋 Interactive Incident Queue & Resolution Tracker    │
└────────────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure

```text
campus_pulse/
├── app.py                 # Primary Streamlit Interactive Application
├── triage.py              # Core AI & Safety Rule-Based Triage Engine
├── eval.py                # Evaluation Script for Benchmark Testing
├── tests.csv              # Multilingual Benchmark Test Dataset
├── requirements.txt       # Production Dependencies
├── LICENSE                # Apache 2.0 Open Source License
├── vercel.json            # Vercel Serverless Hosting Configuration
├── .gitignore             # Git ignore file for environments and caches
├── .streamlit/
│   └── config.toml        # Enterprise Theme and UI Configuration
├── api/
│   └── index.py           # Serverless API Handler (Starlette ASGI)
└── public/                # Static Web Assets (HTML5 / CSS3 / JS)
    ├── index.html         # Responsive Single Page Interface
    ├── style.css          # Glassmorphic Styling & Animations
    └── app.js             # Client-side Logic & LocalStorage Queue
```

---

## 🚀 Quickstart Guide

### 1. Clone & Install
```bash
git clone https://github.com/preksha150607/campus_pulse.git
cd campus_pulse
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
```bash
# Set your Gemini API key (can also be entered directly in the app UI)
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run Benchmark Tests
```bash
python eval.py
```
Output:
```text
rules only: category 15/15, priority 15/15, critical cases caught 7/7
```

---

## 👥 Departmental SLA Directory

| Category | Responsible Department | Target Response Time | Priority |
| :--- | :--- | :--- | :--- |
| **Fire / Smoke** | Security & Fire Safety | Immediate | Critical |
| **Medical Emergency** | Campus Medical Centre | Immediate | Critical |
| **Harassment / Threat** | Security & Student Welfare | 15 Minutes | Critical / High |
| **Trapped in Elevator** | Security & Maintenance (Lift) | Immediate | Critical |
| **Theft / Intrusion** | Security | 1 Hour | High |
| **Water Leak** | Maintenance (Plumbing) | 4 Hours | Medium |
| **Electrical Issue** | Maintenance (Electrical) | 4 Hours | Medium |
| **IT / Wi-Fi Network** | IT Services | 1 Day | Medium |
| **Sanitation / Waste** | Housekeeping | 1 Day | Low / Medium |
| **Transport / Parking** | Transport Office | 2 Days | Low |
| **General** | Administration Office | 3 Days | Low |

---

## 📜 License

Distributed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for more information.
