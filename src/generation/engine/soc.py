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
        task = f"""
<game_task id="{title_english}">
    <title>{metadata.title}</title>
    <objective>
        <text>{metadata.title}</text>
        <icon>{title_english}_icon</icon>
        <article>{title_english}_article</article>
        <infoportion_complete>{title_english}_done_info</infoportion_complete>
    </objective>
            """.strip()

        for i, objective in enumerate(metadata.objectives):
            if i == len(metadata.objectives) - 1:
                subtask_text = f"""
    <objective>
        <text>{objective.title}</text>
        <infoportion_complete>{title_english}_done_info</infoportion_complete>
    </objective>
                """.rstrip()
            else:
                subtask_text = f"""
    <objective>
        <text>{objective.title}</text>
    </objective>
                """.rstrip()

            task += subtask_text

        task += "\n</game_task>"
        return task

    @classmethod
    def create_article(cls, metadata: Metadata, title_english: str):
        return f"""
<article id="{title_english}_article" name="task" article_type="task" group="task">
    <text>{metadata.description}</text>
</article>
        """.strip()

    @classmethod
    def create_infoportions(cls, title_english: str):
        return f"""
<info_portion id="{title_english}_start_info">
    <task>{title_english}</task>
</info_portion>
<info_portion id="{title_english}_done_info"></info_portion>
        """.strip()

    @classmethod
    def create_icon(cls, icon: Image.Image):
        return icon.resize((83, 47), Image.Resampling.LANCZOS)
