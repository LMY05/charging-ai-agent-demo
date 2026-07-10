# ⚡ Charging AI Agent Demo

基于 LangGraph 和 RAG 的充电业务场景 AI Agent 助手演示项目。

## 📋 项目介绍

本项目模拟企业充电业务场景下的 AI Agent 助手，展示了以下核心能力：

- **RAG 知识库问答**：文档上传、解析、向量化、检索、生成回答
- **Multi-Agent 系统**：基于 LangGraph 实现多 Agent 协作工作流
- **NL-to-SQL**：自然语言转 SQL 查询数据库
- **对话式交互**：通过 Streamlit 前端进行友好的聊天交互

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit 前端                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │  聊天窗口     │ │ 历史记录     │ │ 文件上传     │            │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘            │
└─────────│────────────────│────────────────│─────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI 后端                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    POST /chat                              │  │
│  │  session_id + message → Router Agent → Answer             │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    POST /upload                            │  │
│  │  file → PDF解析 → 文本切片 → Embedding → FAISS             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        LangGraph Multi-Agent                    │
│                                                                 │
│   START → Router Agent → [知识问答/数据分析/普通聊天] → END      │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Router Agent│  │Knowledge    │  │ Data Agent  │             │
│  │ 问题分类    │  │Agent        │  │ NL→SQL      │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Shared State                         │    │
│  │  messages, query_type, retrieved_docs, sql_result,      │    │
│  │  answer, agent_name, source                             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   SQLite      │ │   FAISS       │ │   LLM API     │
│   充电订单     │ │   向量存储     │ │   OpenAI      │
│   充电站       │ │   (知识文档)   │ │               │
│   用户记录     │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

## 🤖 Agent 流程图

```
用户提问
    │
    ▼
┌─────────────┐
│ Router Agent│  判断问题类型
└──────┬──────┘
       │
       ├── knowledge ──▶ ┌─────────────────┐
       │                  │ Knowledge Agent │ ──▶ RAG检索 + LLM回答
       │                  └─────────────────┘
       │
       ├── data ──────▶ ┌─────────────────┐
       │                  │   Data Agent    │ ──▶ NL→SQL + 数据库查询
       │                  └─────────────────┘
       │
       └── chat ──────▶ ┌─────────────────┐
                         │   Chat Agent    │ ──▶ 直接LLM回答
                         └─────────────────┘
```

## 📚 RAG 流程说明

```
文档上传
    │
    ▼
文档解析 (PDF/TXT/Markdown)
    │
    ▼
文本切片 (RecursiveCharacterTextSplitter)
    │
    ▼
Embedding (OpenAI text-embedding-3-small)
    │
    ▼
FAISS 向量存储
    │
    ▼
用户提问
    │
    ▼
向量检索 (Top-K)
    │
    ▼
上下文注入
    │
    ▼
LLM 生成回答
    │
    ▼
返回答案 + 引用来源
```

## 🛠️ 技术栈

- **Python 3.11**
- **FastAPI** - 后端 API 框架
- **LangChain** - LLM 应用开发框架
- **LangGraph** - 多 Agent 工作流编排
- **FAISS** - 向量数据库
- **SQLite** - 关系型数据库
- **Streamlit** - 前端交互界面
- **OpenAI API** - LLM 和 Embedding

## 📂 项目结构

```
charging-ai-agent-demo/
├── backend/
│   ├── main.py                      # FastAPI 入口
│   ├── agents/
│   │   ├── router.py                # Router Agent - 问题分类
│   │   ├── knowledge.py             # Knowledge Agent - RAG回答
│   │   ├── data.py                  # Data Agent - NL→SQL
│   │   ├── chat.py                  # Chat Agent - 普通聊天
│   │   └── graph.py                 # LangGraph StateGraph 编排
│   ├── rag/
│   │   ├── loader.py                # PDF/TXT/MD 文档加载
│   │   ├── splitter.py              # 文本切片
│   │   ├── embedding.py             # Embedding 向量化
│   │   ├── vector_store.py          # FAISS 向量存储
│   │   └── retriever.py             # 检索器封装
│   ├── tools/
│   ├── database/
│   │   ├── schema.py                # 表结构定义
│   │   ├── mock_data.py             # 模拟数据
│   │   └── connection.py            # 数据库连接
│   └── config/
│       └── settings.py              # 配置管理
├── frontend/
│   └── app.py                       # Streamlit 前端
├── knowledge/
│   └── charging_faq.md              # 示例知识文档
├── .env.example                     # 环境变量示例
├── requirements.txt                 # 依赖清单
└── README.md                        # 项目说明
```

## 🚀 启动方式

### 1. 安装依赖

```bash
cd charging-ai-agent-demo
uv venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 OpenAI API Key：

```
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### 3. 启动后端服务

```bash
cd charging-ai-agent-demo
.venv\Scripts\activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 4. 启动前端界面

打开新的终端：

```bash
cd charging-ai-agent-demo
.venv\Scripts\activate
streamlit run frontend/app.py
```

### 5. 访问应用

打开浏览器访问 `http://localhost:8501`

## 📝 功能测试

### Knowledge Agent 测试
```
问题：充电费用如何计算？
期望：返回充电费用计算公式和组成部分
```

### Data Agent 测试
```
问题：北京有多少个充电站？
期望：查询数据库并返回统计结果
```

### Chat Agent 测试
```
问题：你好，今天天气怎么样？
期望：友好的聊天回复
```

## 📸 运行截图

运行截图请查看 `screenshots/` 目录（需自行截图保存）。

## 🎯 面试介绍方式

### 项目亮点

1. **多 Agent 架构**：使用 LangGraph StateGraph 实现灵活的 Agent 路由和协作
2. **RAG 检索增强**：完整的文档处理流水线，支持多种格式
3. **NL-to-SQL**：自然语言到 SQL 的自动转换，无需编写查询语句
4. **分层设计**：清晰的模块划分，高内聚低耦合

### 技术深度

- **LangGraph**：展示对 Agent 工作流编排的理解
- **RAG Pipeline**：文档加载、切片、向量化、检索的完整流程
- **Prompt Engineering**：精心设计的提示词模板
- **结构化输出**：使用 Pydantic 确保输出格式一致性

### 架构设计

- **状态管理**：通过 TypedDict 定义共享状态，支持多 Agent 间数据传递
- **条件路由**：基于问题类型动态选择执行路径
- **可扩展性**：易于添加新的 Agent 类型和功能模块

## 📄 许可证

MIT License

## 📬 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
