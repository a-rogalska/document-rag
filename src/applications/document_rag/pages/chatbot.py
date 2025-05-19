import uuid

import streamlit as st
from rag import graph

st.title("✅ Chat")

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = uuid.uuid4()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    config = {"configurable": {"thread_id": st.session_state['thread_id']}}
    response = graph.invoke({"messages": [{"role": "user", "content": prompt}]}, config=config)
    msg = response["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
