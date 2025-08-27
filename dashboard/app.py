import streamlit as st, requests, pandas as pd
import json
from libs.app_config.config import LLM_MODEL, OLLAMA_URL

st.title("YC Startups Explorer")

# Filters for tag, minimum and max funding
tag = st.sidebar.text_input("Filter by tag")
min_funding = st.sidebar.number_input("Min Funding ($)", value=0)
max_funding = st.sidebar.number_input("Max Funding ($)", value=1e12)
limit = st.sidebar.number_input("Number of Companies", value=100)

params = {"tag": tag} if tag else {}
params["min_funding"] = min_funding
params["max_funding"] = max_funding
params["limit"] = limit

# Get the data with the specified params from fastapi backend
try:
    resp = requests.get("http://fastapi:8000/startups/", params=params)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    df = pd.DataFrame()

# Charts showing the funding data
if not df.empty and "Company" in df.columns and "funding" in df.columns:
    st.subheader("Funding per Startup")
    
    chart_data = df[["Company", "funding"]].set_index("Company").sort_values("funding", ascending=False)
    st.bar_chart(chart_data)

# Use ollama model to get insights
st.subheader("AI Summary Assistant")
user_query = st.text_input("Ask something about these startups")

if user_query and not df.empty:
    context_df = df[["Company", "CEO", "locations", "tags","industries", "team_size", "funding"]]

    prompt = f"""
    You are an AI summary assistant on a website. Your job is to answer questions from the client using ONLY the CSV provided.
    Answer the question below using this CSV data on YC startups. Keep your answer short and concise:
    {context_df.to_csv(index=False)}

    Client's Question: {user_query}
    
    Answer:
    """
    response = requests.post(
        url=OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "options": {
                "temperature": 0.1
            }
            },
        timeout=200,
        stream=True
    )
    full_response = ""
    for chunk in response.iter_lines():
        if chunk:
            data = json.loads(chunk.decode('utf-8'))
            full_response += data.get("response", "")
    st.success(full_response)
    
st.dataframe(df)