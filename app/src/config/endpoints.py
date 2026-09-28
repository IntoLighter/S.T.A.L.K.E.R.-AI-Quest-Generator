from pydantic_settings import BaseSettings


class EndpointsConfig(BaseSettings):
    local_model_base_url: str = "http://127.0.0.1:11434/v1"
    local_model_api_key: str = "Key"
    remote_model_base_url: str = "http://127.0.0.1:8000/v1"
    remote_model_api_key: str = "VerysecretKey"
    comfy_ui_base_url: str = "http://127.0.0.1:8188"


endpoints_config = EndpointsConfig()
