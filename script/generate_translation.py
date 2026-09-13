import shlex
import subprocess
from pathlib import Path

SOURCE_DIR = Path("app/src")
TRANSLATION_DIR = Path("app/resource/translation")

OUTPUT_FILES = {
    "ru": TRANSLATION_DIR / "ru.ts",
    "en": TRANSLATION_DIR / "en.ts",
}

EXCLUDED_FILES = {
    "rc_main.py",
}


def main() -> None:
    source_files = sorted(
        path for path in SOURCE_DIR.rglob("*.py") if path.name not in EXCLUDED_FILES
    )

    for language, output_file in OUTPUT_FILES.items():
        command = [
            "pyside6-lupdate",
            *map(str, source_files),
            "-target-language",
            language,
            "-ts",
            str(output_file),
        ]

        print(shlex.join(command))
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
