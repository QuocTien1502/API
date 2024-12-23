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
# .env
# DATABASE_HOSTNAME=localhost
# DATABASE_PASSWORD=Tien%40%401994
# DATABASE_PASSWORD_TEST_CONNECT=Tien@@1994
# DATABASE_NAME=instagram
# DATABASE_USERNAME=postgres
# SECRET_KEY=1bc6a02d984424fa808b7d2484e7e846a704fd3b59942c26eab9cd3160d0a5cb
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
