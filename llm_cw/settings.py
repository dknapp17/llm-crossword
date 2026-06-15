from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE: str = "llm_crossword"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"

settings = Settings()