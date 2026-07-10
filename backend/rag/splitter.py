from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " "]
    )
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    return documents
