from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from backend.config.settings import settings

class QueryType(BaseModel):
    query_type: str = Field(description="问题类型，必须是 knowledge、data 或 chat 中的一个")
    reason: str = Field(description="分类理由")

parser = JsonOutputParser(pydantic_object=QueryType)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能问题分类器，负责判断用户的问题类型。\n\n"
     "请根据以下规则进行分类：\n"
     "- knowledge：与充电业务知识相关的问题，如充电方式、费用计算、故障处理等\n"
     "- data：需要查询数据库的问题，如充电订单、充电站状态、用户统计等\n"
     "- chat：普通聊天或闲聊，与充电业务无关的问题\n\n"
     "请严格按照JSON格式输出。"),
    ("human", "{input}\n\n{format_instructions}")
])

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
    model=settings.openai_model,
    temperature=0
)

chain = prompt | llm | parser

def classify_query(query: str) -> str:
    try:
        result = chain.invoke({"input": query, "format_instructions": parser.get_format_instructions()})
        query_type = result["query_type"]
        return query_type if query_type in {"knowledge", "data", "chat"} else "chat"
    except Exception:
        return "chat"
