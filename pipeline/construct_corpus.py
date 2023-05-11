from common_utils import config
from src.process_corpus import GetCorpus


class ConstructCorpus:
    """ This class generates texts for the Tetun corpus and save them in a file. """

    def __init__(self) -> None:
        self.get_corpus = GetCorpus(
            config.SOLR_API_URL,
            config.START_SOLR_DOCS,
            #config.TOTAL_SOLR_DOCS,
            config.LANGUAGE,
            config.LANG_PROBA_THRESHOLD,
            config.LID_MODEL_FILE_PATH,
            config.FINAL_CORPUS_FILE_PATH,
        )

    def run(self) -> None:
        try:
            self.get_corpus.generate_corpus()
            #print("\nThe final corpus has been generated sucessfully.\n\n")

        except Exception as e:
            print(f"\nError while generating the final corpus: {e}\n")


if __name__ == "__main__":
    build_corpus = ConstructCorpus()
    build_corpus.run()
