import re
from .embeddings import EmbeddingModel

def skill_overlap_score(jd_skills, resume_skills):
    """
    Jaccard similarity between JD skills and resume skills.
    Scaled to 0–100.
    """
    set_jd = set([s.lower() for s in jd_skills])
    set_resume = set([s.lower() for s in resume_skills])
    if not set_jd or not set_resume:
        return 0.0
    overlap = len(set_jd & set_resume)
    union = len(set_jd | set_resume)
    return (overlap / union) * 100

def embedding_score(jd, resume, model=None):
    """
    Embedding similarity between JD text and Resume text.
    """
    if model is None:
        model = EmbeddingModel()
    jd_text = jd.get("title","") + " " + " ".join(jd.get("skills",[])) + " " + " ".join(jd.get("responsibilities",[]))
    resume_text = resume.get("raw_text","")
    return model.similarity(jd_text, resume_text)

def combined_score(jd, resume, model=None, weights=(0.5, 0.5)):
    """
    Combine skill overlap and embedding similarity.
    Default weights = (0.5 skill, 0.5 embedding).
    """
    skill_score = skill_overlap_score(jd.get("skills",[]), resume.get("skills",[]))
    emb_score = embedding_score(jd, resume, model)
    w1, w2 = weights
    return w1*skill_score + w2*emb_score, skill_score, emb_score
