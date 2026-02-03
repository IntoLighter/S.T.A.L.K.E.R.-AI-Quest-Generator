from pydantic_settings import BaseSettings


class TextConfig(BaseSettings):
    default_prompt: str = """
Тип: исследование
Квестодатель: Сидорович
""".strip()

    default_local_model: str = "qwen3:8b"
    default_remote_model: str = "gemini/gemini-flash-latest"

    generate_text: str = "Сгенерировать квест"
    stop_generate_text: str = "Остановить генерацию квеста"
    save_prompt: str = "Сохранить промпт шаблоном"
    reset_text: str = "Сбросить"
    add_parameter_text: str = "Добавить"


text_config = TextConfig()
