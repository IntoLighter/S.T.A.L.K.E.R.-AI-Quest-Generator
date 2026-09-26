from pathlib import Path


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
