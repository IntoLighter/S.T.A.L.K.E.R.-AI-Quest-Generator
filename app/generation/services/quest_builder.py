from functools import lru_cache

from config.constants.main import constants_config
from jinja2 import DictLoader, Environment, Template

from generation.entity import Metadata, QuestData

TASK_TEMPLATE = "task.xml.j2"
ARTICLE_TEMPLATE = "article.xml.j2"
INFOPORTIONS_TEMPLATE = "infoportions.xml.j2"


class QuestBuilder:
    @classmethod
    def create_quest_data(cls, metadata: Metadata, quest_id: str) -> QuestData:
        return QuestData(
            task=cls.create_task(metadata, quest_id),
            article=cls.create_article(metadata, quest_id),
            infoportions=cls.create_infoportions(quest_id),
        )

    @classmethod
    def create_task(cls, metadata: Metadata, quest_id: str) -> str:
        return cls._render(
            TASK_TEMPLATE,
            title_id=quest_id,
            title=metadata.title,
            objectives=[objective.title for objective in metadata.objectives],
        )

    @classmethod
    def create_article(cls, metadata: Metadata, quest_id: str) -> str:
        return cls._render(
            ARTICLE_TEMPLATE,
            title_id=quest_id,
            description=metadata.description,
        )

    @classmethod
    def create_infoportions(cls, quest_id: str) -> str:
        return cls._render(INFOPORTIONS_TEMPLATE, title_id=quest_id)

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
