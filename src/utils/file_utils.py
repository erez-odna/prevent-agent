import os


def write_to_file(file, content):
    with open(file, "w") as f:
        f.write(content)
        f.flush()


def read_from_file(file):
    with open(file, "r") as f:
        return f.read()


def write_lines_to_file(file, lines, append_endline=True):
    if append_endline:
        lines = list(map(lambda l: f"{l}\n", lines))
    with open(file, "w") as f:
        f.writelines(lines)
        f.flush()


def dir_empty(dir_path):
    return not any([True for _ in os.scandir(dir_path)])
