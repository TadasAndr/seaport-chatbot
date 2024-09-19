from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import streamlit as st
import logging

load_dotenv()
logging.info(f"RETRIEVER_K: {config.RETRIEVER_K}")

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
            # Use Streamlit secrets
            self.OPENAI_API_KEY = st.secrets.get("OPENAI", {}).get("API_KEY", "") or st.secrets.get("OPENAI_API_KEY", "")
            self.PINECONE_API_KEY = st.secrets.get("PINECONE", {}).get("API_KEY", "") or st.secrets.get("PINECONE_API_KEY", "")
            self.RETRIEVER_K = st.secrets.get("RETRIEVER", {}).get("K", 5) or st.secrets.get("RETRIEVER_K", 5)
        else:
            self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", self.OPENAI_API_KEY)
            self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", self.PINECONE_API_KEY)
            self.RETRIEVER_K = int(os.getenv("RETRIEVER_K", self.RETRIEVER_K))

        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        if not self.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set")

config = Settings()