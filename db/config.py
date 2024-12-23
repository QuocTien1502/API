from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_password_test_connect: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = r"C:\Users\LinLin Ahihi\PycharmProject\Backend_FastAPI\.venv\.env"



settings = Settings()

# print("Database Hostname:", settings.database_hostname)
