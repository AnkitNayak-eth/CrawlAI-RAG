import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="CrawlAI RAG", layout="centered")
st.title("CrawlAI RAG")

# -------------------------------
# 1. Website Ingestion
# -------------------------------
st.subheader("1. Index a Website")

with st.form("ingest_form"):
    website_url = st.text_input(
        "Enter website URL",
        placeholder="https://example.com"
    )
    ingest_submit = st.form_submit_button("Index Website")

if ingest_submit:
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
# 2. Ask Questions (Press Enter)
# -------------------------------
st.subheader("2. Ask Questions")

with st.form("ask_form"):
    question = st.text_input(
        "Ask something about the website",
        placeholder="What is this website about?"
    )
    ask_submit = st.form_submit_button("Ask")

if ask_submit:
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
            response = res.json()["answer"]

            # Extract clean text
            if isinstance(response, dict) and "result" in response:
                answer_text = response["result"]
            else:
                answer_text = response

            st.markdown("### Answer")
            st.write(answer_text)
        else:
            st.error("Failed to get answer")
