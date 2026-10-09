import os

import streamlit as st

from triage import DEFAULT_MODEL, triage

st.set_page_config(page_title="CampusPulse · Multi-lingual Triage", page_icon="🏫", layout="wide")

DEFAULT_PLACES = """Main Gate & Bus Bay
Academic Block
Computer Labs
Library
Cafeteria
Auditorium
Medical Centre
Girls Hostel
Boys Hostel
Sports Ground & Gym"""

UI_LANG = {
    "English": {
        "title": "CampusPulse",
        "subtitle": "Sapthagiri NPS University · Multi-lingual Incident Reporting & Hazard Dispatch",
        "settings": "Settings",
        "api_key": "Gemini API key",
        "model": "Model",
        "use_ai": "Use Gemini AI",
        "use_ai_help": "Turn off to demo the rules-only fallback",
        "campus_places": "Campus places",
        "campus_places_help": "One per line. Edit to match the real campus.",
        "report_header": "Report an issue",
        "problem_label": "What is the problem?",
        "problem_placeholder": "Lift stuck between floors in the Academic Block, two people inside...",
        "quick_chips_label": "Quick Templates:",
        "quick_chips": [
            ("🚨 Stuck in Lift", "Lift stuck between floors in the Academic Block, two people inside"),
            ("🔥 Smoke in Lab", "Smoke coming from the AC in the Computer Lab, students are leaving"),
            ("💧 Water Leak", "Severe tap leaking and water flooding in the cafeteria wash area"),
            ("📶 Library Wi-Fi", "Wi-Fi keeps dropping in the library reading hall"),
        ],
        "photo_label": "Photo (optional)",
        "cam_expander": "Or take a photo with the camera",
        "submit_btn": "Analyse and submit",
        "empty_warning": "Describe the issue or add a photo first.",
        "analyzing": "Analysing incident with multimodal AI...",
        "safety_alert": "🚨 Safety Escalation: Campus security and emergency teams alerted!",
        "metrics_priority": "Priority",
        "metrics_category": "Category",
        "metrics_sla": "Response target",
        "dept_label": "Department",
        "location_label": "Location",
        "lang_label": "Detected Language",
        "summary_label": "AI Summary",
        "photo_note_label": "Photo Analysis",
        "rules_raised": "Priority was elevated to ensure immediate safety compliance.",
        "reply_header": "Reply to the reporter (Localized)",
        "draft_header": "Drafted institutional work order",
        "open_stat": "Open",
        "critical_stat": "Critical Safety",
        "resolved_stat": "Resolved",
        "cluster_header": "Location Cluster Analysis",
        "cluster_alert": "has {n} open issues. Repeated reports often share a cause, dispatch a unified response team.",
        "queue_header": "Open queue",
        "no_reports": "No reports yet. Submit one on the left.",
        "resolve_btn": "Resolve",
        "resolved_badge": "Resolved ✓",
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "ಕ್ಯಾಂಪಸ್‌ಪಲ್ಸ್ (CampusPulse)",
        "subtitle": "ಸಪ್ತಗಿರಿ ಎನ್‌ಪಿಎಸ್ ವಿಶ್ವವಿದ್ಯಾಲಯ · ಬಹುಭಾಷಾ ಘಟನೆ ವರದಿ ಮತ್ತು ತುರ್ತು ರವಾನೆ ವ್ಯವಸ್ಥೆ",
        "settings": "ಸಂಯೋಜನೆಗಳು (Settings)",
        "api_key": "ಜೆಮಿನಿ ಎಪಿಐ ಕೀಲಿ (Gemini API Key)",
        "model": "ಮಾದರಿ (Model)",
        "use_ai": "ಜೆಮಿನಿ ಎಐ ಬಳಸಿ (Use Gemini)",
        "use_ai_help": "ನಿಯಮ-ಆಧಾರಿತ ಬ್ಯಾಕಪ್ ನೋಡಲು ಆಫ್ ಮಾಡಿ",
        "campus_places": "ಕ್ಯಾಂಪಸ್ ಸ್ಥಳಗಳು",
        "campus_places_help": "ಪ್ರತಿ ಸಾಲಿಗೆ ಒಂದರಂತೆ ನಮೂದಿಸಿ.",
        "report_header": "ಸಮಸ್ಯೆಯನ್ನು ವರದಿ ಮಾಡಿ",
        "problem_label": "ಸಮಸ್ಯೆ ಏನು?",
        "problem_placeholder": "ಅಕಾಡೆಮಿಕ್ ಬ್ಲಾಕ್‌ನಲ್ಲಿ ಲಿಫ್ಟ್ ಮಧ್ಯದಲ್ಲಿ ಸಿಕ್ಕಿಹಾಕಿಕೊಂಡಿದೆ, ಇಬ್ಬರು ಒಳಗಿದ್ದಾರೆ...",
        "quick_chips_label": "ತ್ವರಿತ ಮಾದರಿಗಳು:",
        "quick_chips": [
            ("🚨 ಲಿಫ್ಟ್‌ನಲ್ಲಿ ಸಿಲುಕಿದ್ದಾರೆ", "ಅಕಾಡೆಮಿಕ್ ಬ್ಲಾಕ್‌ನಲ್ಲಿ ಲಿಫ್ಟ್ ಮಧ್ಯದಲ್ಲಿ ಸಿಕ್ಕಿಹಾಕಿಕೊಂಡಿದೆ, ಇಬ್ಬರು ಒಳಗಿದ್ದಾರೆ"),
            ("🔥 ಲ್ಯಾಬ್‌ನಲ್ಲಿ ಹೊಗೆ", "ಕಂಪ್ಯೂಟರ್ ಲ್ಯಾಬ್‌ನಲ್ಲಿ ಎಸಿ ಯಿಂದ ಹೊಗೆ ಬರುತ್ತಿದೆ, ವಿದ್ಯಾರ್ಥಿಗಳು ಹೊರಬರುತ್ತಿದ್ದಾರೆ"),
            ("💧 ನೀರು ಸೋರಿಕೆ", "ಕ್ಯಾಂಟೀನ್ ವಾಶ್ ಪ್ರದೇಶದಲ್ಲಿ ಪೈಪ್ ಒಡೆದು ನೀರು ಸೋರುತ್ತಿದೆ"),
            ("📶 ಲೈಬ್ರರಿ ವೈಫೈ", "ಲೈಬ್ರರಿ ರೀಡಿಂಗ್ ಹಾಲ್‌ನಲ್ಲಿ ವೈಫೈ ಸಂಪರ್ಕ ಕಡಿತಗೊಳ್ಳುತ್ತಿದೆ"),
        ],
        "photo_label": "ಭಾವಚಿತ್ರ (ಐಚ್ಛಿಕ)",
        "cam_expander": "ಅಥವಾ ಕ್ಯಾಮೆರಾ ಮೂಲಕ ಫೋಟೋ ತೆಗೆಯಿರಿ",
        "submit_btn": "ವಿಶ್ಲೇಷಿಸಿ ಮತ್ತು ಸಲ್ಲಿಸಿ",
        "empty_warning": "ದಯವಿಟ್ಟು ಸಮಸ್ಯೆಯನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಫೋಟೋ ಸೇರಿಸಿ.",
        "analyzing": "ಬಹುಭಾಷಾ ಎಐ ಮೂಲಕ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
        "safety_alert": "🚨 ತುರ್ತು ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ: ಕ್ಯಾಂಪಸ್ ಭದ್ರತಾ ಸಿಬ್ಬಂದಿಗೆ ಮಾಹಿತಿ ನೀಡಲಾಗಿದೆ!",
        "metrics_priority": "ಆದ್ಯತೆ",
        "metrics_category": "ವರ್ಗ",
        "metrics_sla": "ಪ್ರತಿಕ್ರಿಯೆ ಗುರಿ",
        "dept_label": "ಜವಾಬ್ದಾರಿಯುತ ಇಲಾಖೆ",
        "location_label": "ಸ್ಥಳ",
        "lang_label": "ಪತ್ತೆಯಾದ ಭಾಷೆ",
        "summary_label": "ಸಾರಾಂಶ",
        "photo_note_label": "ಫೋಟೋ ವಿವರಣೆ",
        "rules_raised": "ಸುರಕ್ಷತಾ ನಿಯಮಗಳ ಅಡಿಯಲ್ಲಿ ಆದ್ಯತೆಯನ್ನು ಹೆಚ್ಚಿಸಲಾಗಿದೆ.",
        "reply_header": "ವರದಿದಾರರಿಗೆ ಸ್ಥಳೀಯ ಪ್ರತ್ಯುತ್ತರ",
        "draft_header": "ಸಿದ್ಧಪಡಿಸಿದ ಅಧಿಕೃತ ದೂರು ಇಮೇಲ್",
        "open_stat": "ತೆರೆದಿರುವ ದೂರುಗಳು",
        "critical_stat": "ತುರ್ತು ಅಪಾಯ",
        "resolved_stat": "ಪರಿಹರಿಸಲಾಗಿದೆ",
        "cluster_header": "ಸ್ಥಳೀಯ ಘಟನೆಗಳ ವಿಶ್ಲೇಷಣೆ (Cluster)",
        "cluster_alert": "ಭಾಗದಲ್ಲಿ {n} ಸಮಸ್ಯೆಗಳು ದಾಖಲಾಗಿವೆ. ಪುನರಾವರ್ತಿತ ಘಟನೆಗಳಿಗೆ ಒಂದೇ ತಂಡವನ್ನು ಕಳುಹಿಸಿ.",
        "queue_header": "ಘಟನೆಗಳ ಸರದಿ (Queue)",
        "no_reports": "ಇನ್ನೂ ಯಾವುದೇ ದೂರುಗಳಿಲ್ಲ. ಎಡಭಾಗದಲ್ಲಿ ಸಲ್ಲಿಸಿ.",
        "resolve_btn": "ಪರಿಹರಿಸಿ",
        "resolved_badge": "ಪರಿಹರಿಸಲಾಗಿದೆ ✓",
    },
    "हिंदी (Hindi)": {
        "title": "कैंपसपल्स (CampusPulse)",
        "subtitle": "सप्तगिरि एनपीएस विश्वविद्यालय · बहुभाषी घटना रिपोर्टिंग और आपातकालीन प्रेषण प्रणाली",
        "settings": "सेटिंग्स (Settings)",
        "api_key": "जेमिनी एपीआई कुंजी (Gemini API Key)",
        "model": "मॉडल (Model)",
        "use_ai": "जेमिनी एआई का उपयोग करें",
        "use_ai_help": "नियम-आधारित बैकअप देखने के लिए बंद करें",
        "campus_places": "परिसर स्थल (Campus Places)",
        "campus_places_help": "प्रति पंक्ति एक स्थल दर्ज करें।",
        "report_header": "समस्या की रिपोर्ट करें",
        "problem_label": "समस्या क्या है?",
        "problem_placeholder": "अकादमिक ब्लॉक में लिफ्ट मंजिलों के बीच फंस गई है, दो लोग अंदर हैं...",
        "quick_chips_label": "त्वरित टेम्पलेट:",
        "quick_chips": [
            ("🚨 लिफ्ट में फंसे लोग", "अकादमिक ब्लॉक में लिफ्ट मंजिलों के बीच फंस गई है, दो लोग अंदर हैं"),
            ("🔥 लैब में धुआं", "कंप्यूटर लैब में एसी से धुआं निकल रहा है, छात्र बाहर निकल रहे हैं"),
            ("💧 पानी का रिसाव", "कैंटीन वॉश एरिया में पाइप से पानी का भारी रिसाव हो रहा है"),
            ("📶 लाइब्रेरी वाई-फाई", "लाइब्रेरी रीडिंग हॉल में वाई-फाई बार-बार डिस्कनेक्ट हो रहा है"),
        ],
        "photo_label": "फोटो (वैकल्पिक)",
        "cam_expander": "या कैमरे से फोटो लें",
        "submit_btn": "विश्लेषण करें और सबमिट करें",
        "empty_warning": "कृपया पहले समस्या का वर्णन करें या फोटो जोड़ें।",
        "analyzing": "बहुभाषी एआई द्वारा विश्लेषण हो रहा है...",
        "safety_alert": "🚨 सुरक्षा आपातकालीन चेतावनी: परिसर सुरक्षा दल को सतर्क कर दिया गया है!",
        "metrics_priority": "प्राथमिकता",
        "metrics_category": "श्रेणी",
        "metrics_sla": "प्रतिक्रिया समय",
        "dept_label": "संबंधित विभाग",
        "location_label": "स्थान",
        "lang_label": "पहचानी गई भाषा",
        "summary_label": "संक्षिप्त विवरण",
        "photo_note_label": "फोटो अवलोकन",
        "rules_raised": "सुरक्षा नियमों के आधार पर प्राथमिकता बढ़ाई गई।",
        "reply_header": "रिपोर्टर को स्थानीय भाषा में जवाब",
        "draft_header": "आधिकारिक शिकायत ईमेल प्रारूप",
        "open_stat": "लंबित शिकायतें",
        "critical_stat": "अति गंभीर",
        "resolved_stat": "सुलझाया गया",
        "queue_header": "घटना कतार (Queue)",
        "cluster_header": "घटना संकुल विश्लेषण (Cluster Analysis)",
        "cluster_alert": "में {n} खुली समस्याएं हैं। एक संयुक्त दल भेजें।",
        "no_reports": "अभी तक कोई रिपोर्ट नहीं है। बाईं ओर से सबमिट करें।",
        "resolve_btn": "सुलझाएं",
        "resolved_badge": "सुलझाया गया ✓",
    },
    "मराठी (Marathi)": {
        "title": "कॅम्पसपल्स (CampusPulse)",
        "subtitle": "सप्तगिरी एनपीएस विद्यापीठ · बहुभाषिक घटना तक्रार आणि सुरक्षा व्यवस्थापन",
        "settings": "सेटिंग्ज (Settings)",
        "api_key": "जेमिनी एपीआय की (Gemini API Key)",
        "model": "मॉडेल (Model)",
        "use_ai": "जेमिनी एआय वापरा",
        "use_ai_help": "नियम-आधारित बॅकअप पाहण्यासाठी बंद करा",
        "campus_places": "कॅम्पस ठिकाणे",
        "campus_places_help": "प्रत्येक ओळीवर एक ठिकाण प्रविष्ट करा.",
        "report_header": "समस्येची नोंद करा",
        "problem_label": "समस्या काय आहे?",
        "problem_placeholder": "अकॅडेमिक ब्लॉकमध्ये लिफ्ट अडकली आहे, दोन जण आत आहेत...",
        "quick_chips_label": "जलद नमुने:",
        "quick_chips": [
            ("🚨 लिफ्टमध्ये अडकले", "अकॅडेमिक ब्लॉकमध्ये लिफ्ट अडकली आहे, दोन जण आत आहेत"),
            ("🔥 लॅबमध्ये धूर", "कॉम्प्युटर लॅबमध्ये एसीतून धूर येत आहे, विद्यार्थी बाहेर पडत आहेत"),
            ("💧 पाण्याची गळती", "कॅन्टीन वॉश भागात पाईप फुटून पाणी वाहत आहे"),
            ("📶 लायब्ररी वाय-फाय", "लायब्ररी रीडिंग हॉलमध्ये वाय-फाय वारंवार बंद पडत आहे"),
        ],
        "photo_label": "छायाचित्र (पर्यायी)",
        "cam_expander": "किंवा कॅमेऱ्याने फोटो घ्या",
        "submit_btn": "विश्लेषण करा आणि सबमिट करा",
        "empty_warning": "कृपया समस्येचे वर्णन करा किंवा फोटो जोडा.",
        "analyzing": "बहुभाषिक एआय द्वारे विश्लेषण करत आहे...",
        "safety_alert": "🚨 सुरक्षा आणीबाणी इशारा: कॅम्पस सुरक्षा रक्षकांना सतर्क केले गेले आहे!",
        "metrics_priority": "प्राधान्य",
        "metrics_category": "वर्ग",
        "metrics_sla": "प्रतिसाद उद्दिष्ट",
        "dept_label": "जबाबदार विभाग",
        "location_label": "ठिकाण",
        "lang_label": "ओळखलेली भाषा",
        "summary_label": "सारांश",
        "photo_note_label": "छायाचित्र निरीक्षण",
        "rules_raised": "सुरक्षा नियमांनुसार प्राधान्य वाढवले आहे.",
        "reply_header": "तक्रारदारास स्थानिक भाषेत उत्तर",
        "draft_header": "अधिकृत तक्रार ईमेल मसुदा",
        "open_stat": "प्रलंबित तक्रारी",
        "critical_stat": "गंभीर",
        "resolved_stat": "सोडवले",
        "cluster_header": "घटना क्लस्टर विश्लेषण",
        "cluster_alert": "मध्ये {n} प्रलंबित समस्या आहेत. एकत्रित पथक पाठवा.",
        "queue_header": "घटना रांग (Queue)",
        "no_reports": "अजून कोणतीही तक्रार नाही. डावीकडे सबमिट करा.",
        "resolve_btn": "सोडवा",
        "resolved_badge": "सोडवले ✓",
    }
}

# Sidebar settings
with st.sidebar:
    selected_lang = st.selectbox(
        "🌐 Language / ಭಾಷೆ / भाषा",
        ["English", "ಕನ್ನಡ (Kannada)", "हिंदी (Hindi)", "मराठी (Marathi)"],
        index=0
    )
    t = UI_LANG[selected_lang]

    st.header(t["settings"])
    secret_key = ""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            secret_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    default_key = os.getenv("GEMINI_API_KEY") or secret_key
    api_key = st.text_input(t["api_key"], value=default_key, type="password")
    model = st.text_input(t["model"], value=DEFAULT_MODEL)
    use_ai = st.toggle(t["use_ai"], value=True, help=t["use_ai_help"])
    with st.expander("🚨 Emergency Hotlines (Sapthagiri NPS)", expanded=False):
        st.markdown("**Security Control (24/7):** `+91 80 2837 2800 (Ext. 100)`  \n"
                    "**Campus Ambulance:** `+91 80 2837 2801 (Ext. 108)`  \n"
                    "**National Anti-Ragging:** `1800-180-5522`  \n"
                    "**Hostel Warden Desk:** `+91 80 2837 2802 (Ext. 104)`")
    st.subheader(t["campus_places"])
    places_text = st.text_area(t["campus_places_help"], value=DEFAULT_PLACES, height=180)

places = [p.strip() for p in places_text.splitlines() if p.strip()]

# Header layout
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.title(t["title"])
    st.caption(t["subtitle"])
with head_col2:
    st.write("")
    st.info(f"Active UI: **{selected_lang}**")

if "tickets" not in st.session_state:
    st.session_state.tickets = []
    st.session_state.nid = 1

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

left, right = st.columns([1, 1.1], gap="large")

with left:
    st.subheader(t["report_header"])

    # Quick template buttons
    st.caption(t["quick_chips_label"])
    chip_cols = st.columns(len(t["quick_chips"]))
    for i, (chip_label, chip_val) in enumerate(t["quick_chips"]):
        if chip_cols[i].button(chip_label, key=f"chip_{i}", use_container_width=True):
            st.session_state.input_text = chip_val
            st.rerun()

    text = st.text_area(
        t["problem_label"],
        value=st.session_state.input_text,
        height=110,
        placeholder=t["problem_placeholder"],
        key="main_problem_text"
    )
    st.session_state.input_text = text

    photo = st.file_uploader(t["photo_label"], type=["png", "jpg", "jpeg", "webp"])
    with st.expander(t["cam_expander"]):
        cam = st.camera_input("Camera")
    img = photo or cam
    if img:
        st.image(img, width=220)

    if st.button(t["submit_btn"], type="primary", use_container_width=True):
        if not text.strip() and not img:
            st.warning(t["empty_warning"])
        else:
            with st.spinner(t["analyzing"]):
                r = triage(text.strip(), img.getvalue() if img else None,
                           getattr(img, "type", None), places, api_key, model, use_ai)
            r["id"], r["text"], r["done"] = st.session_state.nid, text.strip() or "Photo report", False
            r["img"] = img.getvalue() if img else None
            st.session_state.nid += 1
            st.session_state.tickets.insert(0, r)
            st.session_state.last = r
            st.session_state.input_text = ""
            st.rerun()

    r = st.session_state.get("last")
    if r:
        st.divider()
        if r["error"]:
            st.warning(f"Gemini fallback notice: ({r['error'][:160]})")
        if r["priority"] == "Critical":
            st.error(f"{t['safety_alert']} " + (r["reply_to_reporter"] if r.get("people_at_risk") else ""))
            if r.get("emergency_hotline"):
                st.warning(f"📞 Immediate Dispatch Contact: **{r['emergency_hotline']}**")

        pri_icons = {"Critical": "🚨 Critical", "High": "⚠️ High", "Medium": "🟡 Medium", "Low": "🟢 Low"}
        c1, c2, c3 = st.columns(3)
        c1.metric(t["metrics_priority"], pri_icons.get(r["priority"], r["priority"]))
        c2.metric(t["metrics_category"], r["category"].replace("_", " ").title())
        c3.metric(t["metrics_sla"], r["sla"])
        fac_code = f" [{r.get('facility_code', 'GEN')}]" if r.get("facility_code") else ""
        st.write(f"**{t['dept_label']}:** {r['department']}  \n"
                 f"**{t['location_label']}:** {r['location']}{fac_code}  \n"
                 f"**{t['lang_label']}:** {r['language']}  \n"
                 f"**{t['summary_label']}:** {r['summary']}")
        if r.get("photo_note"):
            st.write(f"**{t['photo_note_label']}:** {r['photo_note']}")
        if r.get("raised_by_rules"):
            st.info(t["rules_raised"])
        st.caption(f"Triage Source: {r['source']}")
        st.markdown(f"**{t['reply_header']}**")
        st.info(r["reply_to_reporter"])
        st.markdown(f"**{t['draft_header']}**")
        st.code(r["complaint_draft"], language=None)

with right:
    tickets = st.session_state.tickets
    open_t = [tk for tk in tickets if not tk["done"]]
    a, b, c = st.columns(3)
    a.metric(t["open_stat"], len(open_t))
    b.metric(t["critical_stat"], sum(tk["priority"] == "Critical" for tk in open_t))
    c.metric(t["resolved_stat"], len(tickets) - len(open_t))

    if open_t:
        st.subheader(t["cluster_header"])
        by_loc = {}
        for tk in open_t:
            by_loc[tk["location"]] = by_loc.get(tk["location"], 0) + 1
        for loc, n in sorted(by_loc.items(), key=lambda kv: -kv[1]):
            st.progress(n / max(by_loc.values()), text=f"{loc}: {n}")
        top = max(by_loc, key=by_loc.get)
        if by_loc[top] > 1 and top != "unknown":
            st.info(f"⚠️ {top} {t['cluster_alert'].format(n=by_loc[top])}")

    st.subheader(t["queue_header"])
    if not tickets:
        st.write(t["no_reports"])
    else:
        # CSV Export for administrators
        import csv
        import io as csv_io
        csv_buf = csv_io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(["ID", "Priority", "Category", "Location", "Department", "Status", "Summary", "Reported Text"])
        for tk in tickets:
            writer.writerow([
                tk["id"], tk["priority"], tk["category"], tk["location"],
                tk.get("department", "General"), "Resolved" if tk["done"] else "Open",
                tk.get("summary", ""), tk["text"]
            ])
        st.download_button(
            "📥 Export Incidents to CSV (Excel-ready)",
            data=csv_buf.getvalue().encode("utf-8-sig"),
            file_name="campus_pulse_incidents.csv",
            mime="text/csv",
            use_container_width=True
        )

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    pri_badge = {"Critical": "🚨 Critical", "High": "⚠️ High", "Medium": "🟡 Medium", "Low": "🟢 Low"}
    for tk in sorted(tickets, key=lambda item: (item["done"], order.get(item["priority"], 4))):
        with st.container(border=True):
            cols = st.columns([1, 5, 2])
            if tk.get("img"):
                cols[0].image(tk["img"], width=60)
            badge_text = pri_badge.get(tk["priority"], tk["priority"])
            cols[1].markdown(f"**{badge_text}** · {tk['category'].replace('_', ' ').title()} · 📍 {tk['location']}  \n{tk['text']}")
            if not tk["done"] and cols[2].button(t["resolve_btn"], key=f"r{tk['id']}"):
                tk["done"] = True
                st.rerun()
            elif tk["done"]:
                cols[2].write(t["resolved_badge"])
