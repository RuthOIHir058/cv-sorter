import re
from pathlib import Path
from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text(path: str) -> str:
    """
    Extract raw text from PDF, DOCX, or TXT resume.
    """
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return extract_pdf_text(path)
    elif p.suffix.lower() == ".docx":
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif p.suffix.lower() == ".txt":
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {p.suffix}")

def skill_extractor(raw_text: str, skill_bank=None):
    """
    Extract skills from raw text.
    If skill_bank provided, match those skills case-insensitively.
    Otherwise, return frequent tokens as naive skills.
    """
    tokens = re.findall(r"[A-Za-z\+\-#]{2,}", raw_text.lower())
    if skill_bank:
        skills = [s for s in skill_bank if s.lower() in tokens]
    else:
        # naive: pick unique tokens appearing more than once
        skills = list({t for t in tokens if tokens.count(t) > 1})
    return skills[:30]  # limit to top 30

def parse_basic_fields(raw_text: str, resume_id="unknown", skill_bank=None):
    """
    Extract basic structured fields from resume text.
    """
    # Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", raw_text)
    email = email_match.group(0) if email_match else None

    # Phone (basic)
    phone_match = re.search(r"\+?\d[\d\s\-\(\)]{7,}\d", raw_text)
    phone = phone_match.group(0) if phone_match else None

    # Name heuristic: first line with 2 capitalized words
    lines = raw_text.splitlines()
    name = None
    for line in lines[:10]:
        if re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+", line.strip()):
            name = line.strip()
            break

    # Skills
    skills = skill_extractor(raw_text, skill_bank=skill_bank)

    return {
        "id": resume_id,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience": [],   # can be extended later
        "education": [],    # can be extended later
        "raw_text": raw_text
    }

def parse_resume_file(path: str, skill_bank=None):
    """
    Parse a single resume file into structured JSON-like dict.
    """
    raw_text = extract_text(path)
    resume_id = Path(path).stem
    return parse_basic_fields(raw_text, resume_id, skill_bank=skill_bank)

# Quick test if run directly
if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python src/parse_resumes.py <resume_file>")
    else:
        parsed = parse_resume_file(sys.argv[1])
        print(json.dumps(parsed, indent=2))
