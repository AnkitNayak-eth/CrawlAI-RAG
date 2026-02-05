from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from scraper.crawler import crawl_website
from rag.chunker import chunk_text
from rag.vectorstore import create_vectorstore
from rag.qa import get_qa_chain

app = FastAPI()

LAST_WEBSITE = None


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.post("/ingest")
def ingest(url: str):
    global LAST_WEBSITE

    pages = crawl_website(url)
    chunks = chunk_text(pages)
    create_vectorstore(chunks, url)

    LAST_WEBSITE = url

    return {
        "pages_scraped": len(pages),
        "chunks_created": len(chunks),
        "status": "Website indexed"
    }


@app.post("/ask")
def ask(question: str):
    if not LAST_WEBSITE:
        return {"answer": "No website indexed yet."}

    qa_chain = get_qa_chain(LAST_WEBSITE)
    result = qa_chain.invoke(question)

    if isinstance(result, dict) and "result" in result:
        return {"answer": result["result"]}

    return {"answer": str(result)}
