import streamlit as st
import os, json
import pandas as pd
import sys

# allow imports from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parse_resumes import parse_resume_file
from src.parse_jd import parse_jd_text
from src.ranker import rank_candidates

st.set_page_config(page_title="CV Sorter", layout="wide")
st.title("📄 CV Sorting using LLMs")

# --- Job Description Input ---
st.header("Job Description")
uploaded_jd = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
jd_text = None
if uploaded_jd:
    jd_text = uploaded_jd.read().decode("utf-8")
else:
    jd_text = st.text_area("Or paste job description text here", height=200)

# --- Resume Input ---
st.header("Resumes")
resume_dir = st.text_input("Resume folder path", value="data/resumes")

# --- Run Ranking ---
if st.button("Run Ranking"):
    if not jd_text:
        st.error("Please provide a Job Description first.")
    else:
        # Parse JD
        jd = parse_jd_text(jd_text)

        # Parse resumes in folder
        resumes = []
        if os.path.isdir(resume_dir):
            files = [f for f in os.listdir(resume_dir) if f.lower().endswith(('.pdf','.docx','.txt'))]
            for f in files:
                path = os.path.join(resume_dir, f)
                try:
                    r = parse_resume_file(path)
                    resumes.append(r)
                except Exception as e:
                    st.warning(f"Could not parse {f}: {e}")
        else:
            st.error(f"Folder not found: {resume_dir}")

        if not resumes:
            st.error("No resumes found to process.")
        else:
            # Rank candidates
            results = rank_candidates(jd, resumes, weights=(0.5, 0.5))

            # Display results in a table
            df = pd.DataFrame(results)
            st.subheader("Ranking Results")
            st.dataframe(df[["id","name","email","final_score","skill_score","embedding_score"]])

            # Download buttons
            st.download_button(
                label="Download Results as CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="ranking_results.csv",
                mime="text/csv"
            )
            st.download_button(
                label="Download Results as JSON",
                data=json.dumps(results, indent=2),
                file_name="ranking_results.json",
                mime="application/json"
            )

