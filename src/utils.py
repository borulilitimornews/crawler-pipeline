import joblib
from pathlib import Path
from typing import List


def load_corpus(file_path: Path) -> List[str]:
    """
    Load dataset for initial seeding.

    :param file_path: a path to file.
    :returns: a string corpus.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            contents = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"File not found at: {file_path}")
        return []
    except UnicodeDecodeError:
        print(f"Cannot decode file at: {file_path}")
        return []
    # print(contents)

    return contents


def load_lid_model(lid_model_file_path: Path) -> object:
    """ 
    Load Tetun language identification model 

    :param lid_model_file_path: a path to the Tetun LID model file.
    :return: Tetun LID model.
    """
    if not lid_model_file_path.exists():
        print(f"Model file not found at: {lid_model_file_path}")
        return []
    model = joblib.load(lid_model_file_path)

    return model
