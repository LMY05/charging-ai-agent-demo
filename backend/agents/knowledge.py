from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.rag.retriever import retrieve_documents, get_retrieved_sources
from backend.config.settings import settings

llm = ChatOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
    model=settings.openai_model,
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的充电业务知识问答助手。\n\n"
     "请根据提供的参考文档回答用户问题。\n"
     "如果参考文档中有相关信息，请基于文档内容进行回答，并注明来源。\n"
     "如果参考文档中没有相关信息，请明确说明无法从文档中找到答案。\n\n"
     "参考文档：\n{context}"),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

def answer_with_knowledge(question: str) -> tuple[str, str]:
    documents = retrieve_documents(question)
    context = "\n\n".join([doc.page_content for doc in documents])
    sources = get_retrieved_sources(question)
    
    if not documents:
        return "知识库中没有找到相关信息，请尝试其他问题。", "无相关文档"
    
    answer = chain.invoke({"question": question, "context": context})
    return answer, sources
