import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Website RAG", layout="centered")
st.title("Website RAG Analyzer")

# -------------------------------
# 1. Website Ingestion
# -------------------------------
st.subheader("1. Index a Website")

website_url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

if st.button("Index Website"):
    if not website_url:
        st.warning("Please enter a website URL")
    else:
        with st.spinner("Scraping and indexing website..."):
            res = requests.post(
                f"{BACKEND_URL}/ingest",
                params={"url": website_url},
                timeout=300
            )

        if res.status_code == 200:
            st.success("Website indexed successfully")
        else:
            st.error("Failed to index website")

st.divider()

# -------------------------------
# 2. Ask Questions (Text Only)
# -------------------------------
st.subheader("2. Ask Questions")

question = st.text_input(
    "Ask something about the website",
    placeholder="What is this website about?"
)

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{BACKEND_URL}/ask",
                params={"question": question},
                timeout=120
            )

        if res.status_code == 200:
            response_json = res.json()["answer"]

            # ✅ Extract clean text only
            if isinstance(response_json, dict) and "result" in response_json:
                answer_text = response_json["result"]
            else:
                answer_text = response_json

            st.markdown("### Question")
            st.write(question)

            st.markdown("### Answer")
            st.write(answer_text)
        else:
            st.error("Failed to get answer")
