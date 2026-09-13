import shlex
import subprocess
from pathlib import Path

SOURCE_DIR = Path("app/src")
OUTPUT_FILE = Path("app/resource/translation/main.ts")

EXCLUDED_FILES = [
    "rc_main.py",
]


def main() -> None:
    source_files = sorted(
        path for path in SOURCE_DIR.rglob("*.py") if path.name not in EXCLUDED_FILES
    )

    command = [
        "pyside6-lupdate",
        *map(str, source_files),
        "-ts",
        str(OUTPUT_FILE),
    ]

    print(shlex.join(command))

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
