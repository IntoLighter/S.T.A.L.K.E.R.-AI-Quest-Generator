from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    version: str = "1.0"
    name: str = "S.T.A.L.K.E.R. AI Quest Generator"
    repository: str = "https://github.com/IntoLighter/S.T.A.L.K.E.R.-AI-Quest-Generator"


app_config = AppConfig()
