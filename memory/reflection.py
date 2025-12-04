import os
from sentence_transformers import SentenceTransformer
import chromadb
import math
from chromadb.config import Settings

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 5000

class Retriever:
    def __init__(self, collection_name: str = "ananta_memory", embed_model_name: str = DEFAULT_EMBED_MODEL):
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer(embed_model_name)

    def embed(self, texts):
        if not texts:
            return []
        embs = self.embedder.encode(texts, show_progress_bar=False)
        return embs.tolist() if hasattr(embs, "tolist") else [list(e) for e in embs]

    def add_documents(self, ids, metadatas, documents):
        if not ids:
            return
        clean_metas = []
        for m in metadatas:
            cm = {}
            for k, v in m.items():
                if isinstance(v, (str, int, float, bool)) or v is None:
                    cm[k] = v
                elif isinstance(v, list):
                    cm[k] = ", ".join(map(str, v))
                else:
                    cm[k] = str(v)
            clean_metas.append(cm)

        n = len(ids)
        chunks = math.ceil(n / BATCH_SIZE)
        for i in range(chunks):
            s = i * BATCH_SIZE
            e = min((i + 1) * BATCH_SIZE, n)
            sub_ids = ids[s:e]
            sub_docs = documents[s:e]
            sub_meta = clean_metas[s:e]
            sub_emb = self.embed(sub_docs)
            self.collection.add(ids=sub_ids, documents=sub_docs, metadatas=sub_meta, embeddings=sub_emb)

    def query(self, query_text, top_k=3):
        if not query_text:
            return []
        q_emb = self.embed([query_text])[0]
        results = self.collection.query(query_embeddings=[q_emb], n_results=top_k)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0] if "distances" in results else [None] * len(docs)
        out = []
        for doc, meta, dist in zip(docs, metas, dists):
            out.append({"document": doc, "metadata": meta, "score": None if dist is None else (1.0 / (1.0 + dist))})
        return out

    def list_collections(self):
        return [c["name"] for c in self.client.list_collections()]
