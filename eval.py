"""Run tests.csv through the triage and report accuracy. Usage: python eval.py"""
import csv
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from triage import DEFAULT_MODEL, triage

PLACES = ["Main Gate & Bus Bay", "Academic Block", "Computer Labs", "Library", "Cafeteria",
          "Auditorium", "Medical Centre", "Girls Hostel", "Boys Hostel", "Sports Ground & Gym"]
key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
rows = list(csv.DictReader(open("tests.csv", encoding="utf-8")))

modes = [("rules only", False)] + ([("Gemini + rules", True)] if key else [])
for name, use_ai in modes:
    cat_ok = pri_ok = safe_ok = 0
    for r in rows:
        out = triage(r["text"], places=PLACES, api_key=key, model=model, use_ai=use_ai)
        ok_c, ok_p = out["category"] == r["category"], out["priority"] == r["priority"]
        cat_ok += ok_c
        pri_ok += ok_p
        safe_ok += r["priority"] != "Critical" or out["priority"] == "Critical"
        if not (ok_c and ok_p):
            print(f"  [{name}] MISS: {r['text'][:50]} -> {out['category']}/{out['priority']} (expected {r['category']}/{r['priority']})")
        if use_ai:
            time.sleep(1)
    n = len(rows)
    crit = sum(r["priority"] == "Critical" for r in rows)
    print(f"{name}: category {cat_ok}/{n}, priority {pri_ok}/{n}, critical cases caught {safe_ok - (n - crit)}/{crit}\n")
