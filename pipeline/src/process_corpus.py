import requests
import json
from pathlib import Path
from typing import List
from common_utils.tetun_lid import TetunLid


class GetInitialCorpus:
    """
    This class is mainly responsible to:
    (1) Get a total of documents from the Solr.
    (2) Retrieve and process the crawled documents indexed in the Solr.
    (3) Apply the LID model and filter out documents that do not satisfy the predefined conditions.
    (4) Save each line of the documents that has a length > 50 to the initial corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path,
        initial_corpus_file_path: Path,
    ) -> None:
        self.solr_api_url = solr_api_url
        self.tetun_lang = tetun_lang
        self.lang_proba_threshold = lang_proba_threshold
        self.lid_model_file_path = lid_model_file_path
        self.tetun_lid = TetunLid(self.tetun_lang, self.lang_proba_threshold, lid_model_file_path)
        self.initial_corpus_file_path = initial_corpus_file_path

    def get_total_documents(self) -> int:
        """ Gets total documents from the Solr and return it. """

        params = {"q": "*:*", "rows": 0}
        response = requests.get(self.solr_api_url, params=params)
        response_json = response.json()
        total_doc = response_json["response"]["numFound"]

        return total_doc

    def get_documents(self) -> List[str]:
        """ Retrieves documents from the Solr and return their list. """

        params = {
            "q": "*:*",
            "wt": "json",
            "start": 0,
            "rows": 10,  # self.get_total_documents(),
        }

        response = requests.get(self.solr_api_url, params=params)
        data = json.loads(response.text)
        docs = [d.get("content") for d in data["response"]["docs"] if d.get("content") is not None]

        return docs

    def generate_initial_corpus(self) -> None:
        """
        Generates text corpus and:
        (1) Gets Tetun text that has a probability >= threshold.
        (2) Selects text that has a length > 50 and save them to the initial corpus file.
        """

        for doc in self.get_documents():
            text = doc.split("\n")
            # Init: Apply Tetun LID
            tetun_text = self.tetun_lid.get_tetun_text(text)
            # End
            for text in tetun_text:
                if len(text.strip()) > 50:
                    print("Initial added: ", text)
                    with self.initial_corpus_file_path.open("a", encoding="utf-8") as initial_file:
                        initial_file.write(text + "\n")

        # Add another \n to the end of each doc.
        with self.initial_corpus_file_path.open("a", encoding="utf-8") as initial_file:
            initial_file.write("\n")


class GetFinalCorpus:
    """
    This class generates final text docs and excludes the input texts that meet the predefined 
    filter conditions and blank lines more than two times in consecutive order.
    """

    def __init__(
        self,
        initial_corpus_file_path: Path,
        skipped_corpus_file_path: Path,
        final_corpus_file_path: Path,
        start_patterns: List[str],
        end_patterns: List[str],
        in_patterns: List[str],
    ) -> None:
        self.initial_corpus_file_path = initial_corpus_file_path
        self.skipped_corpus_file_path = skipped_corpus_file_path
        self.final_corpus_file_path = final_corpus_file_path
        self.start_patterns = start_patterns
        self.end_patterns = end_patterns
        self.in_patterns = in_patterns

    def is_text_to_filter(self, text_line: str) -> bool:
        """
        Checks if the given text meets the predefined filter conditions.

        :param text_line: the input text.
        :return: True if the given text meets, False otherwise.
        """

        text_to_filter = any(
            text_line.lower().startswith(start_pattern)
            or text_line.lower().endswith(end_pattern)
            or in_pattern in text_line.lower()
            for start_pattern in self.start_patterns
            for end_pattern in self.end_patterns
            for in_pattern in self.in_patterns
        )

        return text_to_filter

    def get_final_text(self, max_consecutive_newlines: int = 2,) -> None:
        """
        Gets the final text docs and excludes the input texts that meet the predefined filter conditions.

        :param max_consecutive_newlines: the maximum newlines allowed after each document.
        """

        with self.initial_corpus_file_path.open("r", encoding="utf-8") as initial_file:
            consecutive_newlines = 0
            for line in initial_file:
                line = line.strip()
                if self.is_text_to_filter(line):
                    print("Skipped: ", line)
                    with self.skipped_corpus_file_path.open("a", encoding="utf-8") as skipped_file:
                        skipped_file.write(line + "\n")
                    continue
                else:
                    if len(line) == 0:
                        consecutive_newlines += 1
                    else:
                        consecutive_newlines = 0
                    if len(line) == 0 and consecutive_newlines >= max_consecutive_newlines:
                        continue
                    else:
                        with self.final_corpus_file_path.open("a", encoding="utf-8") as final_file:
                            final_file.write(line + "\n")
                            # print("Final added: ", line)
