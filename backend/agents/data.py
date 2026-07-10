from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from backend.database.connection import engine
from backend.config.settings import settings

db = SQLDatabase(engine)

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
    model=settings.openai_model,
    temperature=0
)

query_chain = create_sql_query_chain(llm, db)

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据分析助手。\n\n"
     "请根据SQL查询结果，用自然、友好的语言回答用户的问题。\n"
     "查询结果：\n{result}"),
    ("human", "{question}")
])

answer_chain = answer_prompt | llm | StrOutputParser()

def query_with_sql(question: str) -> tuple[str, str]:
    try:
        sql_query = query_chain.invoke({"question": question})
        
        if not sql_query.strip().upper().startswith("SELECT"):
            return "抱歉，为了安全考虑，我只能执行查询操作。", "SQL查询被拒绝"
        
        result = db.run(sql_query)
        
        answer = answer_chain.invoke({
            "question": question,
            "result": result
        })
        
        return answer, f"SQL: {sql_query}"
    except Exception as e:
        return f"查询出错：{str(e)}", "查询失败"
