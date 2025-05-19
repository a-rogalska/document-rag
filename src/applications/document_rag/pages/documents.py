import pandas as pd
import streamlit as st
from storage import StorageClient

st.title("📄 All Documents")

storage_client = StorageClient()

if st.button("Fetch documents"):
    blobs_list = storage_client.get_blobs_with_metadata(container_name='documents')
    df = pd.DataFrame(blobs_list)
    st.table(df)
