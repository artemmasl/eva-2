from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: str = "http://localhost:5173"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "eva_2"

    yandex_folder_id: str = ""
    yandex_api_key: str = ""
    yandex_model: str = "yandexgpt"

    admin_password: str = "admin"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
