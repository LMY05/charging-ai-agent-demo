from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.config.settings import settings

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
    model=settings.openai_model,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的AI聊天助手。\n\n"
     "请用自然、亲切的语言与用户交流。\n"
     "如果用户的问题与充电业务相关，可以适当提供帮助。"),
    ("human", "{message}")
])

chain = prompt | llm | StrOutputParser()

def chat(message: str) -> str:
    return chain.invoke({"message": message})
