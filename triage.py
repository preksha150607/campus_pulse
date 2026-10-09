"""CampusPulse triage: Gemini (text + photo) with a rule-based safety net."""
import json
import re
from typing import Literal

from pydantic import BaseModel

DEFAULT_MODEL = "gemini-2.0-flash"  # valid default Gemini flash model

CATS = ["fire", "medical", "harassment", "theft", "lift", "water_leak", "electrical",
        "it_network", "sanitation", "transport", "general"]
RANK = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}

# category -> (department, response target)
INFO = {
    "fire": ("Security & Fire Safety", "Immediate"),
    "medical": ("Campus Medical Centre", "Immediate"),
    "harassment": ("Security & Student Welfare", "15 min"),
    "theft": ("Security", "1 hour"),
    "lift": ("Maintenance (Lift)", "2 hours"),
    "water_leak": ("Maintenance (Plumbing)", "4 hours"),
    "electrical": ("Maintenance (Electrical)", "4 hours"),
    "it_network": ("IT Services", "1 day"),
    "sanitation": ("Housekeeping", "1 day"),
    "transport": ("Transport Office", "2 days"),
    "general": ("Administration Office", "3 days"),
}

# (category, base score, regex, is_safety)
RULES = [
    ("fire", 10, r"fire|smoke|spark|short.?circuit|आग|धुआं|चिंगारी|ಬೆಂಕಿ|ಹೊಗೆ|ಕಿಡಿ|धूर", 1),
    ("medical", 10, r"injur|accident|faint|bleed|unconscious|ambulance|chest pain|चोट|दुर्घटना|बेहोश|ಅಪಘಾತ|ಗಾಯ|ಪ್ರಜ್ಞೆ", 1),
    ("harassment", 9, r"harass|ragging|stalk|follow(ed|ing)|threat|fight|bully|unsafe|छेड़|धमकी|रैगिंग|पीछा|ಕಿರುಕುಳ|ಬೆದರಿಕೆ|ಹಿಂಬಾಲಿ|त्रास|पाठलाग", 1),
    ("theft", 7, r"theft|stolen|steal|suspicious|intruder|stranger|चोरी|ಕಳ್ಳತನ|ಅನುಮಾನ", 1),
    ("lift", 6, r"\blift\b|elevator|ಲಿಫ್ಟ್|ಎಲಿವೇಟರ್|लिफ्ट", 0),
    ("water_leak", 5, r"leak|pipe|tap|flood|overflow|seep|water|पानी|रिसाव|गळती|ನೀರು|ಸೋರಿಕೆ|ಸೋರು", 0),
    ("electrical", 5, r"power|electric|light|fan|\bac\b|projector|wire|socket|बिजली|पंखा|ವಿದ್ಯುತ್|ಕರೆಂಟ್|ಫ್ಯಾನ್|सॉकेट", 0),
    ("it_network", 4, r"wifi|wi-fi|internet|network|lms|portal|server|वाईफाई|वाय-फाय|ಇಂಟರ್ನೆಟ್|ವೈಫೈ", 0),
    ("sanitation", 2, r"garbage|dirty|toilet|washroom|smell|waste|trash|कचरा|गंदा|ಕಸ|ಶೌಚಾಲಯ", 0),
    ("transport", 2, r"\bbus\b|transport|route|parking|shuttle|बस|ಬಸ್", 0),
]
BOOST = re.compile(r"urgent|immediately|right now|emergency|many students|children|girls|wet|spreading|तुरंत|जल्दी|ಈಗಲೇ|ತುರ್ತು", re.I)
TRAP = re.compile(r"stuck|trapped|jammed|between floors|people inside|persons inside|अटक|फंस|अडकले|ಸಿಕ್ಕಿ|ಸಿಲುಕ", re.I)


def _pri(score: int) -> str:
    return "Critical" if score >= 9 else "High" if score >= 6 else "Medium" if score >= 3 else "Low"


def rules_triage(text: str) -> dict:
    best, base, safety = "general", 1, 0
    for cat, b, rx, sf in RULES:
        if re.search(rx, text or "", re.I) and b > base:
            best, base, safety = cat, b, sf
    score = base + (2 if BOOST.search(text or "") else 0)
    if best == "lift" and TRAP.search(text or ""):
        score, safety = 10, 1
    return {"category": best, "priority": _pri(min(score, 12)), "safety": bool(safety)}


class Triage(BaseModel):
    category: Literal[
        "fire", "medical", "harassment", "theft", "lift", "water_leak",
        "electrical", "it_network", "sanitation", "transport", "general"
    ]
    priority: Literal["Critical", "High", "Medium", "Low"]
    location: str
    language: str
    summary: str
    people_at_risk: bool
    photo_note: str
    complaint_draft: str
    reply_to_reporter: str


SYSTEM = """You triage problem reports for Sapthagiri NPS University, Bengaluru.
Reports arrive in English, Hindi, Kannada or Marathi, as text, a photo, or both.
Rules:
- category must be one of: """ + ", ".join(CATS) + """.
- priority: Critical = danger to life or safety happening now (fire, smoke, injury, someone trapped in a lift, threat or stalking);
  High = serious fault or safety risk but nobody in immediate danger (lift out of service, exposed wires, theft);
  Medium = disruptive fault (water leak, Wi-Fi, broken fan); Low = minor or cosmetic.
- When unsure between two priorities for a safety issue, choose the higher one.
- location must be exactly one name from the provided campus places, or "unknown". Never invent a place.
- Describe only what you can see or read. If the photo is blurry or unrelated, say so in photo_note and do not guess.
- language = language of the reporter's text (or "none" if photo only).
- summary: one plain English sentence.
- complaint_draft: a short, polite English email body to the responsible department.
- reply_to_reporter: a short acknowledgement written in the reporter's own language, with any immediate safety advice
  (for example: stay calm and press the lift alarm; move away from smoke). Do not promise a repair time.
Return only the JSON object."""


def gemini_triage(text, image, mime, places, api_key, model):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    parts = []
    if image:
        parts.append(types.Part.from_bytes(data=image, mime_type=mime or "image/jpeg"))
    parts.append(f"Campus places: {', '.join(places)}\nReport text: {text or '(no text, photo only)'}")
    resp = client.models.generate_content(
        model=model,
        contents=parts,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            response_mime_type="application/json",
            response_schema=Triage,
            temperature=0.2,
        ),
    )
    return resp.parsed.model_dump() if getattr(resp, "parsed", None) else json.loads(resp.text)


def _find_place(text, places):
    t = (text or "").lower()
    for p in places:
        if not p:
            continue
        pl = p.lower()
        if pl in t or (pl.endswith("s") and pl[:-1] in t):
            return p
    return "unknown"


def _detect_lang(text: str) -> str:
    if not text:
        return "English"
    if re.search(r"[\u0C80-\u0CFF]", text):
        return "Kannada"
    if re.search(r"[\u0900-\u097F]", text):
        if re.search(r"(आहे|आहेत|झाले|झाला|गळती|अडकले|नाही|करा|बघितले|त्रास|पाठलाग)", text):
            return "Marathi"
        return "Hindi"
    return "English"


LOCALIZED_REPLIES = {
    "Kannada": "ನಿಮ್ಮ ವರದಿಯನ್ನು ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ಸುರಕ್ಷತೆಯಾಗಿರಿ, ನಮ್ಮ ಕ್ಯಾಂಪಸ್ ತಂಡಕ್ಕೆ ಮಾಹಿತಿ ನೀಡಲಾಗಿದೆ.",
    "Hindi": "आपकी रिपोर्ट प्राप्त हो गई है। कृपया सुरक्षित रहें, परिसर सहायता टीम को सूचित कर दिया गया है।",
    "Marathi": "तुमची तक्रार नोंदवली गेली आहे. कृपया सुरक्षित रहा, कॅम्पस मदत पथकाला माहिती दिली आहे.",
    "English": "Your report has been received. Please stay safe, the campus support team has been alerted.",
}

LOCALIZED_EMERGENCY_REPLIES = {
    "Kannada": "🚨 ತುರ್ತು ರಕ್ಷಣೆ: ದಯವಿಟ್ಟು ಶಾಂತರಾಗಿರಿ. ಲಿಫ್ಟ್ ಅಲಾರಂ ಒತ್ತಿ, ಕ್ಯಾಂಪಸ್ ಭದ್ರತಾ ದಳವು ತಕ್ಷಣ ಧಾವಿಸುತ್ತಿದೆ.",
    "Hindi": "🚨 आपातकालीन चेतावनी: कृपया शांत रहें। लिफ्ट अलार्म दबाएं, परिसर सुरक्षा दल तुरंत पहुंच रहा है।",
    "Marathi": "🚨 आणीबाणी इशारा: कृपया शांत रहा. अलार्म बटण दाबा, कॅम्पस सुरक्षा पथक त्वरित पोहोचत आहे.",
    "English": "🚨 Emergency alert: Please remain calm. Trigger the alarm, campus security is en route.",
}


def triage(text="", image=None, mime=None, places=(), api_key=None, model=DEFAULT_MODEL, use_ai=True) -> dict:
    rules = rules_triage(text)
    ai, err = None, None
    detected_lang = _detect_lang(text)
    if use_ai and api_key:
        try:
            ai = gemini_triage(text, image, mime, list(places), api_key, model)
        except Exception as e:  # network, quota, bad model name, parse error
            err = f"{type(e).__name__}: {e}"
    raised = False
    if ai:
        cat = ai["category"] if ai["category"] in CATS else rules["category"]
        pri = ai["priority"]
        if text and rules["safety"] and RANK[rules["priority"]] > RANK[pri]:
            pri, raised = rules["priority"], True
        if text and rules["safety"] and cat not in ("fire", "medical", "harassment", "theft", "lift"):
            cat = rules["category"]
        loc = ai["location"] if ai["location"] in places else "unknown"
        out = {**ai, "category": cat, "priority": pri, "location": loc, "source": "Gemini + safety rules"}
    else:
        cat, pri = rules["category"], rules["priority"]
        loc = _find_place(text, places)
        label = cat.replace("_", " ")
        ack_msg = LOCALIZED_EMERGENCY_REPLIES.get(detected_lang, LOCALIZED_EMERGENCY_REPLIES["English"]) if (rules["safety"] or pri == "Critical") else LOCALIZED_REPLIES.get(detected_lang, LOCALIZED_REPLIES["English"])
        out = {
            "category": cat, "priority": pri, "location": loc, "language": detected_lang,
            "summary": text[:140] or "Photo report, needs manual review",
            "people_at_risk": rules["safety"], "photo_note": "Photo not analysed (rules-only mode)." if image else "",
            "complaint_draft": f"Dear team,\n\nA {pri.lower()} priority {label} issue was reported at {loc}: \"{text}\".\nPlease respond within {INFO[cat][1]}.\n\nRegards,\nCampusPulse",
            "reply_to_reporter": ack_msg,
            "source": "Rules only",
        }
    out["department"], out["sla"] = INFO[out["category"]]
    if out["category"] == "lift" and out["priority"] == "Critical":
        out["department"] = "Security & Maintenance (Lift)"
    out["raised_by_rules"] = raised
    out["error"] = err
    return out
