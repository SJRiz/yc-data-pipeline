import streamlit as st, requests, pandas as pd
st.title("YC Startups Explorer")

tag = st.text_input("Filter by tag")
params = {"tag": tag} if tag else {}
resp = requests.get("http://fastapi:8000/startups/", params=params)
df = pd.DataFrame(resp.json())
st.dataframe(df)
