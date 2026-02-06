from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    chunks = []
    for page in pages:
        chunks.extend(splitter.split_text(page))

    return chunks
