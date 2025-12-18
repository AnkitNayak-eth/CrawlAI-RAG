from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text_list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []
    for text in text_list:
        chunks.extend(splitter.split_text(text))

    return chunks
