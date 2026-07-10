from langchain_core.documents import Document
from backend.rag.vector_store import vector_store
from backend.config.settings import settings

def retrieve_documents(query: str, top_k: int = None) -> list[Document]:
    k = top_k or settings.top_k
    results = vector_store.search(query, k=k)
    return [doc for doc, _ in results]

def get_retrieved_sources(query: str, top_k: int = None) -> str:
    k = top_k or settings.top_k
    results = vector_store.search(query, k=k)
    
    sources = []
    for i, (doc, dist) in enumerate(results):
        sources.append(f"来源{i+1}: {doc.page_content[:100]}...")
    
    return "\n".join(sources) if sources else "无相关文档"
