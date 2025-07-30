import streamlit as st, requests, pandas as pd

st.title("YC Startups Explorer")

tag = st.text_input("Filter by tag")
params = {"tag": tag} if tag else {}

try:
    resp = requests.get("http://fastapi:8000/startups/", params=params)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    df = pd.DataFrame()

st.dataframe(df)