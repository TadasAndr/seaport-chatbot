from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

def streamlit_secrets_settings(settings):
    try:
        import streamlit as st
        return st.secrets
    except ImportError:
        # Not running in Streamlit, return empty dict
        return {}

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    RETRIEVER_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                init_settings,
                streamlit_secrets_settings,
                env_settings,
                file_secret_settings,
            )

config = Settings()