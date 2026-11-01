import re
from pathlib import Path

INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_FILENAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def sanitize_filename(name: str, max_length: int) -> str:
    sanitized = " ".join(INVALID_FILENAME_CHARS.sub(" ", name).split())
    sanitized = sanitized[:max_length].rstrip(" .")

    if sanitized.split(".")[0].upper() in RESERVED_FILENAMES:
        sanitized = f"_{sanitized}"

    return sanitized


def get_unique_name_path(path: Path) -> Path:
    new_path = path
    counter = 1

    while new_path.exists():
        new_path = new_path.with_name(f"{path.name} {counter}")
        counter += 1

    return new_path


def get_unique_counter_name_path(path: Path) -> Path:
    counter = 1
    new_path = path / str(counter)

    while new_path.exists():
        counter += 1
        new_path = new_path.with_name(f"{counter}")

    return new_path
