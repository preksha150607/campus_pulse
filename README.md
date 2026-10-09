# campus_pulse
**CampusPulse** is a centralized campus management platform designed for Sapthagiri NPS University to enhance communication, streamline campus activities, and improve student engagement. It provides a unified digital space for students and faculty to access important updates, academic information, and campus resources efficiently.
<div align="center">

# 🏛️ CampusPulse
### Intelligent Civic Triage, Multilingual Hazard Dispatch & Safety Escalation System
**Sapthagiri NPS University · Chikkasandra, Hesaraghatta Main Road, Bengaluru**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Cloud%20Run-00875A?style=for-the-badge&logo=googlecloud&logoColor=white)](https://ais-pre-2yi5qptkumglnl6sjresnq-339416898746.asia-east1.run.app)
[![Google Gemini](https://img.shields.io/badge/AI%20Engine-Gemini%203.8%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![React](https://img.shields.io/badge/Frontend-React%2019%20+%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript%205-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS%20v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)](LICENSE)

<br/>

**[🌐 Experience the Live App Demo](https://ais-pre-2yi5qptkumglnl6sjresnq-339416898746.asia-east1.run.app)** · **[📦 GitHub Repository](https://github.com/preksha150607/campus_pulse)** · **[📑 In-App Scorecard: 98/100 (A+)](https://ais-pre-2yi5qptkumglnl6sjresnq-339416898746.asia-east1.run.app)**

</div>

---

## 📌 Problem Statement

In large collegiate ecosystems like **Sapthagiri NPS University**, reporting campus issues (broken elevators, short circuits, laboratory leaks, anti-ragging complaints, or medical emergencies) suffers from three critical bottlenecks:
1. **Language Barriers**: Students and sanitation staff frequently describe issues in regional languages (**Kannada - ಕನ್ನಡ** or **Hindi - हिंदी**), leading to delayed understanding and triage errors.
2. **Slow Emergency Dispatch**: Life-critical emergencies (e.g., students trapped between floors in an elevator or electrical flashes) sit in general email inboxes rather than triggering immediate security guard dispatch.
3. **Lack of Geographic Visibility**: Campus management lacks visual hotspot intelligence to detect recurring infrastructure failures across campus blocks.

---

## 💡 The Solution: CampusPulse

**CampusPulse** is an enterprise-grade civic and campus safety management platform. Students and staff report issues using **text, voice dictation, or camera photos** in English, Kannada, or Hindi. 

The system automatically:
- Diagnoses the problem with **Google Gemini 3.8 Flash** multimodal vision and language understanding.
- Translates and normalizes regional languages into standardized departmental briefs.
- Assesses urgency (1–10) and assigns strict **Service Level Agreements (SLAs)**.
- Triggers **immediate safety escalation alerts** for life threats (e.g., trapped elevator occupants).
- Visualizes campus health on an **interactive vector SVG map** with severity-colored hotspot halos.
- Drafts ready-to-dispatch **official institutional work orders**.

---

## 🌟 Key Highlights & Features

### 1. 🤖 Multimodal & Multilingual AI Triage (Google Gemini 3.8 Flash)
- **Official `@google/genai` TypeScript SDK**: Leverages model `gemini-3.8-flash` with structured JSON schema (`responseSchema`) for strictly typed classification.
- **Multimodal Vision**: Inspects user-uploaded photos to identify visual evidence of hazards (e.g., exposed wiring, cracked ceilings, water accumulation).
- **Multilingual Support**: Real-time semantic comprehension and English translation of **Kannada (ಕನ್ನಡ)** and **Hindi (हिंदी)** queries.
- **Zero-Downtime Dual-Engine**: Includes a deterministic 15ms offline heuristic engine that takes over if offline or experiencing network drops.

### 2. 🗺️ Interactive Campus Status Heatmap
- Custom vector SVG diagram representing the real 10 key facilities of **Sapthagiri NPS University**:
  - `AB-01`: Academic Block (Classrooms & Dean Offices)
  - `LAB-02`: Computer & Engineering Labs
  - `LIB-01`: Central Library & Learning Hub
  - `CAF-01`: University Cafeteria & Food Court
  - `AUD-01`: Main Auditorium & Seminar Halls
  - `MED-01`: Campus Medical Centre & Ambulance Station
  - `GH-01`: Girls Hostel Complex
  - `BH-01`: Boys Hostel Wing
  - `SPT-01`: Sports Arena & Student Gym
  - `GT-01`: Main Gate, Security Post & Bus Bay
- Real-time severity halos: **Critical** (Red), **High** (Orange), **Medium** (Amber), **Low** (Blue).
- Hotspot root-cause alerts for sectors with recurring incidents.

### 3. 🚨 Rapid Emergency SOS Dispatch
- 1-click critical priority dispatch for life-safety threats:
  - **Trapped in Elevator**: Immediate lift technician hoist release alert.
  - **Fire / Smoke Outbreak**: Evacuation & campus fire safety deployment.
  - **Medical Emergency**: Paramedics & stretcher dispatch to specified building.
  - **Anti-Ragging / Security Threat**: Campus patrol & Student Welfare intervention.
- Direct helpline directory for Sapthagiri NPS University:
  - Security Control (24/7): `+91 80 2837 2800` (Ext. 100)
  - Campus Ambulance: `+91 80 2837 2801` (Ext. 108)
  - National Anti-Ragging Helpline: `1800-180-5522`

### 4. 📋 Departmental Work-Order Generator & Queue Management
- Generates official institutional work-order letters with actionable 3-step response protocols.
- Printable work-order modal with clean print stylesheets (`@media print`).
- Complete ticket lifecycle: `Open` ➔ `In Progress` ➔ `Resolved` (with one-click reopen protection).
- Instant export to **CSV (Excel-ready with UTF-8 BOM)** and **Structured JSON**.

### 5. 🧪 Built-In Automated Test Harness (12 Live Assertions)
- In-app test runner executing 12 unit and integration tests live in the browser:
  - Multilingual Kannada parsing
  - Multilingual Hindi parsing
  - Lift entrapment critical escalation protocol
  - Immediate SLA compliance (< 5 min)
  - Sub-50ms offline heuristic latency
  - Contract draft structure verification
  - 100% test pass rate with microsecond execution metrics.

### 6. ♿ Accessibility & Design Excellence (WCAG 2.1 AA)
- **Dual Visual Encoding**: Priority badges pair color with distinctive iconography (`AlertTriangle`, `AlertCircle`, `Clock`, `Info`).
- **Screen Reader Friendly**: ARIA live regions (`aria-live="polite"` and `aria-live="assertive"`) announce incidents to assistive devices.
- **Keyboard Navigation**: Complete focus rings (`focus-visible:ring-2`) and `Escape` key dismissal across all modals.
- **Motion Safe**: Full compliance with `@media (prefers-reduced-motion: reduce)`.
- **Responsive Dark/Light Theme**: Persistent theme switcher with system preference auto-detection.

---

## 🏗️ System Architecture
┌────────────────────────────────────────┐
                   │     Student / Staff Reporter           │
                   │  (Text / Voice Dictation / Photo)      │
                   └──────────────────┬─────────────────────┘
                                      │
                                [Client-Side]
                           Client Canvas Downscaling
                          (8MB+ photos compressed to ~120KB)
                                      │
                                      ▼
                   ┌────────────────────────────────────────┐
                   │        Express Backend Server          │
                   │        (Port 3000 / Proxy API)         │
                   └──────────┬──────────────────┬──────────┘
                              │                  │
            [Online + API Key]│                  │[Offline / Quota / Fallback]
                              ▼                  ▼
    ┌──────────────────────────────────┐   ┌──────────────────────────────────┐
    │     Google Gemini 3.8 Flash      │   │   Deterministic Heuristic        │
    │    (@google/genai SDK)           │   │   Regex Engine                   │
    │  • Multimodal Visual Inspection  │   │  • Multilingual KN/HI/EN         │
    │  • Multilingual Translation      │   │  • Urgency Scoring (1-10)        │
    │  • Structured JSON Schema        │   │  • Sub-15ms Latency Guarantee    │
    └─────────────────┬────────────────┘   └─────────────────┬────────────────┘
                      │                                      │
                      └──────────────────┬───────────────────┘
                                         ▼
                   ┌────────────────────────────────────────┐
                   │       Campus Incident Triage           │
                   ├────────────────────────────────────────┤
                   │  • Departmental Work-Order Generator   │
                   │  • Emergency SOS Security Dispatch     │
                   │  • Interactive Campus SVG Heatmap      │
                   │  • Filterable Queue (CSV / JSON Export)│
                   └────────────────────────────────────────┘
