from pathlib import Path
from typing import List
import tldextract


class Utils:
    """ This class contains functions to load and write a text corpus from/to a file. """

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load_corpus(self) -> List[str]:
        """ Loads corpus from a file and returns its contents in a list. """

        try:
            with self.file_path.open("r", encoding="utf-8") as load_file:
                contents = [line.strip() for line in load_file]

        except FileNotFoundError:
            print(f"File not found at: {self.file_path}")
            return []

        except UnicodeDecodeError:
            print(f"Cannot decode file at: {self.file_path}")
            return []

        return contents

    def load_final_corpus(self):
        """ Load and read the final corpus. """
        try:
            with self.file_path.open("r", encoding="utf-8") as load_file:
                contents = load_file.read()

        except FileNotFoundError:
            print(f"File not found at: {self.file_path}")
            return []

        return contents

    def load_sample_corpus(self) -> List[str]:
        """ Load and read the final corpus. """
        try:
            with self.file_path.open('r', encoding='utf-8') as load_sample_corpus:
                contents = load_sample_corpus.read().split('\n\n')

        except FileNotFoundError:
            print(f"File not found at: {self.file_path}")
            return []

        return contents

    def save_corpus(self, text_line: str = None, is_not_eol: bool = True):
        """ Save the text corpus (append), if it is an EOL then add a new line. """
        with self.file_path.open("a", encoding="utf-8") as write_file:
            if is_not_eol:
                write_file.write(text_line + "\n")
            else:
                write_file.write("\n")


def extract_domain(seed_url: str) -> str:
    """
    Gets the domain name from an url.

    :param url: the input url.
    :return: the domain or domain with subdomain name.
    """
    exctracted = tldextract.extract(seed_url)
    domain = exctracted.registered_domain
    subdomain = exctracted.subdomain
    if subdomain:
        domain = subdomain + "." + domain

    return domain
