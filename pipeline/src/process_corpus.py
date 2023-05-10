import requests
import json
import logging
from pathlib import Path
from typing import List
from common_utils.tetun_lid import TetunLid
from common_utils.utils import Utils
from common_utils.docs_process import DocumentProcess
from common_utils import config


class GetCorpus:
    """
    This class is mainly responsible to:
    (1) Apply LID model for each document title and collect only those that satisfy the predefined threshold.
    (2) For each title in (3), save it along with the respective URL, and apply LID model to its content.
    (3) Save each line on the content that hat satisfy the predefined threshold to the final corpus file.
    """

    def __init__(
        self,
        solr_api_url: str,
        start_solr_docs: int,
        total_solr_docs: int,
        tetun_lang: str,
        lang_proba_threshold: float,
        lid_model_file_path: Path,
        final_corpus_file_path: Path,
    ) -> None:
        self.tetun_lid = TetunLid(tetun_lang, lang_proba_threshold, lid_model_file_path)
        self.final_corpus = Utils(final_corpus_file_path)
        self.document_process = DocumentProcess(solr_api_url, start_solr_docs, total_solr_docs)
        logging.basicConfig(
            filename=config.LOG_FILE,
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s: %(message)s"
        )

    def generate_corpus(self, max_consecutive_newlines: int = 2) -> None:
        """
        Generates text corpus and:
        (1) Get all the document titles.
        (2) Apply Tetun LID to collect only titles in Tetun with a probability >= threshold.
        (3) Save title, url and its content that has a proba >= threshold to the final corpus file.
        (4) Add a newline to the end of each document.
        """
        
        logging.info("Generating final corpus...")
        logging.info("Generating titles...")
        get_titles = [d.get("title") for d in self.document_process.get_documents() if d.get("title") is not None]
        logging.info("Validating titles...")
        valid_titles = self.tetun_lid.get_tetun_text(get_titles)
        valid_titles_unique = list(set(valid_titles))

        for doc in self.document_process.get_documents():
            title = doc.get("title")
            url = doc.get("url")
            content = doc.get("content")

            if title in valid_titles_unique and '/feed' not in url and '/tag' not in url: # Urls contain '/feed' and '/tag' are excluded.
                if "wikipedia" in url and not "tet.wikipedia.org" in url: # Ensure that only Tetun wikipedia data is processed.
                    continue
                if "wikidata" in url: # The wikidata for Tetun does not exist.
                    continue

                self.final_corpus.save_corpus(title)
                self.final_corpus.save_corpus(url)

                consecutive_newlines = 0
                seen_sentences = set()
                text_lines = content.split("\n")
                tetun_text = self.tetun_lid.get_tetun_text(text_lines)  # Apply Tetun LID
                for index, doc in enumerate(tetun_text):
                    text_line = doc.strip()
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

        logging.info("The final corpus has been generated sucessfully.")
