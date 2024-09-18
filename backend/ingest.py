import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from tools.document_loader import load_document
from backend.vectorstore import create_vector_store
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken


def chunk_data(data, chunk_size=1500):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=200)
    chunks = text_splitter.split_documents(data)
    return chunks


def calculate_embedding_cost(chunks):
    """Calculates the embedding cost for a list of chunks using the OpenAI Ada 002 tokenizer."""
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    total_tokens = sum(len(encoding.encode(chunk.page_content)) for chunk in chunks)
    cost = (total_tokens / 1000) * 0.0004
    return cost


def main():
    index_name = 'seaport-chatbot'
    pdf_file = r'../rinkliavu_taisykles.pdf'

    data = load_document(pdf_file)

    chunks = chunk_data(data)

    create_vector_store(index_name, chunks)


if __name__ == '__main__':
    main()
