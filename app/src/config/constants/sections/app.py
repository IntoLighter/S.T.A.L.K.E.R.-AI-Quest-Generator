from pydantic import BaseModel


class AppConfig(BaseModel):
    version: str = "1.2.0"
    name: str = "S.T.A.L.K.E.R. AI Quest Generator"
    repository: str = "https://github.com/IntoLighter/S.T.A.L.K.E.R.-AI-Quest-Generator"
