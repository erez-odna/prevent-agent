from pathlib import Path
import os
import json


def write_to_file(file, content, is_bytes=False):
    flags = "wb" if is_bytes else "w"
    with open(file, flags, encoding=None if is_bytes else "utf-8") as f:
        f.write(content)
        f.flush()


def read_from_file(file, is_binary=False):
    flags = "rb" if is_binary else "r"
    with open(file, flags, encoding=None if is_binary else "utf-8") as f:
        return f.read()


def write_lines_to_file(file, lines, append_endline=True):
    if append_endline:
        lines = list(map(lambda l: f"{l}\n", lines))
    with open(file, "w", encoding="utf-8") as f:
        f.writelines(lines)
        f.flush()


def write_json_to_file(file, json_obj, indent=2):
    write_to_file(file, json.dumps(json_obj, indent=indent))


def read_json_from_file(json_file):
    return json.loads(read_from_file(json_file))


def dir_empty(dir_path):
    return not any(True for _ in os.scandir(dir_path))


def remove_tree(root):
    if not root.is_dir():
        return

    for p in root.iterdir():
        if p.is_dir():
            remove_tree(p)
        else:
            p.unlink()
    root.rmdir()


def get_files_in_dir(dir_path, expr="*.*"):
    if not Path(dir_path).is_dir():
        raise NotADirectoryError
    return list(dir_path.glob(expr))


def check_create_path(folder):
    folder_path = Path(folder) if isinstance(folder, str) else folder
    if not folder_path.is_dir():
        folder_path.mkdir(parents=True, exist_ok=True)
