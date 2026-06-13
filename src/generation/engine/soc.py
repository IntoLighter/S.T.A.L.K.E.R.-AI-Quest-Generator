from xml.sax.saxutils import escape as xml_escape

from PIL import Image

from generation.entity import Metadata, GameRecords


class SoCObjectFactory:
    @classmethod
    def create_game_records(
        cls, metadata: Metadata, title_english: str
    ) -> GameRecords:
        return GameRecords(
            cls.create_task(metadata, title_english),
            cls.create_article(metadata, title_english),
            cls.create_infoportions(title_english),
        )

    @classmethod
    def create_task(cls, metadata: Metadata, title_english: str):
        title = cls._xml_text(metadata.title)
        title_id = cls._xml_attr(title_english)
        title_id_text = cls._xml_text(title_english)

        task = f"""
<game_task id="{title_id}">
    <title>{title}</title>
    <objective>
        <text>{title}</text>
        <icon>{title_id_text}_icon</icon>
        <article>{title_id_text}_article</article>
        <infoportion_complete>{title_id_text}_done_info</infoportion_complete>
    </objective>
            """.strip()

        for i, objective in enumerate(metadata.objectives):
            objective_title = cls._xml_text(objective.title)
            if i == len(metadata.objectives) - 1:
                subtask_text = f"""
    <objective>
        <text>{objective_title}</text>
        <infoportion_complete>{title_id_text}_done_info</infoportion_complete>
    </objective>
                """.rstrip()
            else:
                subtask_text = f"""
    <objective>
        <text>{objective_title}</text>
    </objective>
                """.rstrip()

            task += subtask_text

        task += "\n</game_task>"
        return task

    @classmethod
    def create_article(cls, metadata: Metadata, title_english: str):
        title_id = cls._xml_attr(title_english)
        description = cls._xml_text(metadata.description)
        return f"""
<article id="{title_id}_article" name="task" article_type="task" group="task">
    <text>{description}</text>
</article>
        """.strip()

    @classmethod
    def create_infoportions(cls, title_english: str):
        title_id = cls._xml_attr(title_english)
        title_id_text = cls._xml_text(title_english)
        return f"""
<info_portion id="{title_id}_start_info">
    <task>{title_id_text}</task>
</info_portion>
<info_portion id="{title_id}_done_info"></info_portion>
        """.strip()

    @classmethod
    def create_icon(cls, icon: Image.Image):
        return icon.resize((83, 47), Image.Resampling.LANCZOS)

    @staticmethod
    def _xml_text(value: str) -> str:
        return xml_escape(value)

    @staticmethod
    def _xml_attr(value: str) -> str:
        xml_attr_entities = {'"': "&quot;", "'": "&apos;"}
        return xml_escape(value, xml_attr_entities)
