import gzip
from typing import Iterator


def open_text_maybe_gzip(path: str):
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")


def iter_lines(path: str) -> Iterator[str]:
    with open_text_maybe_gzip(path) as f:
        for line in f:
            yield line.strip()