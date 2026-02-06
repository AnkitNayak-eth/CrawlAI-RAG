# rag/qa.py

from urllib.parse import urlparse
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_qa_chain(website_url: str, base_dir="vector_db"):
    domain = urlparse(website_url).netloc.replace(".", "_")
    persist_dir = f"{base_dir}/{domain}"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Answer using ONLY the provided website content.

Rules:
- Give a brief but complete answer (4–6 sentences).
- Be clear and informative.
- Do NOT repeat the question.
- Do NOT add information not present in the context.
- If the answer is not found in the context, say so clearly.
- If the user asks for a link (e.g., GitHub, website), look for it in the "Links Found" section of the content.
- If the user asks about projects, prioritize sections marked "PERSONAL PROJECT", "Featured Projects", or distinct project cards over general mentions in testimonials.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 25}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
