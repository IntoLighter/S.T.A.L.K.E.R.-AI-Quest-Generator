from pydantic_settings import BaseSettings


class ConstantsConfig(BaseSettings):
    quest_generated_tray_message_msecs: int = 5000


constants_config = ConstantsConfig()
