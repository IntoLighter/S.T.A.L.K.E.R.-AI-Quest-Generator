import shlex
import subprocess
from pathlib import Path
from typing import TypedDict


class GroupSettings(TypedDict):
    function: str
    languages: list[str]


SOURCE_DIR = Path("app")
TS_DIR = Path("app/resources/translations")
QM_DIR = Path("app/resources/files/translations")

GROUPS: dict[str, GroupSettings] = {
    "ui": {"function": "ui", "languages": ["ru"]},
    "errors": {"function": "err", "languages": ["ru", "en"]},
}

EXCLUDED_FILES = {
    "rc_main.py",
}


def run(command: list[str]) -> None:
    print(shlex.join(command))
    subprocess.run(command, check=True)


def update_ts(source_files: list[str], function: str, ts_file: Path) -> None:
    run(
        [
            "pyside6-lupdate",
            *source_files,
            "-tr-function-alias",
            f"tr={function}",
            "-target-language",
            ts_file.stem.split("_")[-1],
            "-ts",
            str(ts_file),
        ]
    )


def main() -> None:
    source_files = sorted(
        str(path)
        for path in SOURCE_DIR.rglob("*.py")
        if path.name not in EXCLUDED_FILES
    )
    TS_DIR.mkdir(parents=True, exist_ok=True)
    QM_DIR.mkdir(parents=True, exist_ok=True)

    for group, settings in GROUPS.items():
        for language in settings["languages"]:
            ts_file = TS_DIR / f"{group}_{language}.ts"
            update_ts(source_files, settings["function"], ts_file)
            run(
                [
                    "pyside6-lrelease",
                    str(ts_file),
                    "-qm",
                    str(QM_DIR / f"{group}_{language}.qm"),
                ]
            )


if __name__ == "__main__":
    main()
