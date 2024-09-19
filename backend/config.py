from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Dict

def streamlit_secrets_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A settings source that loads variables from Streamlit secrets.
    """
    try:
        import streamlit as st
        return dict(st.secrets)
    except ImportError:
        return {}

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    RETRIEVER_K: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        # Customize sources to include Streamlit secrets
        customise_sources=lambda init_settings, env_settings, file_secret_settings: (
            init_settings,
            streamlit_secrets_settings_source,
            env_settings,
            file_secret_settings,
        ),
    )

config = Settings()
