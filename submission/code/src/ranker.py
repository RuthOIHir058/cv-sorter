from .scorer import combined_score
from .embeddings import EmbeddingModel

def rank_candidates(jd, resumes, weights=(0.5, 0.5)):
    """
    Rank resumes against a job description.
    Returns list of dicts sorted by final score.
    """
    model = EmbeddingModel()
    results = []

    for r in resumes:
        final, skill_score, emb_score = combined_score(jd, r, model, weights)
        results.append({
            "id": r.get("id"),
            "name": r.get("name"),
            "email": r.get("email"),
            "final_score": round(final,2),
            "skill_score": round(skill_score,2),
            "embedding_score": round(emb_score,2)
        })

    results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    return results
