from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
     
    app_name: str = 'ResumeIQ'
    debug: bool = False

    database_user: str
    database_password: str

    database_host: str #
    database_port: int #

    database_name: str #


    @property
    def database_url(self) -> str: 
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
        
settings = Settings()