from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, List
from backend.agents.router import classify_query
from backend.agents.knowledge import answer_with_knowledge
from backend.agents.data import query_with_sql
from backend.agents.chat import chat

class AgentState(TypedDict):
    messages: List[BaseMessage]
    query_type: str
    retrieved_docs: List[str]
    sql_result: str
    answer: str
    agent_name: str
    source: str

def route_query(state: AgentState) -> dict:
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        query = last_message.content
        query_type = classify_query(query)
        return {"query_type": query_type}
    return {"query_type": "chat"}

def knowledge_agent(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    question = last_message.content
    answer, sources = answer_with_knowledge(question)
    state["answer"] = answer
    state["agent_name"] = "Knowledge Agent"
    state["source"] = sources
    return state

def data_agent(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    question = last_message.content
    answer, sql_info = query_with_sql(question)
    state["answer"] = answer
    state["agent_name"] = "Data Agent"
    state["source"] = sql_info
    return state

def chat_agent(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    message = last_message.content
    answer = chat(message)
    state["answer"] = answer
    state["agent_name"] = "Chat Agent"
    state["source"] = "无引用来源"
    return state

workflow = StateGraph(AgentState)

workflow.add_node("router", route_query)
workflow.add_node("knowledge", knowledge_agent)
workflow.add_node("data", data_agent)
workflow.add_node("chat", chat_agent)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    lambda x: x["query_type"],
    {
        "knowledge": "knowledge",
        "data": "data",
        "chat": "chat"
    }
)

workflow.add_edge("knowledge", END)
workflow.add_edge("data", END)
workflow.add_edge("chat", END)

graph = workflow.compile()
