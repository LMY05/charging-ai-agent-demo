# ⚡ Charging AI Agent Demo

基于 LangGraph 和 RAG 的充电业务场景 AI Agent 助手演示项目。

## 📋 项目介绍

本项目模拟企业充电业务场景下的 AI Agent
助手，展示大模型应用开发中的核心能力：

-   **RAG 知识库问答**：文档上传、解析、向量化、检索、生成回答
-   **Multi-Agent 系统**：基于 LangGraph 实现多 Agent 协作工作流
-   **NL-to-SQL**：自然语言转 SQL 查询业务数据库
-   **Agent 路由机制**：根据用户意图自动选择不同 Agent
-   **对话式交互**：通过 Streamlit 前端完成智能聊天

## ✨ 项目亮点

### 🤖 Multi-Agent Workflow

基于 LangGraph 构建 Agent 工作流：

``` text
用户输入

↓

Router Agent

↓

Knowledge Agent / Data Agent / Chat Agent

↓

RAG检索 / SQL查询 / LLM对话

↓

最终回答
```

### 📚 RAG Pipeline

完整实现：

``` text
文档上传
    ↓
文档解析
    ↓
文本切片
    ↓
Embedding
    ↓
FAISS向量检索
    ↓
上下文增强
    ↓
LLM生成回答
```

### 📊 NL-to-SQL

支持自然语言查询业务数据库：

示例：

    北京有多少个充电站？
    最近一个月充电订单是多少？

流程：

``` text
用户问题

↓

Data Agent

↓

SQL生成

↓

SQLite查询

↓

结果分析
```

## 🏗️ 技术架构

``` text
Streamlit 前端

        ↓

FastAPI 后端

        ↓

LangGraph Multi-Agent

        ↓

Router Agent

        ↓

Knowledge Agent / Data Agent / Chat Agent

        ↓

FAISS / SQLite / LLM API
```

## 🤖 Agent 流程图

``` text
用户提问

↓

Router Agent 判断问题类型

↓

knowledge
    ↓
Knowledge Agent
    ↓
RAG检索 + LLM回答


data
    ↓
Data Agent
    ↓
NL2SQL + 数据库查询


chat
    ↓
Chat Agent
    ↓
LLM回复
```

## 📚 RAG 流程说明

``` text
文档上传

↓

PDF/TXT/Markdown解析

↓

文本切片

↓

Embedding

↓

FAISS向量存储

↓

用户提问

↓

Top-K检索

↓

上下文注入

↓

LLM生成回答
```

## 🛠️ 技术栈

-   Python 3.11
-   FastAPI
-   LangChain
-   LangGraph
-   FAISS
-   SQLite
-   Streamlit
-   OpenAI API
-   Embedding Model

## 📂 项目结构

``` text
charging-ai-agent-demo/

├── backend/
│   ├── main.py
│   ├── agents/
│   │   ├── router.py
│   │   ├── knowledge.py
│   │   ├── data.py
│   │   ├── chat.py
│   │   └── graph.py
│   ├── rag/
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── embedding.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   └── database/
│
├── frontend/
│   └── app.py
│
├── knowledge/
│
├── requirements.txt
└── README.md
```

## 🚀 启动方式

### 安装依赖

``` bash
cd charging-ai-agent-demo

uv venv

.venv\Scripts\activate

pip install -r requirements.txt
```

### 配置环境变量

复制：

``` bash
cp .env.example .env
```

配置：

``` env
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### 启动后端

``` bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 启动前端

``` bash
streamlit run frontend/app.py
```

访问：

    http://localhost:8501

## 📝 功能测试

### Knowledge Agent

问题：

    充电费用如何计算？

返回知识库相关答案。

### Data Agent

问题：

    北京有多少个充电站？

查询数据库并返回结果。

### Chat Agent

问题：

    你好

返回普通对话回复。

## 📬 联系方式

欢迎交流 AI Agent、RAG 和 LLM 应用开发。
