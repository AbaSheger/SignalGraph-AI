from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str = "sgadmin"
    db_password: str = "changeme"
    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "signalgraph"
    test_database_url: str = "sqlite+aiosqlite:///./test.db"
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 64
    max_chunks_retrieved: int = 5
    llm_provider: str = "mock"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


settings = Settings()
