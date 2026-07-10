import streamlit as st
import requests
import uuid

API_BASE = "http://localhost:8000"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Charging AI Agent Demo", page_icon="⚡", layout="wide")

st.title("⚡ 充电业务AI助手")
st.subheader("基于LangGraph和RAG的智能问答系统")

with st.sidebar:
    st.header("功能说明")
    st.markdown("""
    - **Knowledge Agent**: 基于RAG的知识库问答
    - **Data Agent**: 自然语言转SQL查询
    - **Chat Agent**: 普通聊天对话
    """)
    
    uploaded_file = st.file_uploader("上传知识文档", type=["pdf", "txt", "md"])
    if uploaded_file is not None:
        with st.spinner("上传中..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = requests.post(f"{API_BASE}/upload", files=files)
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"上传失败: {response.json().get('error', '未知错误')}")
            except Exception as e:
                st.error(f"连接失败: {e}")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "agent" in message and message["agent"]:
            st.caption(f"Agent: {message['agent']}")
        if "source" in message and message["source"]:
            with st.expander("查看引用来源"):
                st.markdown(message["source"])

if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                response = requests.post(
                    f"{API_BASE}/chat",
                    json={"message": prompt, "session_id": st.session_state.session_id}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result["answer"])
                    
                    if result["agent"]:
                        st.caption(f"Agent: {result['agent']}")
                    
                    if result["source"] and result["source"] != "无引用来源":
                        with st.expander("查看引用来源"):
                            st.markdown(result["source"])
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "agent": result["agent"],
                        "source": result["source"]
                    })
                else:
                    st.error(f"请求失败: {response.json().get('detail', '未知错误')}")
            except Exception as e:
                st.error(f"连接失败: {e}")
