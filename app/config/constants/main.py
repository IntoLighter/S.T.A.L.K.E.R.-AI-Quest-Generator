from pydantic_settings import BaseSettings

from config.constants.sections.app import AppConfig
from config.constants.sections.endpoints import EndpointsConfig
from config.constants.sections.paths import PathsConfig
from config.constants.sections.resources import ResourcesConfig
from config.constants.sections.ui import UIConfig


class ConstantsConfig(BaseSettings):
    app: AppConfig = AppConfig()
    endpoints: EndpointsConfig = EndpointsConfig()
    paths: PathsConfig = PathsConfig()
    resources: ResourcesConfig = ResourcesConfig()
    ui: UIConfig = UIConfig()


constants_config = ConstantsConfig()
