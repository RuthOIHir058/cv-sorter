#!/usr/bin/env python3
import json
from pathlib import Path
import re

IN_DIR = Path("data/parsed_resumes")
OUT_DIR = Path("data/parsed_resumes_anonymized")
OUT_DIR.mkdir(parents=True, exist_ok=True)

email_re = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_re = re.compile(r"\+?\d[\d\-\s\(\)]{7,}\d")

for p in sorted(IN_DIR.glob("*.json")):
    doc = json.load(open(p, encoding="utf-8"))
    # redact personal fields
    doc["name"] = "REDACTED"
    doc["email"] = "REDACTED"
    doc["phone"] = "REDACTED"
    # redact email/phone patterns inside raw_text and shorten
    raw = doc.get("raw_text","")
    raw = email_re.sub("[REDACTED_EMAIL]", raw)
    raw = phone_re.sub("[REDACTED_PHONE]", raw)
    # optionally keep first N chars as sample evidence
    doc["raw_text_snippet"] = (raw[:800] + "...") if len(raw) > 800 else raw
    # remove or shorten detailed lists if present
    if "experience" in doc:
        doc["experience"] = [{"title":"REDACTED","company":"REDACTED","start":"XXXX","end":"XXXX"} for _ in doc.get("experience",[])]
    if "education" in doc:
        doc["education"] = [{"degree":"REDACTED","institution":"REDACTED","year":"XXXX"} for _ in doc.get("education",[])]
    # write anonymized file
    outp = OUT_DIR / p.name
    json.dump(doc, open(outp, "w", encoding="utf-8"), indent=2)
    print("Wrote", outp)
