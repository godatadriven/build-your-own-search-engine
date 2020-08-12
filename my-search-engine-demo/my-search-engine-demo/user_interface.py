import os

import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import streamlit as st

st.title("Cognitive search bar")

search_text = st.text_input(
    "Cognitive search bar", value="luxury", max_chars=None, key=None, type="default"
)


index_name = "hotels"
endpoint = os.environ["SEARCH_ENDPOINT"]
credential = AzureKeyCredential(os.environ["ACS_API_KEY"])


search_client = SearchClient(
    endpoint=endpoint, index_name=index_name, credential=credential
)

results = search_client.search(search_text=search_text)
results_df = pd.DataFrame([r for r in results])

search_output = st.dataframe(results_df)
