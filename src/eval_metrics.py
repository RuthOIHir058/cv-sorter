import json
import numpy as np
from scipy.stats import kendalltau
from pathlib import Path

def precision_at_k(recommended_ids, relevant_ids, k):
    rec_k = recommended_ids[:k]
    return len(set(rec_k) & set(relevant_ids)) / k

def average_precision(recommended_ids, relevant_ids):
    score = 0.0
    hits = 0
    for i, rid in enumerate(recommended_ids, start=1):
        if rid in relevant_ids:
            hits += 1
            score += hits / i
    return score / max(1, len(relevant_ids))

def map_score(list_of_recommended, list_of_relevant):
    return np.mean([
        average_precision(r, rel) for r, rel in zip(list_of_recommended, list_of_relevant)
    ])

def kendall_tau(rank_a, rank_b):
    # both are lists of ids in order
    return kendalltau(
        [rank_a.index(x) for x in rank_a],
        [rank_b.index(x) for x in rank_b]
    )[0]

def run_evaluation(gold_file="tests/gold_standard.json"):
    from src.parse_jd import parse_jd_text
    from src.ranker import rank_candidates
    import json

    gold = json.load(open(gold_file))
    jd_text = open(gold["job_description"]).read()
    jd = parse_jd_text(jd_text)

    # Load system resumes
    resumes = []
    for r in gold["resumes"]:
        resume_path = Path("data/parsed_resumes") / (r["id"] + ".json")
        if resume_path.exists():
            resumes.append(json.load(open(resume_path)))

    # Run system ranking
    system_results = rank_candidates(jd, resumes)
    system_ranked_ids = [r["id"] for r in system_results]

    # Gold rankings
    gold_ranked_ids = [r["id"] for r in sorted(gold["resumes"], key=lambda x: x["rank"])]
    gold_relevant = [r["id"] for r in gold["resumes"] if r["relevant"]]

    # Metrics
    p_at_5 = precision_at_k(system_ranked_ids, gold_relevant, 5)
    ap = average_precision(system_ranked_ids, gold_relevant)
    tau = kendall_tau(system_ranked_ids, gold_ranked_ids)

    print("📊 Evaluation Results")
    print(f"Precision@5: {p_at_5:.2f}")
    print(f"Average Precision: {ap:.2f}")
    print(f"Kendall Tau (rank correlation): {tau:.2f}")

if __name__ == "__main__":
    run_evaluation()
