from functools import lru_cache

from config.constants.main import constants_config
from jinja2 import DictLoader, Environment, Template
from PIL import Image

from generation.entity import Metadata, QuestData

TASK_TEMPLATE = "task.xml.j2"
ARTICLE_TEMPLATE = "article.xml.j2"
INFOPORTIONS_TEMPLATE = "infoportions.xml.j2"

ICON_SIZE = (83, 47)


class QuestBuilder:
    @classmethod
    def create_quest_data(cls, metadata: Metadata, title_english: str) -> QuestData:
        return QuestData(
            task=cls.create_task(metadata, title_english),
            article=cls.create_article(metadata, title_english),
            infoportions=cls.create_infoportions(title_english),
        )

    @classmethod
    def create_task(cls, metadata: Metadata, title_english: str) -> str:
        return cls._render(
            TASK_TEMPLATE,
            title_id=title_english,
            title=metadata.title,
            objectives=[objective.title for objective in metadata.objectives],
        )

    @classmethod
    def create_article(cls, metadata: Metadata, title_english: str) -> str:
        return cls._render(
            ARTICLE_TEMPLATE,
            title_id=title_english,
            description=metadata.description,
        )

    @classmethod
    def create_infoportions(cls, title_english: str) -> str:
        return cls._render(INFOPORTIONS_TEMPLATE, title_id=title_english)

    @classmethod
    def create_icon(cls, icon: Image.Image) -> Image.Image:
        return icon.resize(ICON_SIZE, Image.Resampling.LANCZOS)

    @classmethod
    def _render(cls, template_name: str, **context: str | list[str]) -> str:
        return cls._get_template(template_name).render(**context)

    @classmethod
    def _get_template(cls, template_name: str) -> Template:
        return cls._get_environment().get_template(template_name)

    @classmethod
    @lru_cache
    def _get_environment(cls) -> Environment:
        resources = constants_config.resources
        return Environment(
            loader=DictLoader(
                {
                    TASK_TEMPLATE: resources.task_template,
                    ARTICLE_TEMPLATE: resources.article_template,
                    INFOPORTIONS_TEMPLATE: resources.infoportions_template,
                }
            ),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=False,
        )
