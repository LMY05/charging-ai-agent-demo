from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from backend.agents.graph import graph
from backend.rag.loader import load_document
from backend.rag.splitter import split_text
from backend.rag.vector_store import vector_store
from backend.database import init_db
from backend.config.settings import settings
import os

app = FastAPI(title="Charging AI Agent Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    agent: str
    source: str

init_db()

knowledge_dir = settings.knowledge_dir
if not os.path.exists(knowledge_dir):
    os.makedirs(knowledge_dir)

for filename in os.listdir(knowledge_dir):
    if filename.endswith((".pdf", ".txt", ".md", ".markdown")):
        file_path = os.path.join(knowledge_dir, filename)
        try:
            text = load_document(file_path)
            documents = split_text(text)
            vector_store.add_documents(documents)
            print(f"Loaded {filename} successfully")
        except Exception as e:
            print(f"Failed to load {filename}: {e}")

vector_store.save()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    messages = [HumanMessage(content=request.message)]
    
    result = graph.invoke({
        "messages": messages,
        "query_type": "",
        "retrieved_docs": [],
        "sql_result": "",
        "answer": "",
        "agent_name": "",
        "source": ""
    })
    
    return ChatResponse(
        answer=result["answer"],
        agent=result["agent_name"],
        source=result["source"]
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(knowledge_dir, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        text = load_document(file_path)
        documents = split_text(text)
        vector_store.add_documents(documents)
        vector_store.save()
        
        return {"message": f"文件 {file.filename} 上传成功并已添加到知识库"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Charging AI Agent Demo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
