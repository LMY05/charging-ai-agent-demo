from langchain_openai import OpenAIEmbeddings
from backend.config.settings import settings

embedding_model = OpenAIEmbeddings(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
    model="text-embedding-3-small"
)

def get_embedding(text: str):
    return embedding_model.embed_query(text)

def get_embeddings(texts: list[str]):
    return embedding_model.embed_documents(texts)
