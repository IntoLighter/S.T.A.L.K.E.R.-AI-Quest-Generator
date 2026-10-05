from pydantic import BaseModel


class ConfiguratorConfig(BaseModel):
    concept: str = ""
    metadata: str = ""
    icon_prompt: str = ""
