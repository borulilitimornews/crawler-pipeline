import requests
import json
from utils import load_lid_model
from pathlib import Path
from typing import List


class GetInitialCorpus:
    """
    This class is mainly responsible to:
    1. Process the crawled documents indexed in Solr.
    2. Read each line of each document and apply the LID model.
    3. Save to the initial corpus file the text lines that has a probability 
    score >= predefined threshold
    """

    def __init__(self, solr_api_url: str, start_row: int, rows: int, lang_proba_treshold) -> None:
        self.solr_api_url = solr_api_url
        self.start_row = start_row
        self.rows = rows
        self.lang_proba_treshold = lang_proba_treshold

    def get_documents(self) -> List[str]:
        """
        Retrieve the documents from Solr.

        :param start: the start row.
        :param rows: a total of rows.
        :return: a list of text documents.
        """

        params = {"q": "*:*", "wt": "json",
                  "start": self.start_row, "rows": self.rows}

        # Send a GET request to the Solr API
        response = requests.get(self.solr_api_url, params=params)

        data = json.loads(response.text)
        docs = [d.get("content") for d in data["response"]
                ["docs"] if d.get("content") is not None]

        return docs

    def is_tetun_text(self, lid_model_file_path: Path, text: str) -> bool:
        """
        Check if the given text has a probability of being Tetun >= predefined threshold.

        :param lid_model_file_path: a path to the LID model file.
        :param text: an input text.
        :return: True if the given text has a probability >= predefined threshold, otherwise False
        """

        lid_model = load_lid_model(lid_model_file_path)

        tetun_text = False
        pred_probs = lid_model.predict_proba([text])
        for probs in pred_probs:
            for j, lang in enumerate(lid_model.classes_):
                if lang == 'tet' and round(probs[j], 2) >= self.lang_proba_treshold:
                    tetun_text = True

        return tetun_text

    def generate_corpus(self, lid_model_file_path: Path, initial_corpus_file_path: Path) -> None:
        """
        Generate the corpus as per the following steps:
        1. For each document, read each line.
        2. Select only lines with a length higher than 50.
        3. Add to the corpus if it has a probability of being Tetun >= predefined threshold.

        :param start: the start row.
        :param rows: a total of rows.
        :param lid_model_file_path: a path to the LID model file.
        :param initial corpus_file_path: a path to initial corpus file.
        :return: a conclusion message.
        """

        for doc in self.get_documents():
            texts = doc.split('\n')
            for text in texts:
                print("Read: ", text)
                if len(text.strip()) > 50 and self.is_tetun_text(lid_model_file_path, text):
                    with initial_corpus_file_path.open('a', encoding='utf-8') as f:
                        f.write(text + '\n')
                        print("Added: ", text)

            # Add an extra newline to the end of each document
            with initial_corpus_file_path.open('a', encoding='utf-8') as f:
                f.write('\n')
