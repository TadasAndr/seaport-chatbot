import os
import streamlit as st
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

print("Environment variables:")
for key, value in os.environ.items():
    if key.startswith(('OPENAI', 'PINECONE', 'RETRIEVER')):
        print(f"{key}: {'*' * len(value)}")

print("\nStreamlit secrets:")
if hasattr(st, 'secrets'):
    for key in st.secrets:
        if isinstance(st.secrets[key], dict):
            print(f"{key}:")
            for subkey, value in st.secrets[key].items():
                print(f"  {subkey}: {'*' * len(str(value))}")
        else:
            print(f"{key}: {'*' * len(str(st.secrets[key]))}")
else:
    print("No Streamlit secrets found")

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    PINECONE_API_KEY: str = ""
    RETRIEVER_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        print("\nInitializing Settings...")
        
        if 'STREAMLIT_SHARING_MODE' in os.environ:
            print("Running on Streamlit Cloud")
            self.OPENAI_API_KEY = st.secrets.get("OPENAI", {}).get("API_KEY", "") or st.secrets.get("OPENAI_API_KEY", "")
            self.PINECONE_API_KEY = st.secrets.get("PINECONE", {}).get("API_KEY", "") or st.secrets.get("PINECONE_API_KEY", "")
            self.RETRIEVER_K = st.secrets.get("RETRIEVER", {}).get("K", 5) or st.secrets.get("RETRIEVER_K", 5)
        else:
            print("Running locally")
            self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", self.OPENAI_API_KEY)
            self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", self.PINECONE_API_KEY)
            self.RETRIEVER_K = int(os.getenv("RETRIEVER_K", self.RETRIEVER_K))

        print(f"OPENAI_API_KEY set: {'Yes' if self.OPENAI_API_KEY else 'No'}")
        print(f"PINECONE_API_KEY set: {'Yes' if self.PINECONE_API_KEY else 'No'}")
        print(f"RETRIEVER_K: {self.RETRIEVER_K}")

        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        if not self.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set")

print("\nCreating Settings instance...")
config = Settings()
print("Settings instance created successfully")