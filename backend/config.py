from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import streamlit as st

# Try to load .env file if it exists (for local development)
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    PINECONE_API_KEY: str = ""
    RETRIEVER_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if 'STREAMLIT_SHARING_MODE' in os.environ:
            self.OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", self.OPENAI_API_KEY)
            self.PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY", self.PINECONE_API_KEY)
            self.RETRIEVER_K = st.secrets.get("RETRIEVER_K", self.RETRIEVER_K)
        else:
            self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", self.OPENAI_API_KEY)
            self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", self.PINECONE_API_KEY)
            self.RETRIEVER_K = int(os.getenv("RETRIEVER_K", self.RETRIEVER_K))

config = Settings()
