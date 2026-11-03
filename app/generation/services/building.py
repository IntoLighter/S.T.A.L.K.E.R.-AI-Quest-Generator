from functools import lru_cache

from config.constants.main import constants_config
from jinja2 import DictLoader, Environment

from generation.entity import Metadata, QuestData

TASK_TEMPLATE = "task.xml.j2"
ARTICLE_TEMPLATE = "article.xml.j2"
INFOPORTIONS_TEMPLATE = "infoportions.xml.j2"


def create_quest_data(metadata: Metadata, quest_id: str) -> QuestData:
    return QuestData(
        task=create_task(metadata, quest_id),
        article=create_article(metadata, quest_id),
        infoportions=create_infoportions(quest_id),
    )


def create_task(metadata: Metadata, quest_id: str) -> str:
    return _render(
        TASK_TEMPLATE,
        title_id=quest_id,
        title=metadata.title,
        objectives=[objective.title for objective in metadata.objectives],
    )


def create_article(metadata: Metadata, quest_id: str) -> str:
    return _render(
        ARTICLE_TEMPLATE,
        title_id=quest_id,
        description=metadata.description,
    )


def create_infoportions(quest_id: str) -> str:
    return _render(INFOPORTIONS_TEMPLATE, title_id=quest_id)


def _render(template_name: str, **context: str | list[str]) -> str:
    return _get_environment().get_template(template_name).render(**context)


@lru_cache
def _get_environment() -> Environment:
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
