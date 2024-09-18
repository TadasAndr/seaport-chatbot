from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    RETRIEVER_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
