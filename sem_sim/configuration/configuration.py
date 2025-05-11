from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

# Настройка конфигурации из файла .env и валидация имен переменных окружения
class Config(BaseSettings):
    model_name: str = Field(validation_alias="MODEL_NAME")
    gigachat_credentials: str | None = Field(validation_alias="GIGACHAT_CREDENTIALS", default=None)
    gigachat_scope: str | None = Field(validation_alias="GIGACHAT_SCOPE", default=None)

    sent_thresh: float = Field(validation_alias="SENT_THRESH")
    sim_epsilon: float = Field(validation_alias="SIM_EPSILON")

    project_root: Path = Path(__file__).resolve().parents[2]
    env_file_path: Path = project_root / ".env"

    if env_file_path.is_file():
        model_config = SettingsConfigDict(env_file=env_file_path, extra="ignore", validate_default=False)
    

configuration = Config()