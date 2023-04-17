import requests
import json
from pathlib import Path
from typing import List
from common_utils.tetun_lid import TetunLid
from common_utils.utils import Utils


class GetCorpus:
    """
    This class is mainly responsible to:
    (1) Get a total of documents from the Solr.
    (2) Retrieve and process the crawled documents indexed in the Solr.
    (3) Apply the LID model and filter out documents that do not satisfy the predefined conditions.
    (4) Save each unique line of the documents that has a length > 50 to the initial corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path,
        start_patterns: List[str],
        end_patterns: List[str],
        in_patterns: List[str],
        skipped_corpus_file_path: Path,
        final_corpus_file_path: Path,
    ) -> None:
        self.solr_api_url = solr_api_url
        self.tetun_lang = tetun_lang
        self.lang_proba_threshold = lang_proba_threshold
        self.lid_model_file_path = lid_model_file_path
        self.tetun_lid = TetunLid(self.tetun_lang, self.lang_proba_threshold, lid_model_file_path)
        self.start_patterns = start_patterns
        self.end_patterns = end_patterns
        self.in_patterns = in_patterns
        self.skipped_corpus = Utils(skipped_corpus_file_path)
        self.final_corpus = Utils(final_corpus_file_path)

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
            "rows": self.get_total_documents(),
        }
        response = requests.get(self.solr_api_url, params=params)
        data = json.loads(response.text)
        docs = [d.get("content") for d in data["response"]["docs"] if d.get("content") is not None]

        return docs

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

    def generate_corpus(self, max_consecutive_newlines: int = 2) -> None:
        """
        Generates text corpus and:
        (1) Gets Tetun text that has a probability >= threshold.
        (2) Selects text that has a length > 50 and save them to the final corpus file.
        (3) Add a newline to the end of each document.
        """

        consecutive_newlines = 0
        seen_sentences = set()
        for doc in self.get_documents():
            text = doc.split("\n")
            tetun_text = self.tetun_lid.get_tetun_text(text)  # Apply Tetun LID
            for index, doc in enumerate(tetun_text):
                text_line = doc.strip()
                if len(text_line) > 50:
                    print("Initial added: ", text_line)
                    if self.is_text_to_filter(text_line):
                        print("Skipped: ", text_line)
                        self.skipped_corpus.save_corpus(text_line)
                        continue
                    if text_line not in seen_sentences:
                        if len(text_line) == 0:
                            consecutive_newlines += 1
                        else:
                            consecutive_newlines = 0
                        if len(text_line) == 0 and consecutive_newlines == max_consecutive_newlines:
                            continue
                        else:
                            self.final_corpus.save_corpus(text_line)
                            # Add a new line at the end of each non-empty document
                            if index == len(tetun_text) - 1:
                                self.final_corpus.save_corpus(is_not_eol=False)
                            if len(text_line) > 0:
                                seen_sentences.add(text_line)
