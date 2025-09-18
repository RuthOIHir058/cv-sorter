# CV Sorter: AI-Powered Resume Ranking System

## 📌 Project Overview
This project implements an AI-based Applicant Tracking System (ATS) that parses resumes, extracts skills and experiences, and ranks candidates against job descriptions using embeddings and semantic similarity.  
Developed as part of a capstone project.

---

## 🚀 Features
- 📄 **Resume Parsing**: Extracts text from `.pdf`, `.docx`, `.txt` resumes.
- 📝 **Job Description Parsing**: Extracts skills, responsibilities, and requirements.
- 🤖 **Candidate Ranking**:
  - Skill overlap (Jaccard similarity)
  - Sentence-transformer embeddings (`all-MiniLM-L6-v2`)
  - Configurable scoring weights
- 📊 **Evaluation Metrics**:
  - Precision@k, MAP, Kendall Tau
- 🌐 **Streamlit App**:
  - Upload resumes & JDs
  - Get ranked candidates with scores
  - Export results as CSV/JSON
- 🐳 **Dockerized Deployment**

---

## 🗂️ Project Structure
cv-sorter/
├── data/
│ ├── resumes/ # Raw resumes
│ ├── parsed_resumes/ # Parsed JSON resumes
│ └── sample_jd.txt # Example job description
├── src/
│ ├── app_streamlit.py # Streamlit UI
│ ├── parse_resumes.py # Resume parsing
│ ├── parse_jd.py # JD parsing
│ ├── embeddings.py # Embeddings
│ ├── scorer.py # Scoring functions
│ ├── ranker.py # Ranking pipeline
│ ├── eval_metrics.py # Evaluation metrics
│ └── utils.py # Helper functions
├── tests/
│ └── gold_standard.json # Human-annotated test set
├── requirements.txt
├── Dockerfile
├── README.md
└── report.pdf (to be added)

---

## ⚙️ Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/RuthOIHir058/cv-sorter.git
cd cv-sorter
2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Run locally
streamlit run src/app_streamlit.py
App will run at: http://localhost:8501

🐳 Docker Deployment
docker build -t cv-sorter:latest .
docker run -p 8501:8501 cv-sorter:latest
📊 Evaluation
Run evaluation against gold standard:

python -m src.eval_metrics
Metrics include:

Precision@k

Average Precision

Mean Average Precision (MAP)

Kendall Tau ranking correlation

📑 Report & Slides
report.pdf – Contains goals, design rationale, metrics, and analysis.

slides.pdf – Summarizes technical approach and results.

demo – Streamlit app demonstration.

📬 Contact
Author: Sirsha Dattasarma
Email: sirshodattasarma@gmail.com
GitHub: RuthOIHir058
