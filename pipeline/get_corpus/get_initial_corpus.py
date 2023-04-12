import requests
import json
from pathlib import Path
from typing import List
from common_utils.tetun_lid import TetunLid


class GetInitialCorpus:
    """
    This class is mainly responsible to:
    (1) Retrieve and process the crawled documents indexed in Solr.
    (2) Apply the LID model and filter out documents that do not satisfy the predefined conditions.
    (3) For each line of the documents having a length > 50, save them to the initial corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        start_row: int,
        rows: int,
        tetun_lang: str,
        lang_proba_treshold: float,
        lid_model_file_path: Path,
    ) -> None:
        self.solr_api_url = solr_api_url
        self.start_row = start_row
        self.rows = rows
        self.tetun_lang = tetun_lang
        self.lang_proba_treshold = lang_proba_treshold
        self.tetun_lid = TetunLid(self.tetun_lang, self.lang_proba_treshold)
        self.lid_model_file_path = lid_model_file_path

    def get_documents(self) -> List[str]:
        """
        Retrieve documents from the Solr.

        :return: a list of text documents.
        """

        params = {
            "q": "*:*",
            "wt": "json",
            "start": self.start_row,
            "rows": self.rows,
        }

        response = requests.get(self.solr_api_url, params=params)
        data = json.loads(response.text)
        docs = [
            d.get("content")
            for d in data["response"]["docs"]
            if d.get("content") is not None
        ]

        return docs

    def generate_corpus(self, initial_corpus_file_path: Path) -> None:
        """
        Generate text corpus as per the following steps:
        (1) Get Tetun corpus with a probability >= threshold.
        (2) Select text having a length > 50 and save them to the initial corpus file.

        :param initial corpus_file_path: a path to initial corpus file.
        """

        for doc in self.get_documents():
            text = doc.split("\n")
            # Init: Apply Tetun LID
            tetun_text = self.tetun_lid.get_tetun_text(
                text, self.lid_model_file_path
            )
            # End
            for text in tetun_text:
                if len(text.strip()) > 50:
                    with initial_corpus_file_path.open(
                        "a", encoding="utf-8"
                    ) as f:
                        f.write(text + "\n")
                        print("Added: ", text)

            # Add an extra newline to the end of each document
            with initial_corpus_file_path.open("a", encoding="utf-8") as f:
                f.write("\n")
