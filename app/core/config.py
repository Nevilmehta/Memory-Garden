import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    APP_NAME: str = "AI Memory Garden"
    APP_VERSION: str = "0.1.0"

    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION_NAME: str = os.getenv(
        "QDRANT_COLLECTION_NAME",
        "memory_garden",
    )

    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "all-MiniLM-L6-v2",
    )

    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "memory_garden")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "memory_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "memory_password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5433"))

    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()