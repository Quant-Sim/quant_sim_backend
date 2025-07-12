from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        # 아래 한 줄을 추가합니다.
        extra = "ignore"

settings = Settings()