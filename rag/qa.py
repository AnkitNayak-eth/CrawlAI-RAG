from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_qa_chain(persist_dir="vector_db"):
    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    # Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # LLM (low temperature for factual answers)
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    # ✅ Prompt to control answer length & quality
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an AI assistant answering questions using ONLY the provided website content.

Rules:
- Give a brief but complete answer (4–6 sentences).
- Be clear and informative.
- Do NOT repeat the question.
- Do NOT add information not present in the context.
- If the answer is not found in the context, say so clearly.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    # QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    return qa_chain
