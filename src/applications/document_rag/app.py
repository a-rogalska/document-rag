import logging

import streamlit as st

logging.basicConfig(level=logging.INFO)

chatbot = st.Page("pages/chatbot.py", title="Chatbot", icon="✅")
add_documents = st.Page("pages/add_documents.py", title="Add Documents", icon="📝")
documents = st.Page("pages/documents.py", title="All Documents", icon="📄")

pg = st.navigation([chatbot, add_documents, documents])

pg.run()
