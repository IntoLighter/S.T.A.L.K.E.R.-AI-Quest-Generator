from pydantic import BaseModel
from util.resource import read_resource


class ResourcesConfig(BaseModel):
    default_concept_prompt: str = read_resource(":/prompt/concept.txt")
    default_metadata_prompt: str = read_resource(":/prompt/metadata.txt")
    default_icon_prompt: str = read_resource(":/prompt/icon.txt")

    icon_path: str = ":/icon/icon.ico"

    default_icon_workflow: str = read_resource(":/workflow/icon.json")

    task_template: str = read_resource(":/templates/quest_data/task.xml.j2")
    article_template: str = read_resource(":/templates/quest_data/article.xml.j2")
    infoportions_template: str = read_resource(
        ":/templates/quest_data/infoportions.xml.j2"
    )
