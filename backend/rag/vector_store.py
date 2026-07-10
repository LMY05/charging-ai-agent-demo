import faiss
import numpy as np
import os
from pathlib import Path
from langchain_core.documents import Document
from backend.rag.embedding import embedding_model
from backend.config.settings import settings

class FAISSVectorStore:
    def __init__(self):
        self.index = None
        self.documents = []
        self.store_path = Path(settings.vector_store_path)
    
    def add_documents(self, documents: list[Document]):
        if not documents:
            return
        
        texts = [doc.page_content for doc in documents]
        embeddings = embedding_model.embed_documents(texts)
        embeddings = np.array(embeddings).astype("float32")
        
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
        
        self.index.add(embeddings)
        self.documents.extend(documents)
    
    def save(self):
        if self.index is not None:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.store_path))
            
            docs_file = self.store_path.with_suffix(".pkl")
            import pickle
            with open(docs_file, "wb") as f:
                pickle.dump(self.documents, f)
    
    def load(self):
        if self.store_path.exists():
            self.index = faiss.read_index(str(self.store_path))
            
            docs_file = self.store_path.with_suffix(".pkl")
            if docs_file.exists():
                import pickle
                with open(docs_file, "rb") as f:
                    self.documents = pickle.load(f)
            return True
        return False
    
    def search(self, query: str, k: int = 3) -> list[tuple[Document, float]]:
        if self.index is None or len(self.documents) == 0:
            return []
        
        query_embedding = embedding_model.embed_query(query)
        query_embedding = np.array([query_embedding]).astype("float32")
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], dist))
        
        return results

vector_store = FAISSVectorStore()
