from pydantic_settings import BaseSettings, SettingsConfigDict

from config.preferences.sections.configurator import ConfiguratorConfig
from config.preferences.sections.general import GeneralConfig
from config.preferences.sections.model import ModelConfig
from config.preferences.sections.prompt import PromptConfig


class PreferencesConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        validate_by_name=True,
    )

    general: GeneralConfig = GeneralConfig()
    model: ModelConfig = ModelConfig()
    prompt: PromptConfig = PromptConfig()
    configurator: ConfiguratorConfig = ConfiguratorConfig()
