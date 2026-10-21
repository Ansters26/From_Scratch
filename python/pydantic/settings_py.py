from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    api_key:str
    db_user:str
    db_pass:str

settings=Settings()
print(settings.model_dump())
