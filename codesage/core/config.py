from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CODESAGE_", case_sensitive=False)

    db_url: str = "sqlite:///./codesage.db"
    data_dir: Path = Path("./.data")
    clone_dir_name: str = "repos"

    embedding_model: str = "microsoft/codebert-base"
    embedding_max_length: int = 256

settings = Settings()
