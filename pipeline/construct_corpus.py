from common_utils import config
from src.get_corpus import GetCorpus


class ConstructCorpus:
    """ This class generates text pages for the Tetun corpus and save them in a file. """

    def __init__(self) -> None:
        self.get_corpus = GetCorpus(
            config.SOLR_API_URL,
            config.SOLR_START,
            config.SOLR_ROWS,
            config.MAX_CONSECUTIVE_NEW_LINE,
            config.LANGUAGE,
            config.LANG_PROBA_THRESHOLD,
            config.LID_MODEL_FILE_PATH,
            config.FINAL_CORPUS_FILE_PATH,
        )

    def run(self) -> None:
        try:
            self.get_corpus.generate_corpus()
            print("\nThe final corpus has been generated sucessfully.\n\n")

        except Exception as e:
            print(f"\nError while generating the final corpus: {e}\n")


if __name__ == "__main__":
    construct_corpus = ConstructCorpus()
    construct_corpus.run()
