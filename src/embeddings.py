"""Rule 2 with BERT-based sentence embeddings instead of TF-IDF.

Everything else stays the same as the TF-IDF baseline: the same templates (numbers masked),
the same top 50 candidates, the same "first with the same count of numbers" rule.
"""
import numpy as np

from .baseline import CopyBaseline

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BLOCK = 512

_models = {}
_cache = {}  # (model name, template) -> vector, so pooled splits do not encode the same text twice


def _model(name):
    if name not in _models:
        import torch
        from sentence_transformers import SentenceTransformer
        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        _models[name] = SentenceTransformer(name, device=device)
    return _models[name]


def encode(texts, model_name):
    missing = sorted({t for t in texts if (model_name, t) not in _cache})
    if missing:
        vectors = _model(model_name).encode(missing, batch_size=128, normalize_embeddings=True,
                                            convert_to_numpy=True, show_progress_bar=len(missing) > 2000)
        for text, vector in zip(missing, vectors):
            _cache[(model_name, text)] = vector.astype(np.float32)
    return np.stack([_cache[(model_name, t)] for t in texts])


class EmbeddingBaseline(CopyBaseline):
    """Rule 1 is unchanged. Rule 2 ranks training questions by cosine similarity of sentence embeddings."""

    def __init__(self, dataset, train, model_name=DEFAULT_MODEL):
        super().__init__(dataset, train)
        self.model_name = model_name
        self.train_vectors = encode([dataset.template(r) for r in train], model_name)

    def similarity_rows(self, questions):
        vectors = encode([self.dataset.template(r) for r in questions], self.model_name)
        for start in range(0, len(vectors), BLOCK):
            # float64 so that the stable sort breaks ties the same way as the TF-IDF version
            yield from (vectors[start:start + BLOCK] @ self.train_vectors.T).astype(np.float64)
