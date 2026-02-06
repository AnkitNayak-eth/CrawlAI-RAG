# CrawlAI RAG

**CrawlAI RAG** is an AI-powered website intelligence platform that allows users to **crawl entire websites, index their content, and ask natural-language questions** using **Retrieval-Augmented Generation (RAG)**.

It transforms static websites into **queryable knowledge bases**.

---

## Key Features

### Website Crawling
- Crawls all internal pages of a website  
- Extracts clean, readable text  

### RAG-Based Question Answering
- Uses vector embeddings + LLM  
- Answers are grounded in website content  
- Minimizes hallucinations  

### Multi-Website Indexing
- Index multiple websites  
- All content stored in a shared vector database  

### Fast & Scalable Backend
- Built with FastAPI  
- ChromaDB for vector storage  

### Simple Frontend
- Built with Streamlit  
- Clean, single-query interface  

### Secure Configuration
- Environment variables via `.env`  
- API keys are never committed to GitHub  

---

## Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | FastAPI |
| Frontend | Streamlit |
| AI / RAG | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence-Transformers |
| LLM | Groq (LLaMA 3.3 70B) |
| Web Scraping | BeautifulSoup4 & Playwright |
| Configuration | python-dotenv |

---

## Usage Guide

### 1. Index a Website
1. Enter a website URL  
2. Click **Index Website**  
3. Website content is crawled, chunked, and embedded  

### 2. Ask Questions
Ask natural-language questions such as:
- What is this website about?  
- List all services mentioned  
- Who is the author?  

The system returns **accurate, grounded answers** based only on the indexed website content.

---

## How It Works

1. Website is crawled and text is extracted  
2. Text is split into manageable chunks  
3. Embeddings are generated and stored in ChromaDB  
4. User query retrieves the most relevant chunks  
5. LLM generates an answer using retrieved context  

This is **true Retrieval-Augmented Generation (RAG)**.

---

## Use Cases

- Website documentation Q&A  
- Internal knowledge bases  
- Research and analysis  
- Client website intelligence  
- Portfolio / demo RAG application  

---

## Author

**CrawlAI RAG**  
Built by **Ankit Kumar Nayak**

---

## Support

If you like this project:
- Give it a **star**
- Fork it
- Contribute or suggest improvements
