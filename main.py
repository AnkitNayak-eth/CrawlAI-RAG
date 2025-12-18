from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from scraper.crawler import crawl_website
from rag.chunker import chunk_text
from rag.vectorstore import create_vectorstore
from rag.qa import get_qa_chain

app = FastAPI()

qa_chain = None  # global


@app.on_event("startup")
def startup_event():
    global qa_chain
    qa_chain = get_qa_chain()


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.post("/ingest")
def ingest(url: str):
    pages = crawl_website(url)
    chunks = chunk_text(pages)
    create_vectorstore(chunks)

    return {
        "pages_scraped": len(pages),
        "chunks_created": len(chunks),
        "status": "Website indexed"
    }


@app.post("/ask")
def ask(question: str):
    result = qa_chain.invoke(question)
    return {"answer": result}
