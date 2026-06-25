from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_size = 384

    def embed_text(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()