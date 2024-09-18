from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from backend.config import config


def get_pinecone():
    return Pinecone(api_key=config.PINECONE_API_KEY)


def create_vector_store(index_name, chunks, model='text-embedding-ada-002'):
    pc = get_pinecone()
    embeddings = OpenAIEmbeddings(model=model)

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine'
        )

    index = pc.Index(index_name)

    # Change this line
    vector_store = PineconeVectorStore(index, embeddings, "text")

    vector_store.add_documents(chunks)

    return vector_store


def load_vector_store(index_name, model='text-embedding-ada-002', dimension=1536):
    pc = get_pinecone()
    embeddings = OpenAIEmbeddings(model=model)

    print(f"Attempting to load index '{index_name}'")

    if index_name not in pc.list_indexes().names():
        print(f"Index '{index_name}' does not exist. Creating it now.")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' found.")

    index = pc.Index(index_name)

    vector_store = PineconeVectorStore(index, embeddings, "text")
    print(f"Vector store loaded successfully. Stats: {index.describe_index_stats()}")
    return vector_store


def delete_vector_store_index(index_name='all'):
    pc = get_pinecone()
    if index_name == 'all':
        indexes = pc.list_indexes().names()
        for index in indexes:
            pc.delete_index(index)
    else:
        pc.delete_index(index_name)