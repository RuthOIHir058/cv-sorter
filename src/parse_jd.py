import re

def parse_jd_text(text: str, skill_bank=None):
    """
    Parse a job description into a structured JSON-like dict.
    - Extract skills using the same method/skill_bank as resumes.
    - Detect minimum years of experience.
    - Extract responsibilities / requirements (bullet points).
    """
    jd = {}

    # ---- Title ----
    first_line = text.strip().splitlines()[0]
    jd["title"] = first_line.strip() if first_line else "Unknown Role"

    # ---- Skills ----
    if skill_bank:
        # Match known skills in text (case-insensitive)
        skills = [s for s in skill_bank if re.search(rf"\\b{re.escape(s)}\\b", text, re.I)]
    else:
        # Fallback: naive token extraction
        tokens = re.findall(r"[A-Za-z\+\-#]{2,}", text.lower())
        # pick common tokens that repeat
        skills = list({t for t in tokens if tokens.count(t) > 1})
    jd["skills"] = skills[:30]

    # ---- Years of experience ----
    years_match = re.search(r"(\\d+)\\+?\\s+years?", text, re.I)
    jd["min_years_experience"] = int(years_match.group(1)) if years_match else 0

    # ---- Responsibilities / Requirements ----
    resp = []
    # Look for section headers
    sections = re.split(r"Responsibilities|Requirements|Duties", text, flags=re.I)
    if len(sections) > 1:
        # take the part after the first header
        lines = sections[1].splitlines()
        resp = [line.strip(" -•\t") for line in lines if len(line.strip()) > 3][:15]
    jd["responsibilities"] = resp

    # ---- Keywords ----
    # Just pick capitalized words of 3+ letters as naive keywords
    keywords = re.findall(r"\\b[A-Z][a-zA-Z]{2,}\\b", text)
    jd["keywords"] = list(set(keywords))[:20]

    return jd

# Quick test
if __name__ == "__main__":
    sample_text = """Job Title: Data Scientist
Responsibilities:
- Build ML models
- Analyze data
Requirements:
- 3+ years of Python experience
- Knowledge of PyTorch
"""
    parsed = parse_jd_text(sample_text, skill_bank=["python","pytorch","sql","ml"])
    import json
    print(json.dumps(parsed, indent=2))
