import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

def is_streamlit_cloud():
    return os.environ.get('STREAMLIT_RUNTIME') == 'streamlit_cloud'

if not is_streamlit_cloud():
    load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    RETRIEVER_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def load(cls):
        if is_streamlit_cloud():
            import streamlit as st
            env_vars = {}
            for field in cls.__fields__:
                value = st.secrets.get(field)
                if value is not None:
                    env_vars[field] = value
        else:
            env_vars = {field: os.getenv(field) for field in cls.__fields__ if os.getenv(field) is not None}
        
        return cls(**env_vars)

# Create the config object
try:
    config = Settings.load()
except Exception as e:
    print(f"Error loading configuration: {str(e)}")
    raise