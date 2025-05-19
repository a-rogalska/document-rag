import streamlit as st
from storage import StorageClient

st.title("📝 Add Documents")

storage_client = StorageClient()

uploaded_file = st.file_uploader("Upload new document", type=("jpg", "jpeg", "pdf", "png"))

if uploaded_file:
    storage_client.upload_blob(uploaded_file.read(), container_name="files", filename=uploaded_file.name)
