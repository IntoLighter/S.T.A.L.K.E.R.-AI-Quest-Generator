from pydantic import BaseModel

EDITOR_BASE_HEIGHT = 100


class EditorSize(BaseModel):
    stretch: int

    @property
    def height(self) -> int:
        return EDITOR_BASE_HEIGHT * self.stretch


class UIConfig(BaseModel):
    window_size: tuple[int, int] = (1280, 720)
    dialog_size: tuple[int, int] = (1024, 576)
    quest_generated_tray_message_msecs: int = 5000

    editor_size: EditorSize = EditorSize(stretch=1)
    concept_editor_size: EditorSize = EditorSize(stretch=4)
    metadata_editor_size: EditorSize = EditorSize(stretch=2)
    id_editor_size: EditorSize = EditorSize(stretch=2)
    icon_prompt_editor_size: EditorSize = EditorSize(stretch=2)
    icon_workflow_editor_size: EditorSize = EditorSize(stretch=4)
