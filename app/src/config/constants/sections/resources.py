from pydantic import BaseModel
from util.resource import read_resource


class ResourcesConfig(BaseModel):
    default_concept_prompt: str = read_resource(":/prompt/concept.txt")
    default_metadata_prompt: str = read_resource(":/prompt/metadata.txt")
    default_icon_prompt: str = read_resource(":/prompt/icon.txt")

    icon_path: str = ":/icon/icon.ico"

    default_icon_workflow: str = read_resource(":/workflow/icon.json")
