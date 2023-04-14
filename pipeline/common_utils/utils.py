from pathlib import Path
from typing import List


def load_corpus(file_path: Path) -> List[str]:
    """
    Loads corpus from a file and returns its contents.

    :param file_path: a path to the file.
    :returns: a list of text.
    """

    try:
        with file_path.open("r", encoding="utf-8") as corpus_file:
            contents = [line.strip() for line in corpus_file]
    except FileNotFoundError:
        print(f"File not found at: {file_path}")
        return []
    except UnicodeDecodeError:
        print(f"Cannot decode file at: {file_path}")
        return []

    return contents
