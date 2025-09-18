from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Small, fast model
MODEL_NAME = "all-MiniLM-L6-v2"

class EmbeddingModel:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Encode a list of texts into embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, convert_to_numpy=True)

    def similarity(self, text_a, text_b):
        """
        Cosine similarity between two texts.
        """
        emb_a = self.encode(text_a)
        emb_b = self.encode(text_b)
        return float(cosine_similarity(emb_a, emb_b)[0][0]) * 100
