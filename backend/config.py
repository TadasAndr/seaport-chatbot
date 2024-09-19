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
        
        print("Initializing Settings...")
        
        # Check if running on Streamlit Cloud
        if 'STREAMLIT_SHARING_MODE' in os.environ:
            print("Running on Streamlit Cloud")
            # Use Streamlit secrets
            self.OPENAI_API_KEY = st.secrets.get("OPENAI", {}).get("API_KEY", "") or st.secrets.get("OPENAI_API_KEY", "")
            self.PINECONE_API_KEY = st.secrets.get("PINECONE", {}).get("API_KEY", "") or st.secrets.get("PINECONE_API_KEY", "")
            self.RETRIEVER_K = st.secrets.get("RETRIEVER", {}).get("K", 5) or st.secrets.get("RETRIEVER_K", 5)
            
            print(f"Secrets keys: {list(st.secrets.keys())}")
            if "OPENAI" in st.secrets:
                print(f"OPENAI secret keys: {list(st.secrets.OPENAI.keys())}")
            if "PINECONE" in st.secrets:
                print(f"PINECONE secret keys: {list(st.secrets.PINECONE.keys())}")
            if "RETRIEVER" in st.secrets:
                print(f"RETRIEVER secret keys: {list(st.secrets.RETRIEVER.keys())}")
        else:
            print("Running locally")
            # For local development, use environment variables
            self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", self.OPENAI_API_KEY)
            self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", self.PINECONE_API_KEY)
            self.RETRIEVER_K = int(os.getenv("RETRIEVER_K", self.RETRIEVER_K))

        print(f"OPENAI_API_KEY set: {'Yes' if self.OPENAI_API_KEY else 'No'}")
        print(f"PINECONE_API_KEY set: {'Yes' if self.PINECONE_API_KEY else 'No'}")
        print(f"RETRIEVER_K: {self.RETRIEVER_K}")

        # Validate that required keys are not empty
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        if not self.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set")

print("Creating Settings instance...")
config = Settings()
print("Settings instance created successfully")