import requests
import json
from pathlib import Path
from typing import List
from common_utils.tetun_lid import TetunLid


class GetInitialCorpus:
    """
    This class is mainly responsible to:
    (1) Get total of documents indexed in the Solr.
    (2) Retrieve and process the crawled documents indexed in the Solr.
    (3) Apply the LID model and filter out documents that do not satisfy the predefined conditions.
    (4) For each line of the documents having a length > 50, save them to the initial corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        # start_row: int,
        # rows: int
        tetun_lang: str,
        lang_proba_treshold: float,
        lid_model_file_path: Path,
    ) -> None:
        self.solr_api_url = solr_api_url
        # self.start_row = start_row
        # self.rows = rows
        self.tetun_lang = tetun_lang
        self.lang_proba_treshold = lang_proba_treshold
        self.tetun_lid = TetunLid(self.tetun_lang, self.lang_proba_treshold)
        self.lid_model_file_path = lid_model_file_path

    def get_total_documents(self) -> int:
        """ 
        Get total documents from the Solr. 

        :return: the total documents. 
        """

        params = {"q": "*:*", "rows": 0}
        response = requests.get(self.solr_api_url, params=params)
        response_json = response.json()
        total_doc = response_json["response"]["numFound"]

        return total_doc

    def get_documents(self) -> List[str]:
        """
        Retrieve documents from the Solr.

        :return: a list of text documents.
        """

        params = {
            "q": "*:*",
            "wt": "json",
            "start": 0,  # self.start_row,
            "rows": self.get_total_documents(),  # self.rows
        }

        response = requests.get(self.solr_api_url, params=params)
        data = json.loads(response.text)
        docs = [
            d.get("content")
            for d in data["response"]["docs"]
            if d.get("content") is not None
        ]

        return docs

    def generate_initial_corpus(self) -> List[str]:
        """
        Generate text corpus and:
        (1) Get Tetun corpus with a probability >= threshold.
        (2) Select text having a length > 50 and save them to the initial corpus file.

        :param initial corpus_file_path: a path to initial corpus file.
        :return: a list contains initial corpus.
        """
        initial_corpus = []
        for doc in self.get_documents():
            text = doc.split("\n")
            # Init: Apply Tetun LID
            tetun_text = self.tetun_lid.get_tetun_text(
                text, self.lid_model_file_path
            )
            # End
            for text in tetun_text:
                if len(text.strip()) > 50:
                    print("Initial added: ", text)
                    initial_corpus.append(text + "\n")

            # Add another newline to the end of each document.
            initial_corpus.append("\n")

        return initial_corpus


class GetFinalCorpus:
    """
    A class to filter the input text that meets the predefined filter conditions 
    and blank lines more than two times in consecutive order.
    """

    def __init__(
        self,
        generate_initial_corpus,
        get_skipped_corpus_file_path,
        start_patterns,
        end_patterns,
        in_patterns,
    ) -> None:
        self.generate_initial_corpus = generate_initial_corpus
        self.start_patterns = start_patterns
        self.end_patterns = end_patterns
        self.in_patterns = in_patterns
        self.get_skipped_corpus_file_path = get_skipped_corpus_file_path

    def is_text_to_filter(self, text_line: str) -> bool:
        """
        Check if the given text meets the predefined filter conditions.

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

    def get_final_text(
        self,
        final_corpus_file_path: Path,
        get_skipped_corpus_file_path: Path,
        max_consecutive_newlines: int = 2,
    ) -> str:
        """
        Filtered the input text that meets the predefined filter conditions.

        :param initial_corpus_file_path: a path to the input file.
        :param final_corpus_file_path: a path to the output file.
        :param max_consecutive_newlines: the maximum newlines allowed after each document.
        :return: a conclusion message.
        """
        unique_sentences = []
        seen_sentences = set()
        consecutive_newlines = 0

        for line in self.generate_initial_corpus:
            line = line.strip()
            if self.is_text_to_filter(line):
                print("Skipped: ", line)
                with get_skipped_corpus_file_path.open(
                    "a", encoding="utf-8"
                ) as f:
                    f.write(line + "\n")
                continue

            if line not in seen_sentences:
                if len(line) == 0:
                    consecutive_newlines += 1
                else:
                    consecutive_newlines = 0
                if (
                    len(line) == 0
                    and consecutive_newlines >= max_consecutive_newlines
                ):
                    continue
                else:
                    unique_sentences.append(line)
                    if len(line) > 0:
                        seen_sentences.add(line)
                    # print("Final added: ", line)

        with final_corpus_file_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(unique_sentences))

        return f"Total unique sentences: {len(unique_sentences)}"

