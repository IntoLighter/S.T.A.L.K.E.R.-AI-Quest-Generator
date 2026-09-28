from pydantic_settings import BaseSettings


class LayoutConfig(BaseSettings):
    window_size: tuple[int, int] = (1280, 720)
    dialog_size: tuple[int, int] = (1024, 576)
    quest_generated_tray_message_msecs: int = 5000

    editor_stretch: int = 1
    concept_stretch: int = 4
    metadata_stretch: int = 2
    icon_prompt_stretch: int = 2

    editor_height: int = 100
    concept_height: int = editor_height * concept_stretch
    metadata_height: int = editor_height * metadata_stretch
    icon_prompt_height: int = editor_height * icon_prompt_stretch

    icon_workflow_stretch: int = 4
    icon_workflow_height: int = editor_height * icon_workflow_stretch


layout_config = LayoutConfig()
