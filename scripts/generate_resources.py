import shlex
import subprocess
from collections import defaultdict
from pathlib import Path, PurePosixPath

RESOURCES_DIR = Path("app/resources")
FILES_DIR = RESOURCES_DIR / "files"
QRC_FILE = RESOURCES_DIR / "main.qrc"
OUTPUT_FILE = RESOURCES_DIR / "rc_main.py"


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def is_rc_outdated() -> bool:
    if not OUTPUT_FILE.exists():
        return True
    built_at = OUTPUT_FILE.stat().st_mtime
    # The script itself counts too: changing the rcc command must rebuild the file
    sources = [
        Path(__file__),
        *(path for path in FILES_DIR.rglob("*") if path.is_file()),
    ]
    return any(path.stat().st_mtime > built_at for path in sources)


def build_qrc() -> str:
    """Map every file in FILES_DIR to the resource path ":/<path inside FILES_DIR>"."""

    groups: dict[PurePosixPath, list[PurePosixPath]] = defaultdict(list)
    for path in FILES_DIR.rglob("*"):
        relative = PurePosixPath(path.relative_to(FILES_DIR).as_posix())
        if path.is_file() and not any(part.startswith(".") for part in relative.parts):
            groups[relative.parent].append(relative)

    lines = ["<RCC>"]
    for directory in sorted(groups):
        prefix = "/" if directory == PurePosixPath() else f"/{directory}"
        lines.append(f'    <qresource prefix="{prefix}">')
        lines.extend(
            f'        <file alias="{file.name}">{FILES_DIR.name}/{file}</file>'
            for file in sorted(groups[directory])
        )
        lines.append("    </qresource>")
    lines.append("</RCC>")
    return "\n".join(lines) + "\n"


def build_rc() -> str:
    # Format 1 has no file timestamps, so the output depends only on the content
    command = ["pyside6-rcc", "--format-version", "1", str(QRC_FILE)]
    print(shlex.join(command))
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    # rcc writes CRLF on Windows, the repository stores .py files with LF
    return result.stdout.replace("\r\n", "\n")


def main() -> None:
    # A changed qrc covers added and removed files, mtime covers edited ones
    if write_if_changed(QRC_FILE, build_qrc()) or is_rc_outdated():
        write_if_changed(OUTPUT_FILE, build_rc())


if __name__ == "__main__":
    main()
