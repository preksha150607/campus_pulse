import os

import streamlit as st

from triage import DEFAULT_MODEL, triage

st.set_page_config(page_title="CampusPulse", page_icon="🏫", layout="wide")

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

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API key", value=os.getenv("GEMINI_API_KEY", ""), type="password")
    model = st.text_input("Model", value=DEFAULT_MODEL)
    use_ai = st.toggle("Use Gemini", value=True, help="Turn off to demo the rules-only fallback")
    st.subheader("Campus places")
    places_text = st.text_area("One per line. Edit to match the real campus.", value=DEFAULT_PLACES, height=250)
places = [p.strip() for p in places_text.splitlines() if p.strip()]

st.title("CampusPulse")
st.caption("Sapthagiri NPS University · Report by text or photo, in English, Hindi, Kannada or Marathi")

if "tickets" not in st.session_state:
    st.session_state.tickets = []
    st.session_state.nid = 1

left, right = st.columns([1, 1.1], gap="large")

with left:
    st.subheader("Report an issue")
    text = st.text_area("What is the problem?", height=110,
                        placeholder="Lift stuck between floors in the Academic Block, two people inside")
    photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg", "webp"])
    with st.expander("Or take a photo with the camera"):
        cam = st.camera_input("Camera")
    img = photo or cam
    if img:
        st.image(img, width=220)
    if st.button("Analyse and submit", type="primary"):
        if not text.strip() and not img:
            st.warning("Describe the issue or add a photo first.")
        else:
            with st.spinner("Analysing..."):
                r = triage(text.strip(), img.getvalue() if img else None,
                           getattr(img, "type", None), places, api_key, model, use_ai)
            r["id"], r["text"], r["done"] = st.session_state.nid, text.strip() or "Photo report", False
            r["img"] = img.getvalue() if img else None
            st.session_state.nid += 1
            st.session_state.tickets.insert(0, r)
            st.session_state.last = r

    r = st.session_state.get("last")
    if r:
        st.divider()
        if r["error"]:
            st.warning(f"Gemini failed, so the rules-only fallback was used. ({r['error'][:160]})")
        if r["priority"] == "Critical":
            st.error("Safety escalation: campus security alerted. " + (r["reply_to_reporter"] if r["people_at_risk"] else ""))
        c1, c2, c3 = st.columns(3)
        c1.metric("Priority", r["priority"])
        c2.metric("Category", r["category"].replace("_", " "))
        c3.metric("Response target", r["sla"])
        st.write(f"**Department:** {r['department']}  \n**Location:** {r['location']}  \n"
                 f"**Language:** {r['language']}  \n**Summary:** {r['summary']}")
        if r["photo_note"]:
            st.write(f"**Photo:** {r['photo_note']}")
        if r["raised_by_rules"]:
            st.info("Priority was raised by the safety rules.")
        st.caption(f"Source: {r['source']}")
        st.markdown("**Reply to the reporter**")
        st.info(r["reply_to_reporter"])
        st.markdown("**Drafted complaint**")
        st.code(r["complaint_draft"], language=None)

with right:
    tickets = st.session_state.tickets
    open_t = [t for t in tickets if not t["done"]]
    a, b, c = st.columns(3)
    a.metric("Open", len(open_t))
    b.metric("Critical", sum(t["priority"] == "Critical" for t in open_t))
    c.metric("Resolved", len(tickets) - len(open_t))
    if open_t:
        by_loc = {}
        for t in open_t:
            by_loc[t["location"]] = by_loc.get(t["location"], 0) + 1
        for loc, n in sorted(by_loc.items(), key=lambda kv: -kv[1]):
            st.progress(n / max(by_loc.values()), text=f"{loc}: {n}")
        top = max(by_loc, key=by_loc.get)
        if by_loc[top] > 1 and top != "unknown":
            st.info(f"{top} has {by_loc[top]} open issues. Repeated reports often share a cause, so send one team.")
    st.subheader("Open queue")
    if not tickets:
        st.write("No reports yet. Submit one on the left.")
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    for t in sorted(tickets, key=lambda t: (t["done"], order[t["priority"]])):
        with st.container(border=True):
            cols = st.columns([1, 5, 2])
            if t["img"]:
                cols[0].image(t["img"], width=60)
            cols[1].markdown(f"**{t['priority']}** · {t['category'].replace('_', ' ')} · {t['location']}  \n{t['text']}")
            if not t["done"] and cols[2].button("Resolve", key=f"r{t['id']}"):
                t["done"] = True
                st.rerun()
            elif t["done"]:
                cols[2].write("Resolved")
